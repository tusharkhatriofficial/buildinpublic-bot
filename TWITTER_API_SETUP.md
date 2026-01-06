# Twitter API Setup Guide

Complete step-by-step guide to get your Twitter API credentials for the bot.

## Prerequisites
- Twitter account (the account the bot will tweet from)
- Email address
- Phone number (for verification)

## Step-by-Step Instructions

### 1. Apply for Developer Account

1. **Go to Twitter Developer Portal**
   - Visit: https://developer.twitter.com/en/portal/dashboard
   - Click **"Sign in"** with your Twitter account

2. **Apply for Developer Access**
   - Click **"Apply for a developer account"** if prompted
   - Choose **"Hobbyist"** → **"Making a bot"**
   - Fill out the application form:
     - Country: Your country
     - Use case: "Creating an automated bot to tweet about my open-source development progress"
     - Will you make Twitter content available to government entities? **No**
   - Agree to terms and submit
   - **Usually approved instantly!**

### 2. Create Project and App

1. **Create Project**
   - Click **"+ Create Project"**
   - Project name: `build-in-public-bot` (or your choice)
   - Use case: **"Making a bot"**
   - Project description: "Automated bot to share development progress"
   - Click **"Next"**

2. **Create App**
   - App name: `my-twitter-bot` (must be unique across Twitter)
   - Click **"Complete"**
   - **SAVE YOUR API KEY & SECRET NOW!** (You'll need them)

### 3. Configure App Permissions (CRITICAL!)

1. **Go to App Settings**
   - In your project, click on your app name
   - Go to **"Settings"** tab

2. **Set Up User Authentication**
   - Scroll to **"User authentication settings"**
   - Click **"Set up"**

3. **Configure OAuth Settings**
   - **App permissions**: 
     - ✅ Select **"Read and Write"** (NOT Read-only!)
     - This allows the bot to post tweets
   
   - **Type of App**: 
     - ✅ Select **"Web App, Automated App or Bot"**
   
   - **App info**:
     - Callback URI: `http://localhost:3000`
     - Website URL: `https://github.com/yourusername/your-repo`
   
   - Click **"Save"**

### 4. Generate All Required Keys

#### A. API Key and Secret (Consumer Keys)
1. Go to **"Keys and tokens"** tab
2. Under **"Consumer Keys"**:
   - You should already have these from step 2
   - If not, click **"Regenerate"**
3. Copy and save:
   - `API Key` → This is your `TWITTER_API_KEY`
   - `API Key Secret` → This is your `TWITTER_API_SECRET`

#### B. Bearer Token
1. Still in **"Keys and tokens"** tab
2. Under **"Bearer Token"**:
   - Click **"Regenerate"**
3. Copy and save:
   - `Bearer Token` → This is your `TWITTER_BEARER_TOKEN`

#### C. Access Token and Secret (IMPORTANT!)
1. Still in **"Keys and tokens"** tab
2. Under **"Authentication Tokens"**:
   - **FIRST**: Make sure you completed step 3 (Read and Write permissions)
   - Click **"Generate"** or **"Regenerate"**
   - ⚠️ If you see "Read-only", STOP! Go back to step 3
3. Copy and save:
   - `Access Token` → This is your `TWITTER_ACCESS_TOKEN`
   - `Access Token Secret` → This is your `TWITTER_ACCESS_TOKEN_SECRET`

### 5. Verify Your Setup

Check that everything is correct:

✅ **App Permissions**: Should show "Read and Write"
✅ **Access Token**: Should show "Read and Write" (NOT "Read-only")
✅ **All 5 credentials saved**:
   - API Key
   - API Secret
   - Bearer Token
   - Access Token
   - Access Token Secret

### 6. Add to Your Bot

1. **Copy .env.example to .env**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file and paste your credentials**
   ```env
   TWITTER_API_KEY=your_actual_api_key_here
   TWITTER_API_SECRET=your_actual_api_secret_here
   TWITTER_ACCESS_TOKEN=your_actual_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret_here
   TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
   ```

3. **Never commit .env to Git!** (Already in .gitignore)

## Common Issues and Solutions

### Issue: 403 Forbidden when posting tweets
**Solution**: Access Token has Read-only permissions
1. Go to User authentication settings
2. Change to "Read and Write"
3. **Delete** existing Access Token
4. **Generate new** Access Token and Secret
5. Update .env file with new tokens

### Issue: "Read-only" shown on Access Token
**Solution**: You generated tokens before setting Read and Write permissions
1. Set permissions to Read and Write first
2. Then regenerate Access Token and Secret

### Issue: App name already taken
**Solution**: App names must be unique across all of Twitter
- Try: `my-bot-2026`, `username-twitter-bot`, etc.
- Add random numbers if needed

### Issue: Can't find "User authentication settings"
**Solution**: Make sure you're in the correct location
1. Go to Developer Portal
2. Select your Project
3. Click on your App name (not Project name)
4. Click "Settings" tab
5. Scroll down to find it

## Rate Limits (Free Tier)

- **Posts**: 50 tweets per day
- **API calls**: 500,000 requests per month
- **Should be plenty** for daily posting bot!

## Security Best Practices

1. ✅ Keep all keys in .env file
2. ✅ Never commit .env to Git
3. ✅ Never share keys publicly
4. ✅ Regenerate keys if accidentally exposed
5. ✅ Use different apps for different bots

## Need Help?

- Twitter API Docs: https://developer.twitter.com/en/docs
- This bot's issues: [Your GitHub repo]/issues

---

**Pro Tip**: Take screenshots while setting up in case you need to reference later!
