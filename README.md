# 🤖 Twitter Bot - Build in Public

An intelligent Twitter bot that analyzes your **entire codebase** (Java, Python, JavaScript, TypeScript, etc.) and posts engaging daily tweets about your development journey. Perfect for building in public!

## ✨ Key Features

- 🔍 **Universal Code Analysis** - Analyzes ANY programming language (Java, Python, JS, TS, Go, Rust, etc.)
- 📅 **Chronological Tweets** - Uses Git commit history to tweet in order (earliest work first)
- 🤖 **AI-Powered** - Uses Groq's Llama 3.3 70B to generate human-like, engaging tweets
- 📱 **Daily Automated Tweets** - Posts one engaging tweet per day
- 🎯 **Smart Content** - Creates diverse tweet types based on actual commits and progress
- 🚫 **Duplicate Prevention** - Never posts the same content twice
- 💬 **No Emojis** - Clean, professional tweets that sound genuinely human
- 🔒 **280 Character Limit** - Respects Twitter's free account limitations

## 🎯 How It Works

1. **Analyzes your Git repository** - Reads commit history chronologically
2. **Understands what you built** - Detects languages, frameworks, features, fixes
3. **Generates engaging tweets** - Uses AI to create compelling narratives about your work
4. **Posts in order** - Tweets follow your actual development journey from beginning to end
5. **Tracks progress** - Remembers what's been posted, never repeats

## 📋 Prerequisites

