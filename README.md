# 🔮 Live Token Predictor

Real-time GPT-4o token prediction with log probabilities as you type!

## ✨ Features

- **Live Predictions**: See next token predictions as you type
- **Log Probabilities**: View actual model confidence scores
- **Real-time Updates**: Auto-update predictions as text changes
- **Visual Probability Bars**: Easy-to-read probability visualization
- **Prediction History**: Track recent predictions
- **GPT-4o Powered**: Uses OpenAI's latest model

## 🚀 Quick Start

### Method 1: Using the script
```streamlit run live_token_predictor.py
```

### Method 2: Manual setup
```bash
# Install dependencies
pip3 install -r requirements_token_predictor.txt

# Run the app
/usr/bin/python3 -m streamlit run live_token_predictor.py --server.port 8504
```

### Method 3: Direct launch
```bash
streamlit run live_token_predictor.py --server.port 8504
```

## 🔑 API Key Setup

### Option 1: Environment Variable
Create a `.env` file:
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Option 2: UI Input
Enter your API key directly in the sidebar when the app starts.

### Getting an API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and use it in the app

## 📱 How to Use

1. **Enter API Key**: Either in `.env` file or the sidebar
2. **Start Typing**: Type in the text area
3. **Watch Predictions**: See real-time token predictions
4. **Explore**: Try different text types and see how predictions change

## 🎯 Example Use Cases

### Creative Writing
```
"The mysterious door slowly opened to reveal..."
```
**Predictions might show:**
- " a" (45.2%)
- " an" (23.1%)
- " darkness" (8.9%)

### Code Completion
```
"def calculate_fibonacci(n):"
```
**Predictions might show:**
- "\n" (67.3%)
- " if" (15.2%)
- " return" (9.1%)

### News Headlines
```
"Breaking: Scientists discover new"
```
**Predictions might show:**
- " species" (28.4%)
- " planet" (21.7%)
- " treatment" (19.3%)

## 🔬 Understanding the Output

### Metrics Explained
- **Token**: The actual text piece (word, punctuation, etc.)
- **Probability**: Likelihood as percentage (0-100%)
- **Log Prob**: Raw model score (always negative)
- **Color Coding**:
  - 🟢 Green: High confidence (>20%)
  - 🟡 Yellow: Medium confidence (5-20%)
  - 🔴 Red: Low confidence (<5%)

### Temperature Setting
- Uses **0.3 temperature** for more predictable, focused predictions
- Lower = more deterministic predictions
- Higher = more creative/random predictions

## 🛠️ Advanced Features

### Auto-Update Mode
- Enable "Auto-update predictions" for real-time updates
- Automatically fetches new predictions as you type
- Can be disabled for manual control

### Prediction Count
- Adjust slider to show 1-10 top predictions
- More predictions = broader view of model uncertainty
- Fewer predictions = focus on top choices

### Prediction History
- Tracks your last 10 prediction sessions
- Shows text snippets and top 3 predictions
- Helps analyze model behavior patterns

## 🚨 Usage Notes

### API Costs
- Each prediction = 1 API call to GPT-4o
- Costs approximately $0.03 per 1K tokens
- Auto-update mode will make frequent calls

### Rate Limits
- OpenAI has rate limits on API calls
- If you hit limits, wait a moment before continuing
- Consider disabling auto-update for heavy usage

### Privacy
- Your text is sent to OpenAI for processing
- Don't input sensitive/confidential information
- API keys are stored locally only

## 🐛 Troubleshooting

### "No API Key" Error
- Check your API key is valid
- Ensure it has GPT-4o access
- Try entering key in UI if `.env` doesn't work

### "Prediction Failed" Error
- Check internet connection
- Verify API key has sufficient credits
- Try shorter text input

### App Won't Start
- Check Python 3.9+ is installed
- Install requirements: `pip3 install -r requirements_token_predictor.txt`
- Try running with `/usr/bin/python3 -m streamlit run ...`

## 🔗 Running Multiple Apps

- **Token Predictor**: http://localhost:8504

Both apps can run simultaneously!

## 💡 Tips for Best Results

1. **Complete thoughts**: End sentences with periods for clearer predictions
2. **Context matters**: Longer context = better predictions
3. **Domain-specific**: Technical text gives different predictions than creative writing
4. **Experiment**: Try different writing styles and topics
5. **Watch patterns**: Notice how model confidence changes with context

## 🎓 Educational Value

Perfect for:
- **Understanding AI**: See how language models work internally
- **Writing assistance**: Discover unexpected word choices
- **AI research**: Analyze model behavior and biases
- **Creative inspiration**: Use predictions to overcome writer's block
- **Language learning**: See natural language patterns

---

*Happy token predicting! 🔮✨*
