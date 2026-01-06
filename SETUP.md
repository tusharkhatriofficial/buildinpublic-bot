# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Git
- Twitter Developer Account
- Groq API Account (free)

## Step-by-Step Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/twitter-bot.git
cd twitter-bot
```

### 2. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get API Keys

**Twitter API:**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create app with "Read and Write" permissions
3. Generate API keys and tokens

**Groq API:**
1. Go to https://console.groq.com/
2. Sign up (free)
3. Create API key

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 6. Add Your Project
```bash
cp -r /path/to/your/project code/
```

### 7. Build Knowledge Base
```bash
python bot.py analyze
```

### 8. Test
```bash
python bot.py test
```

### 9. Post First Tweet
```bash
python bot.py post-now
```

### 10. Run Daily (Optional)
```bash
python bot.py  # Runs continuously, posts daily
```

## Troubleshooting

**Rate Limit Errors?**
- Make sure you ran `python bot.py analyze` first

**403 Forbidden on Tweet Post?**
- Check Twitter app has "Read and Write" permissions
- Regenerate Access Token & Secret after changing permissions

**No LLM Insights?**
- Verify GROQ_API_KEY in .env file
- Check Groq API quota at console.groq.com

## Need Help?
Open an issue on GitHub!
