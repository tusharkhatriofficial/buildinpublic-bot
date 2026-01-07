"""
DevEcho - Twitter Bot
Automatically posts daily tweets about your codebase
Transform your Git commits into engaging social media content
"""
import os
import tweepy
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from universal_code_analyzer import UniversalCodeAnalyzer
from llm_tweet_generator import LLMTweetGenerator
import random
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TwitterBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Twitter API
        self.api = self._setup_twitter_api()
        
        # Initialize components
        self.code_folder = os.path.join(os.path.dirname(__file__), 'code')
        self.analyzer = UniversalCodeAnalyzer(self.code_folder)
        
        # Get project info
        project_info = self.analyzer.get_project_info()
        logger.info(f"Project: {project_info['name']}, GitHub: {project_info['github_url']}")
        
        # Use LLM-powered tweet generator
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key or groq_api_key == 'your_groq_api_key_here':
            logger.warning("GROQ_API_KEY not set in .env file. Will try to use it anyway.")
        
        self.tweet_generator = LLMTweetGenerator(
            groq_api_key, 
            project_name=project_info['name'],
            github_url=project_info['github_url']
        )
        
        # Track which commits have been tweeted
        self.commit_index = 0
        self.all_insights = []
        self.used_commit_hashes = self._load_used_commits()
        
    def _load_used_commits(self):
        """Load commit hashes that have already been tweeted"""
        used_hashes = set()
        try:
            import json
            if os.path.exists('posted_tweets.json'):
                with open('posted_tweets.json', 'r') as f:
                    posted = json.load(f)
                    for tweet in posted:
                        if 'metadata' in tweet and 'hash' in tweet['metadata']:
                            used_hashes.add(tweet['metadata']['hash'])
            logger.info(f"Loaded {len(used_hashes)} previously tweeted commits")
        except Exception as e:
            logger.warning(f"Could not load used commits: {e}")
        return used_hashes
    
    def _score_commit(self, commit: dict) -> float:
        """Score a commit based on its potential for interesting tweets"""
        score = 1.0
        
        # Already used? Score 0
        if commit['hash'] in self.used_commit_hashes:
            return 0.0
        
        # Prioritize commits with LLM insights
        if commit.get('llm_insights'):
            score += 1.0
        
        # File changes (sweet spot is 2-10 files)
        files = commit['files_changed']
        if files < 1:
            score -= 0.5
        elif 2 <= files <= 10:
            score += 0.3
        elif files > 20:
            score -= 0.2  # Too big, might be messy
        
        # Category bonuses
        categories = commit.get('categories', [])
        if 'feature' in categories:
            score += 0.4
        if 'performance' in categories:
            score += 0.3
        if 'bug fix' in categories:
            score += 0.2
        if 'documentation' in categories:
            score -= 0.3  # De-prioritize docs
        if 'general' in categories and len(categories) == 1:
            score -= 0.2  # Generic commits less interesting
        
        # Tech stack diversity (more tech = more interesting)
        tech_count = len(commit.get('tech_stack', []))
        if tech_count >= 2:
            score += 0.2
        
        # Message quality (avoid generic messages)
        message = commit['message'].lower()
        generic_terms = ['update', 'fix typo', 'merge', 'wip', 'temp']
        if any(term in message for term in generic_terms):
            score -= 0.3
        
        # Specific implementation terms (good signals)
        good_terms = ['implement', 'add', 'create', 'build', 'optimize', 'refactor']
        if any(term in message for term in good_terms):
            score += 0.2
        
        return max(0.0, score)
        
    def _setup_twitter_api(self):
        """Setup Twitter API authentication"""
        try:
            # Twitter API v2 authentication
            client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            logger.info("Twitter API initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            raise
    
    def generate_tweet(self):
        """Generate a new tweet from code analysis"""
        try:
            # Get chronological insights if not already loaded
            if not self.all_insights:
                # Try to load from cache first
                cached = self.analyzer.load_from_cache()
                if cached:
                    self.all_insights = cached
                else:
                    logger.warning("⚠️  No knowledge base found. Run 'python bot.py analyze' first to avoid rate limits.")
                    print("⚠️  Using basic analysis without LLM insights (may be less engaging)")
                    print("   Run 'python bot.py analyze' first to build knowledge base with LLM.\n")
                    self.all_insights = self.analyzer.get_chronological_insights()
                logger.info(f"Loaded {len(self.all_insights)} commits from git history")
            
            if not self.all_insights:
                logger.warning("No git commits found, trying project overview")
                overview = self.analyzer.get_project_overview()
                if overview['total_files'] > 0:
                    tweet, metadata = self.tweet_generator.generate_milestone(overview)
                    if tweet:
                        return tweet, metadata
                return None, None
            
            # Score all unused commits and sort by score
            scored_commits = []
            for commit in self.all_insights:
                score = self._score_commit(commit)
                if score > 0:
                    scored_commits.append((score, commit))
            
            # Sort by score (highest first)
            scored_commits.sort(reverse=True, key=lambda x: x[0])
            
            if not scored_commits:
                logger.info("All commits have been used, generating milestone tweet")
                overview = self.analyzer.get_project_overview()
                tweet, metadata = self.tweet_generator.generate_milestone(overview)
                if tweet:
                    # Reset used commits to start over
                    self.used_commit_hashes.clear()
                    return tweet, metadata
                return None, None
            
            # Try top-scored commits
            max_attempts = min(len(scored_commits), 10)
            
            for i in range(max_attempts):
                score, commit_insight = scored_commits[i]
                
                logger.info(f"Trying commit (score: {score:.2f}): {commit_insight['message'][:50]}")
                tweet, metadata = self.tweet_generator.generate_from_commit(commit_insight)
                
                if tweet:
                    logger.info(f"Generated tweet from commit {commit_insight['hash']}")
                    # Mark as used
                    self.used_commit_hashes.add(commit_insight['hash'])
                    return tweet, metadata
            
            # If we couldn't generate from any commit, try milestone
            logger.info("Could not generate from commits, trying milestone")
            overview = self.analyzer.get_project_overview()
            tweet, metadata = self.tweet_generator.generate_milestone(overview)
            if tweet:
                return tweet, metadata
            
            logger.warning("Could not generate tweet")
            return None, None
            
        except Exception as e:
            logger.error(f"Error generating tweet: {e}", exc_info=True)
            return None, None
    
    def post_tweet(self, tweet_text: str, metadata: dict):
        """Post a tweet to Twitter"""
        try:
            response = self.api.create_tweet(text=tweet_text)
            timestamp = datetime.now().isoformat()
            
            self.tweet_generator.mark_as_posted(tweet_text, metadata, timestamp)
            
            logger.info(f"Successfully posted tweet: {tweet_text}")
            logger.info(f"Tweet ID: {response.data['id']}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False
    
    def daily_task(self):
        """Daily task to generate and post a tweet"""
        logger.info("Starting daily tweet task...")
        
        tweet, metadata = self.generate_tweet()
        
        if tweet:
            success = self.post_tweet(tweet, metadata)
            if success:
                logger.info("Daily task completed successfully")
            else:
                logger.error("Daily task failed - could not post tweet")
        else:
            logger.error("Daily task failed - could not generate tweet")
    
    def test_tweet(self):
        """Test function to generate a tweet without posting"""
        logger.info("Testing tweet generation...")
        tweet, metadata = self.generate_tweet()
        
        if tweet:
            logger.info(f"Generated test tweet: {tweet}")
            logger.info(f"Metadata: {metadata}")
            return tweet
        else:
            logger.warning("Could not generate test tweet")
            return None
    
    def run(self):
        """Run the bot with scheduling"""
        logger.info("Twitter bot started")
        logger.info(f"Analyzing code from: {self.code_folder}")
        
        # Get schedule time from environment
        tweet_time = os.getenv('TWEET_TIME', '10:00')
        
        # Schedule daily tweet
        schedule.every().day.at(tweet_time).do(self.daily_task)
        
        logger.info(f"Scheduled daily tweets at {tweet_time}")
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        # Run immediately on first start (optional)
        # self.daily_task()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main entry point"""
    import sys
    
    bot = TwitterBot()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'analyze':
            # Build knowledge base once
            print("🚀 Building knowledge base from codebase...\n")
            print("⏱️  This will analyze all commits with LLM once to avoid future rate limits.")
            print("   Please wait, this may take a few minutes...\n")
            success = bot.analyzer.build_knowledge_base()
            if not success:
                sys.exit(1)
        
        elif command == 'test':
            # Test mode - generate tweet without posting
            print("Testing tweet generation...")
            tweet = bot.test_tweet()
            if tweet:
                print(f"\n✅ Generated tweet:\n{tweet}\n")
            else:
                print("❌ Failed to generate tweet")
        
        elif command == 'post-now':
            # Post immediately
            print("Posting tweet now...")
            bot.daily_task()
        
        elif command == 'overview':
            # Show codebase overview
            overview = bot.analyzer.get_project_overview()
            print("\n📊 Codebase Overview:")
            print(f"  Total files: {overview['total_files']}")
            print(f"  Languages: {', '.join(overview['languages'])}")
            print(f"  Frameworks: {', '.join(overview['frameworks'])}")
            print(f"  Is Git repo: {overview['is_git_repo']}")
            
            if overview['is_git_repo']:
                commits = bot.analyzer.get_chronological_insights()
                print(f"\n  Total commits: {len(commits)}")
                if commits:
                    print(f"  First commit: {commits[0]['message'][:50]}... ({commits[0]['date']})")
                    print(f"  Latest commit: {commits[-1]['message'][:50]}... ({commits[-1]['date']})")
        
        elif command == 'commits':
            # Show commit history
            commits = bot.analyzer.get_chronological_insights()
            print(f"\n📝 Found {len(commits)} commits (showing first 10):\n")
            for i, commit in enumerate(commits[:10], 1):
                print(f"{i}. [{commit['hash']}] {commit['date']}")
                print(f"   {commit['message']}")
                print(f"   Tech: {', '.join(commit['tech_stack'][:3])}")
                print(f"   Files changed: {commit['files_changed']}")
                print()
        
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  analyze   - Build knowledge base (run once to avoid rate limits)")
            print("  test      - Generate and display a test tweet")
            print("  post-now  - Generate and post a tweet immediately")
            print("  overview  - Show codebase analysis overview")
            print("  commits   - List all commits in chronological order")
    
    else:
        # Normal mode - run with scheduler
        try:
            bot.run()
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Bot crashed: {e}")


if __name__ == "__main__":
    main()
