<div align="center">

# DevEcho

### *Your code deserves an audience. Automate the storytelling.*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/badge/Twitter-Bot-1DA1F2?logo=twitter)](https://twitter.com)
[![Made with Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com)
[![Build in Public](https://img.shields.io/badge/Build-in%20Public-success)](https://twitter.com/search?q=%23BuildInPublic)

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

---

</div>

**DevEcho** is an AI-powered Twitter bot that transforms your Git commits into engaging social media content. Built for developers who want to #BuildInPublic without the manual overhead.

> **📁 How it works:** Place your project in the `code/` folder → DevEcho reads your Git history → AI generates tweets → Posts daily automatically

```bash
# One command to rule them all
python bot.py analyze && python bot.py post-now
```

**Stop manually tweeting. Start building.**

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- **Multi-Language Support** - Java, Python, JS, TS, Go, Rust, C++
- **AI-Powered** - Groq's Llama 3.3 70B for natural language
- **Zero Rate Limits** - Smart caching system
- **Chronological Order** - Follows your actual dev timeline
- **Daily Automation** - Set it and forget it

</td>
<td width="50%">

### 🚀 Smart Features
- **One-Time Analysis** - Analyze once, tweet forever
- **Advanced Duplicate Prevention** - Tracks commit hashes & semantic similarity (65% threshold)
- **Smart Commit Scoring** - Prioritizes impactful commits (features > docs)
- **Quality Control** - Evaluates tweets with 0.6+ quality threshold & auto-retry
- **Natural Language** - No robotic tweets
- **Project Branding** - Auto-includes name & GitHub link
- **Character Optimized** - Perfect for Twitter free tier

</td>
</tr>
</table>

---

## 🎯 How It Works

**1.** Analyze your commits once → **2.** AI extracts insights → **3.** Smart scoring & quality control → **4.** Tweet daily on autopilot

<div align="center">

| Step | What Happens |
|------|-------------|
| 📁 | Copy your project to `code/` folder |
| 🔍 | DevEcho reads Git commit history |
| 🤖 | AI analyzes what you built |
| 🎯 | Scores commits by impact (features, performance, etc.) |
| 💾 | Insights cached locally |
| ✅ | Quality checks + duplicate detection |
| 🐦 | Tweets posted daily (never repeats commits!) |

</div>

---

## 🎨 Example Tweets

<table>
<tr>
<td width="50%">

**Before DevEcho:**
```
Spent all day coding... 
*Forgets to tweet*
*Project dies in silence*
```

</td>
<td width="50%">

**After DevEcho:**
```
Eventara: Just shipped Kafka 
event streaming with Docker 
Compose. Real-time data flow 
now live. #BuildInPublic
github.com/user/eventara
```

</td>
</tr>
</table>

---

## 📋 Prerequisites

<div align="center">

| Requirement | Status | Get It |
|------------|--------|--------|
| Python 3.8+ | 🐍 | [Download](https://python.org) |
| Twitter API | 🐦 | [Get Keys](https://developer.twitter.com) |
| Groq API (Free) | 🤖 | [Sign Up](https://console.groq.com) |
| Git Repository | 📁 | Your project |

</div>

---

## 🚀 Quick Start

### 1. Clone DevEcho

```bash
git clone https://github.com/YOUR_USERNAME/devecho.git
cd devecho
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

### 5. Configure Environment Variables

Copy the example environment file and add your credentials:

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

### 6. Add Your Code

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

**Important:** The bot analyzes **Git commit history**, so make sure your project is a Git repository.

### 7. Build Knowledge Base (IMPORTANT - First Time Only)

Before posting tweets, analyze your codebase once to avoid rate limits:

```bash
python bot.py analyze
```

This command will:
- ✅ Analyze all commits using LLM for rich insights
- ✅ Cache everything in `commit_insights.json`
- ✅ Take 2-3 minutes (with 2-second delays between commits)
- ✅ Prevent rate limit errors when posting tweets

**You only need to run this once** or when you want to refresh the knowledge base with new commits.

### 8. Test the Bot

Before running it live, test tweet generation:

```bash
python bot.py test
```

This will generate a tweet from your first commit without posting it (uses cached knowledge base).

### 9. Post Your First Tweet

```bash
python bot.py post-now
```

Your first tweet is now live! 🎉

---

## 🖱️ One-Click Quick Actions (macOS)

For ultimate convenience, use these clickable files - **no terminal required!**

### 📤 Post Tweet Instantly
**Double-click:** `post-tweet.command`
- Generates and posts a tweet immediately
- Shows progress in a terminal window
- Auto-activates virtual environment
- Press Enter to close when done

### 🧪 Test Tweet Generation
**Double-click:** `test-tweet.command`
- Generates a preview tweet without posting
- Perfect for checking quality before going live
- Shows the tweet in terminal
- Press Enter to close when done

**⚠️ First-time setup (macOS only):**
1. Right-click the `.command` file
2. Select "Open" 
3. Click "Open" in the security dialog
4. After this, double-clicking will work normally

**💡 Pro Tip:** Add these to your Dock for instant access!

---

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
### What You'll See in Logs

After the improvements, you'll see detailed information:

```bash
# Before (Old System):
Generating tweet for commit: Initial commit...

# After (New System with Smart Features):
Loaded 7 previously tweeted commits  # Tracking works!
Trying commit (score: 2.10): Implemented EventResponse dto  # Smart scoring!
LLM generated tweet (quality: 0.85): Eventara: Built robust DTOs...  # Quality control!
```

**Key Metrics:**
- **Commit Scores**: 2.0+ (Excellent) → 1.5-2.0 (Good) → 1.0-1.5 (Decent) → 0.5-1.0 (Low)
- **Tweet Quality**: 0.8-1.0 (Excellent) → 0.6-0.8 (Good) → Below 0.6 (Auto-retry)

---

## 🎯 Smart Features Explained

### 🚫 Advanced Duplicate Prevention
- **Commit Hash Tracking**: Never tweets the same commit twice
- **Semantic Similarity**: Detects similar tweets with 65% threshold
- **Persistent Memory**: Remembers all previous tweets across restarts

### 🧠 Intelligent Commit Scoring
Commits are automatically scored based on impact:
- **+1.0** - Has LLM insights
- **+0.4** - Feature implementation
- **+0.3** - Performance optimization
- **+0.2** - Bug fix or refactor
- **-0.3** - Documentation (de-prioritized)
- **+0.3** - Optimal file count (2-10 files)
- **+0.2** - Multiple technologies used
- **-0.3** - Generic commit messages ("update", "wip", "merge")

**Result**: The bot tweets your most impactful work first!

### ✅ Quality Control System
Every generated tweet is scored on:
- ✓ Project name included
- ✓ #BuildInPublic hashtag present
- ✓ GitHub link added
- ✓ Technical specifics (bullets, numbers)
- ✓ Minimum 100 characters
- ✓ Not too generic

**Minimum Score**: 0.6/1.0 (auto-retries up to 3 times if below)

---

## 🎮 Usage

### Available Commands

```bash
# Build knowledge base (run once, first time only)
python bot.py analyze

# Test tweet generation (without posting)
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

```bash
python bot.py test
```

---

## 📁 Project Structure

```
devecho/
├── bot.py                     # Main bot orchestrator
├── universal_code_analyzer.py # Multi-language code analysis
├── llm_tweet_generator.py     # AI-powered tweet generation
├── post-tweet.command         # 🖱️ One-click tweet poster (macOS)
├── test-tweet.command         # 🧪 One-click tweet tester (macOS)
├── requirements.txt           # Python dependencies
├── .env                       # Your API credentials (create from .env.example)
├── .env.example              # Example configuration template
├── .gitignore                # Git ignore rules
├── commit_insights.json      # Cached LLM analysis (auto-generated)
├── posted_tweets.json        # Posted tweet tracker (auto-generated)
├── bot.log                   # Bot execution logs (auto-generated)
├── code/                     # Your project folder to analyze
│   └── (your project files)
└── README.md                 # Documentation
```

---

## 🧠 How It Generates Tweets

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

---

## 🔧 Customization

### Change Posting Schedule

Edit the `TWEET_TIME` in your `.env` file:

```env
TWEET_TIME=14:30  # Posts at 2:30 PM daily
```

### Refresh Knowledge Base

When you have new commits:

```bash
python bot.py analyze  # Re-analyze with new commits
```

### Adjust Tweet Generation Strategy

Modify the `TWEET_TIME` in your `.env` file to change when tweets are posted.

You can also adjust tweet generation strategy by modifying the probabilities in `bot.py` `generate_tweet()` method:

```python
# Strategy 1: File analysis (70% of the time)
if random.random() < 0.7:
    # ...
```

---

## 📊 Tracking Posted Tweets

All posted tweets are saved in `posted_tweets.json` with:
- Tweet text
- Metadata (type, file, feature, etc.)
- Timestamp

This prevents duplicate posts and helps you track your progress.

---

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

---

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

---

## ⚠️ Important Notes

- **Rate Limits**: Twitter has rate limits. The bot uses `wait_on_rate_limit=True` to handle this automatically.
- **API Costs**: Twitter API v2 Free tier allows 1,500 tweets per month (about 50 per day).
- **Content Policy**: Ensure your tweets follow [Twitter's Automation Rules](https://help.twitter.com/en/rules-and-policies/twitter-automation).
- **Privacy**: Don't commit your `.env` file with real credentials to version control!

---

## 📝 License

This project is open source and available for personal and commercial use.

---

## 🤝 Contributing

Feel free to fork, modify, and improve this bot! Some ideas:
- Support for other programming languages
- Integration with other platforms (LinkedIn, Mastodon)
- More sophisticated tweet templates
- AI-powered tweet generation
- Analytics dashboard

---

## 💡 Tips for Building in Public

1. **Be Authentic** - Share real progress, challenges, and wins
2. **Engage** - Reply to comments and join conversations
3. **Be Consistent** - Daily posts build momentum
4. **Add Value** - Share insights that help others
5. **Use Hashtags** - #BuildInPublic, #100DaysOfCode, #IndieDev

---

**Happy Building! 🚀**

If you find this bot useful, give it a star ⭐ and share it with other developers!
