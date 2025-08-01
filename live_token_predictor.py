#!/usr/bin/env python3
"""
Live Token Predictor with Log Probabilities
GPT-4o token prediction as you type
"""

import streamlit as st
import openai
import time
import json
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import asyncio
import threading

# Load environment variables
load_dotenv()

class TokenPredictor:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        
    def get_token_predictions(self, text: str, max_tokens: int = 1) -> Dict:
        """Get next token predictions with log probabilities"""
        try:
            # Create a completion prompt that forces next-token prediction
            prompt = f"{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Complete the text with just the next most likely word or token. Do not rewrite or correct the input text - just add what naturally comes next."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.1,  # Very low temperature for focused predictions
                logprobs=True,
                top_logprobs=10  # Get top 10 token predictions
            )
            
            if response.choices and response.choices[0].logprobs:
                logprobs_data = response.choices[0].logprobs
                return {
                    'success': True,
                    'predictions': self._format_chat_predictions(logprobs_data),
                    'generated_text': response.choices[0].message.content,
                    'model_used': self.model
                }
            else:
                return {'success': False, 'error': 'No logprobs returned'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _format_chat_predictions(self, logprobs_data) -> List[Dict]:
        """Format chat completions logprobs data into readable predictions"""
        predictions = []
        
        if logprobs_data.content and len(logprobs_data.content) > 0:
            # Get the first token's logprobs
            first_token_logprobs = logprobs_data.content[0]
            
            if hasattr(first_token_logprobs, 'top_logprobs') and first_token_logprobs.top_logprobs:
                for logprob_item in first_token_logprobs.top_logprobs:
                    token = logprob_item.token
                    logprob = logprob_item.logprob
                    probability = 2 ** logprob  # Convert log probability to probability
                    predictions.append({
                        'token': token,
                        'logprob': logprob,
                        'probability': probability,
                        'percentage': probability * 100
                    })
        
        # Sort by probability (highest first)
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        return predictions
    
    def _format_predictions(self, logprobs_data) -> List[Dict]:
        """Legacy format - keeping for compatibility"""
        return self._format_chat_predictions(logprobs_data)

def init_session_state():
    """Initialize Streamlit session state"""
    if 'last_prediction_text' not in st.session_state:
        st.session_state.last_prediction_text = ""
    if 'predictions' not in st.session_state:
        st.session_state.predictions = []
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []

def main():
    st.set_page_config(
        page_title="Live Token Predictor",
        page_icon="🔮",
        layout="wide"
    )
    
    st.title("🔮 Live Token Predictor")
    st.markdown("*See GPT-4o's next token predictions with log probabilities in real-time!*")
    
    init_session_state()
    
    # API Key Configuration
    st.sidebar.header("🔑 OpenAI Configuration")
    
    # Try to get API key from environment or session state
    env_key = os.getenv('OPENAI_API_KEY')
    session_key = st.session_state.get('openai_api_key', '')
    
    if env_key:
        api_key = env_key
        st.sidebar.success("✅ API Key loaded from environment")
        masked_key = env_key[:8] + "..." + env_key[-4:] if len(env_key) > 12 else "***"
        st.sidebar.text(f"Key: {masked_key}")
    else:
        api_key = st.sidebar.text_input(
            "OpenAI API Key:",
            value=session_key,
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        if api_key:
            st.session_state.openai_api_key = api_key
            st.sidebar.success("✅ API Key entered")
        else:
            st.sidebar.error("❌ No API Key")
    
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to start predicting!")
        st.markdown("""
        ### Getting Started:
        1. 🔑 Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
        2. 📝 Enter it in the sidebar
        3. ✍️ Start typing in the text area below
        4. 🔮 Watch real-time token predictions appear!
        """)
        return
    
    # Initialize predictor
    try:
        predictor = TokenPredictor(api_key)
    except Exception as e:
        st.error(f"❌ Failed to initialize predictor: {e}")
        return
    
    # Main interface
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("✍️ Live Writing Input")
        
        # Text input area
        user_text = st.text_area(
            "Start typing to see predictions:",
            height=200,
            key="text_input",
            placeholder="Once upon a time, in a land far away..."
        )
        
        # Debug display
        if user_text:
            st.caption(f"*Current input: '{user_text}' (length: {len(user_text)})*")
        
        # Settings
        st.subheader("⚙️ Prediction Settings")
        show_count = st.slider("Number of predictions to show:", 1, 10, 5)
        auto_update = st.checkbox("Auto-update predictions", value=True)
        
        if st.button("🔮 Predict Next Token") or (auto_update and user_text != st.session_state.last_prediction_text):
            if user_text.strip():
                with st.spinner("🤖 Getting predictions..."):
                    result = predictor.get_token_predictions(user_text)
                    
                    if result['success']:
                        st.session_state.predictions = result['predictions'][:show_count]
                        st.session_state.last_prediction_text = user_text
                        
                        # Add to history
                        st.session_state.prediction_history.append({
                            'text': user_text,
                            'predictions': result['predictions'][:3],  # Store top 3
                            'timestamp': time.time()
                        })
                        
                        # Keep only last 10 predictions in history
                        if len(st.session_state.prediction_history) > 10:
                            st.session_state.prediction_history = st.session_state.prediction_history[-10:]
                    else:
                        st.error(f"❌ Prediction failed: {result['error']}")
    
    with col2:
        st.subheader("🔮 Next Token Predictions")
        
        if st.session_state.predictions:
            st.markdown(f"*Predictions for text: **{st.session_state.last_prediction_text}***")
            st.caption(f"*Debug: Full input length: {len(st.session_state.last_prediction_text)} characters*")
            
            # Display predictions in a nice format
            for i, pred in enumerate(st.session_state.predictions):
                token = pred['token']
                percentage = pred['percentage']
                logprob = pred['logprob']
                
                # Create a visual probability bar
                bar_width = int(percentage * 2)  # Scale for display
                bar = "█" * min(bar_width, 50)
                
                # Color code by probability
                if percentage > 20:
                    color = "🟢"  # High probability
                elif percentage > 5:
                    color = "🟡"  # Medium probability
                else:
                    color = "🔴"  # Low probability
                
                # Display with formatting
                token_display = repr(token) if token.strip() != token else f'"{token}"'
                
                st.markdown(f"""
                **{i+1}.** {color} {token_display}
                - **Probability:** {percentage:.2f}%
                - **Log Prob:** {logprob:.3f}
                - {bar}
                """)
            
            # Show what the model would generate
            st.markdown("---")
            st.subheader("🎯 Model's Top Choice")
            if st.session_state.predictions:
                top_choice = st.session_state.predictions[0]
                st.success(f"Next token: **{repr(top_choice['token'])}** ({top_choice['percentage']:.1f}%)")
                
                # Show how the text would continue
                preview_text = st.session_state.last_prediction_text + top_choice['token']
                st.text_area("Preview with next token:", value=preview_text, height=100, disabled=True)
        
        else:
            st.info("👆 Start typing in the text area to see predictions!")
            
            # Show example predictions
            st.markdown("### 📖 Example Predictions")
            st.markdown("""
            When you type "The weather today is", you might see:
            
            🟢 **" sunny"** - 35.2% (logprob: -1.04)
            🟡 **" cloudy"** - 18.7% (logprob: -1.67)
            🟡 **" rainy"** - 12.3% (logprob: -2.10)
            🔴 **" cold"** - 8.9% (logprob: -2.42)
            🔴 **" warm"** - 6.1% (logprob: -2.80)
            """)
    
    # Prediction History
    if st.session_state.prediction_history:
        st.markdown("---")
        st.subheader("📚 Recent Prediction History")
        
        with st.expander("View prediction history", expanded=False):
            for i, entry in enumerate(reversed(st.session_state.prediction_history[-5:])):
                st.markdown(f"**{len(st.session_state.prediction_history)-i}.** Text: *{entry['text'][-50:]}...*")
                for j, pred in enumerate(entry['predictions']):
                    st.write(f"   {j+1}. {repr(pred['token'])} ({pred['percentage']:.1f}%)")
                st.markdown("---")
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### 💡 About Log Probabilities
    - **Log Probability**: The natural logarithm of the token probability (always negative)
    - **Probability**: Converted from logprob (2^logprob), shows actual likelihood
    - **Higher percentage** = more confident prediction
    - **Temperature 0.7** used for balanced creativity vs. predictability
    
    ### 🔬 How it works:
    1. Your text is sent to GPT-4o
    2. Model returns top 10 most likely next tokens
    3. Each token has a log probability score
    4. We convert and display as percentages for easy reading
    """)

if __name__ == "__main__":
    main()
