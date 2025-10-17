# Setting Up Your API Key for CodeForge

CodeForge uses **Google's Gemini API** to generate code. You need a valid API key to use the code generation features.

## 🔑 Getting Your API Key

### Step 1: Get a Free API Key from Google AI Studio

1. Visit: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the generated API key (starts with `AIza...`)

### Step 2: Configure Your API Key

#### Option A: Update the `.env` file (Recommended)

1. Open `/backend/.env` in your text editor
2. Replace the line:
   ```
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
   with:
   ```
   GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   ```
3. Save the file

#### Option B: Set Environment Variable

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Step 3: Restart the Backend Server

After updating the API key:

```bash
# Stop the current backend server (Ctrl+C)
# Then restart it:
cd backend
source venv/bin/activate
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## ✅ Verify It's Working

1. Open http://localhost:3000
2. Go to the **Generate** tab
3. Try generating a simple app like "Create a button that changes color when clicked"
4. If configured correctly, it should generate code!

## 💰 API Costs

- **Free Tier**: Google AI Studio provides a generous free tier
- **Rate Limits**: 60 requests per minute for free tier
- **No Credit Card Required** for the free tier

## 🔒 Security Notes

- **Never commit** your API key to git
- The `.env` file is in `.gitignore` to protect your key
- Keep your API key private and secure

## 🆘 Troubleshooting

### Error: "API key not configured"
- Make sure you've updated the `.env` file with your real API key
- Restart the backend server after changing the `.env` file

### Error: "Failed to parse AI response"
- This usually means the API key is invalid or expired
- Generate a new API key from Google AI Studio
- Check that you copied the entire key (including the `AIza` prefix)

### Error: "Rate limit exceeded"
- You've exceeded the free tier limits
- Wait a few minutes and try again
- Consider upgrading to a paid plan for higher limits

## 📚 Additional Resources

- **Google AI Studio**: https://aistudio.google.com/
- **Gemini API Docs**: https://ai.google.dev/gemini-api/docs
- **Pricing Info**: https://ai.google.dev/pricing

---

**Questions?** Check the main README.md or open an issue on GitHub.