- Python 3.8 or higher
- Twitter Developer Account with API access
- Groq API key (free at [console.groq.com](https://console.groq.com/))
- A `code` folder with your project (can be ANY language)

## 🚀 Quick Start

### 1. Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/twitter-bot.git
cd twitter-bot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Twitter API Credentials

Follow these steps carefully to get your Twitter API keys:

#### Step 1: Create Twitter Developer Account
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Apply for a developer account (usually approved instantly for basic access)

#### Step 2: Create a Project and App
1. Click **"+ Create Project"**
2. Enter project name (e.g., "Build in Public Bot")
3. Select use case: **"Making a bot"**
4. Enter project description
5. Create an App within the project

#### Step 3: Configure App Settings
1. Go to your App Settings
2. Click **"User authentication settings"** → **"Set up"**
3. Configure as follows:
   - **App permissions**: Select **"Read and Write"** (CRITICAL!)
   - **Type of App**: Select **"Web App, Automated App or Bot"**
   - **Callback URI**: Enter `http://localhost:3000` (required but not used)
   - **Website URL**: Enter your GitHub repo URL
4. Click **"Save"**

#### Step 4: Generate Keys and Tokens
1. Go to **"Keys and tokens"** tab
2. **API Key and Secret** (Consumer Keys):
   - Click **"Regenerate"** if already generated
   - Copy both and save securely
3. **Bearer Token**:
   - Click **"Regenerate"** if needed
   - Copy and save
4. **Access Token and Secret**:
   - Click **"Generate"** (MUST do this AFTER setting Read and Write permissions!)
   - Copy both and save securely

#### Step 5: Verify Permissions
- Make sure Access Token shows **"Read and Write"** permissions
- If it says "Read-only", you need to:
  1. Delete the current Access Token
  2. Set permissions to "Read and Write" in User authentication settings
  3. Generate new Access Token and Secret

**⚠️ Important Notes:**
- Keep all keys private and secure
- Never commit them to Git (use .env file)
- Bearer Token is optional but recommended
- Access Token must be generated AFTER setting Read and Write permissions

### 5. Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Create an API key

### 6. Configure Environment Variables

Copy the example environmcredentials:

```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

GROQ_API_KEY=your_groq_api_key_here

# Schedule time (24-hour format, e.g., 10:00, 14:30)
TWEET_TIME=10:00
```

### 7ER_BEARER_TOKEN=your_bearer_token_here

# Schedule time (24-hour format, e.g., 10:00, 14:30)
TWEET_TIME=10:00
```

### 5. Add Your Code

**Simply copy your entire project** to the `code/` folder:

```bash
# Example: Copy your project
cp -r ~/your-awesome-project/* code/
```

The bot works with **ANY programming language**:
- ✅ Java (Spring Boot, Maven, Gradle)
- ✅ Python (Django, Flask, FastAPI)
- ✅ JavaScript/TypeScript (React, Node.js, Next.js)
- ✅ Go, Rust, C++, and more!

**Im8ortant:** The bot analyzes **Git commit history**, so make sure your project is a Git repository.

### 6. Build Knowledge Base (IMPORTANT - First Time Only)

Before posting tweets, analyze your codebase once to avoid rate limits:

```bash
python bot.py analyze
```

This command will:
- ✅ Analyze all commits using LLM for rich insights
- ✅ Cache everything in `commit_insights.json`
- ✅ Take 2-3 minutes (with 2-second delays between commits)
- ✅ Prevent rate limit errors when posting tweets

**Yo9 only need to run this once** or when you want to refresh the knowledge base with new commits.

### 7. Test the Bot

Before running it live, test tweet generation:

```bash
python bot.py test
```

This will generate a tweet from your first commit without posting it (uses cached knowledge base).

### 10. Post Your First Tweet

```bash
python bot.py post-now
```

Your first tweet is now live! 🎉

## 🎮 Usage

### Available Commands

```bash
# Build knowledge base (run once, first time only)
python bot.py analyze

# Test tweet generation (without posting)
python bot.py test

# Post a tweet immediately
python bot.py post-now

# View codebase statistics
python bot.py overview

# List all commits chronologically
python bot.py commits

# Run bot with daily scheduler
python bot.py
```

### Run the Bot (Scheduled Mode)

Start the bot to post tweets daily at the scheduled time:

```bash
python bot.py
```

The bot will run continuously and post once per day at the time specified in your `.env` file.

### Post a Tweet Immediately

To post a tweet right now:

```bash
python bot.py post-now
```

### View Codebase Overview

See statistics about your codebase:

```bash
python bot.py overview
```

### Test Tweet Generation

Generate a test tweet without posting:

```bash   # Main bot orchestrator
├── universal_code_analyzer.py # Multi-language code analysis
├── llm_tweet_generator.py     # AI-powered tweet generation
├── requirements.txt           # Python dependencies
├── .env                       # Your API credentials (create from .env.example)
├── .env.example              # Example configuration template
├── .gitignore                # Git ignore rules
├── commit_insights.json      # Cached LLM analysis (auto-generated)
├── posted_tweets.json        # Posted tweet tracker (auto-generated)
├── bot.log                   # Bot execution logs (auto-generated)
├── code/                     # Your project folder to analyze
│   └── (your project files)
└── README.md                 # Documentationdependencies
├── .env                    # Configuration (create from .env.example)
├── .eHow It Generates Tweets

The bot creates engaging tweets by:

1. **Analyzing Commits** - Extracts what was built, tech used, and impact
2. **LLM Deep Analysis** - Uses Groq's Llama 3.3 70B to understand code context
3. **Caching Insights** - Stores analysis once to avoid rate limits
4. **Chronological Order** - Tweets follow your actual development timeline
5. **Smart Generation** - Creates human-like tweets with hashtags and links

### Tweet Structure

```
[Project Name]: [Hook/Opening]
[What was built] [Technical detail]
[Impact/Why it matters]
#BuildInPublic #RelevantTech
[GitHub Link]
```

## 🔧 Customization

### Change Posting Schedule

Edit the `TWEET_TIME` in your `.env` file:

```env
TWEET_TIME=14:30  # Posts at 2:30 PM daily
```

### Refresh Knowledge Base

When you have new commits:

```bash
python bot.py analyze  # Re-analyze with new commits`TWEET_TIME` in your `.env` file to change when tweets are posted.

### Adjust Tweet Generation Strategy

Modify the probabilities in `bot.py` `generate_tweet()` method:

```python
# Strategy 1: File analysis (70% of the time)
if random.random() < 0.7:
    # ...
```

## 📊 Tracking Posted Tweets

All posted tweets are saved in `posted_tweets.json` with:
- Tweet text
- Metadata (type, file, feature, etc.)
- Timestamp

This prevents duplicate posts and helps you track your progress.

## 🐛 Troubleshooting

### "Authentication Error"
- Double-check your API credentials in `.env`
- Ensure your Twitter app has "Read and Write" permissions
- Regenerate tokens if needed

### "No Python files found"
- Make sure you have `.py` files in the `code/` folder
- Check that the folder path is correct

### "Could not generate unique tweet"
- You may have posted about all available content
- Add more code to the `code/` folder
- Clear `posted_tweets.json` to reset (warning: will allow reposts)

### Bot not posting at scheduled time
- Ensure the bot is running continuously
- Check that `TWEET_TIME` is in correct 24-hour format (HH:MM)
- Review `bot.log` for error messages

## 🚦 Running in Production

For continuous operation, consider:

1. **Using a Process Manager** (e.g., systemd, pm2, supervisor)
2. **Hosting on a VPS** (e.g., DigitalOcean, Linode, AWS EC2)
3. **Using Docker** for containerized deployment
4. **Setting up monitoring** to ensure the bot stays running

Example with systemd on Linux:

```bash
# Create service file: /etc/systemd/system/twitter-bot.service
[Unit]
Description=Twitter Build in Public Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/twitter-bot
ExecStart=/usr/bin/python3 /path/to/twitter-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## ⚠️ Important Notes

- **Rate Limits**: Twitter has rate limits. The bot uses `wait_on_rate_limit=True` to handle this automatically.
- **API Costs**: Twitter API v2 Free tier allows 1,500 tweets per month (about 50 per day).
- **Content Policy**: Ensure your tweets follow [Twitter's Automation Rules](https://help.twitter.com/en/rules-and-policies/twitter-automation).
- **Privacy**: Don't commit your `.env` file with real credentials to version control!

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this bot! Some ideas:
- Support for other programming languages
- Integration with other platforms (LinkedIn, Mastodon)
- More sophisticated tweet templates
- AI-powered tweet generation
- Analytics dashboard

## 💡 Tips for Building in Public

1. **Be Authentic** - Share real progress, challenges, and wins
2. **Engage** - Reply to comments and join conversations
3. **Be Consistent** - Daily posts build momentum
4. **Add Value** - Share insights that help others
5. **Use Hashtags** - #BuildInPublic, #100DaysOfCode, #IndieDev

---

**Happy Building! 🚀**

If you find this bot useful, give it a star ⭐ and share it with other developers!
