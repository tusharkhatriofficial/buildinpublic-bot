"""
LLM-Powered Tweet Generator using Groq
Generates engaging, human-like tweets from code analysis
"""
import os
import json
from typing import Dict, List, Any, Optional
from groq import Groq
import logging

logger = logging.getLogger(__name__)


class LLMTweetGenerator:
    def __init__(self, api_key: str, posted_tweets_file: str = 'posted_tweets.json', 
                 project_name: str = None, github_url: str = None):
        self.client = Groq(api_key=api_key)
        self.posted_tweets_file = posted_tweets_file
        self.posted_tweets = self._load_posted_tweets()
        self.max_length = 280
        self.project_name = project_name
        self.github_url = github_url
        # Twitter shortens all links to 23 characters
        self.twitter_link_length = 23
        
    def _load_posted_tweets(self) -> List[Dict[str, Any]]:
        """Load previously posted tweets from JSON file"""
        if os.path.exists(self.posted_tweets_file):
            try:
                with open(self.posted_tweets_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_posted_tweet(self, tweet: str, metadata: Dict[str, Any]):
        """Save a posted tweet to prevent duplicates"""
        self.posted_tweets.append({
            'tweet': tweet,
            'metadata': metadata,
            'timestamp': None
        })
        with open(self.posted_tweets_file, 'w') as f:
            json.dump(self.posted_tweets, f, indent=2)
    
    def _is_duplicate(self, tweet: str) -> bool:
        """Check if a similar tweet has been posted before"""
        for posted in self.posted_tweets:
            if posted['tweet'] == tweet:
                return True
            if self._similarity(tweet, posted['tweet']) > 0.75:
                return True
        return False
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Simple similarity check between two strings"""
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())
        if not words1 or not words2:
            return 0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)
    
    def _create_prompt(self, insights: Dict[str, Any], tweet_type: str) -> str:
        """Create a prompt for the LLM based on code insights"""
        
        project_context = ""
        if self.project_name:
            project_context = f"\nProject name: {self.project_name}"
        if self.github_url:
            project_context += f"\nGitHub URL: {self.github_url}"
        
        base_context = f"""You are a software developer building in public on Twitter. Generate an engaging, authentic tweet about your coding progress.{project_context}

Style guidelines:
- Start with the project name if provided (e.g., "Eventara:")
- Write like a real human developer, not marketing copy
- Be specific and technical when relevant
- Show genuine progress and insights
- Use natural language, no emojis
- Must include #BuildInPublic hashtag
- Add 1-2 relevant technical hashtags based on the tech used
- Include GitHub link at the end if provided
- Maximum 280 characters (note: Twitter shortens links to 23 chars)
- Use line breaks for readability
- Be concise but impactful

Example of good tweet style:
"Eventara: Building open-source observability

Just shipped real-time analytics
- Kafka-powered event streaming
- Self-hosted, deploy in 5 mins

https://github.com/user/eventara

#BuildInPublic #OpenSource #Kafka"
"""
        
        if tweet_type == 'commit':
            tech = ' '.join(insights.get('tech_stack', []))
            return f"""{base_context}

Commit details:
- What changed: {insights['message']}
- Category: {', '.join(insights.get('categories', []))}
- Tech used: {tech if tech else 'Various technologies'}
- Files changed: {insights['files_changed']}
- Date: {insights['date']}

Generate a tweet that explains what was built/fixed/improved in this commit. Make it engaging and show the technical work. Focus on the achievement or insight. Include project name at start and GitHub link at end."""

        elif tweet_type == 'milestone':
            return f"""{base_context}

Project stats:
- Languages: {', '.join(insights['languages'])}
- Frameworks: {', '.join(insights['frameworks'])}
- Total files: {insights['total_files']}
- Is Git Repo: {insights['is_git_repo']}

Generate a tweet celebrating project progress or technical achievement. Show scale and complexity. Include project name at start and GitHub link at end."""

        elif tweet_type == 'project_intro':
            return f"""{base_context}

Project information:
- README excerpt: {insights.get('readme', 'Building an open-source project')[:200]}
- Tech stack: {', '.join(insights.get('tech_stack', []))}
- Languages: {', '.join(insights.get('languages', []))}

Generate a compelling tweet introducing this project. Highlight what it does and why it matters. Include project name at start and GitHub link at end."""

        return base_context

    def generate_from_commit(self, commit_info: Dict) -> Optional[tuple]:
        """Generate tweet about a git commit"""
        prompt = self._create_prompt(commit_info, 'commit')
        return self._generate_with_llm(prompt, {'type': 'commit', 'hash': commit_info['hash'], 'message': commit_info['message']})
    
    def generate_milestone(self, overview: Dict[str, Any]) -> Optional[tuple]:
        """Generate milestone tweet"""
        prompt = self._create_prompt(overview, 'milestone')
        return self._generate_with_llm(prompt, {'type': 'milestone', 'stats': overview})
    
    def generate_project_intro(self, project_info: Dict[str, Any]) -> Optional[tuple]:
        """Generate project introduction tweet"""
        prompt = self._create_prompt(project_info, 'project_intro')
        return self._generate_with_llm(prompt, {'type': 'project_intro'})
    
    def _generate_with_llm(self, prompt: str, metadata: Dict) -> Optional[tuple]:
        """Generate tweet using Groq LLM"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a software developer who tweets about your coding journey. Write authentic, engaging tweets that show real progress and technical insights. No emojis. Always include #BuildInPublic. Start with project name and end with GitHub link when provided."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=200,
                top_p=0.9
            )
            
            tweet = response.choices[0].message.content.strip()
            
            # Remove quotes if LLM wrapped the tweet
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            if tweet.startswith("'") and tweet.endswith("'"):
                tweet = tweet[1:-1]
            
            # Ensure GitHub link is included if available
            if self.github_url and self.github_url not in tweet:
                # Calculate available space (280 - current length - link length - newlines)
                available_space = self.max_length - len(tweet) - self.twitter_link_length - 2
                if available_space > 0:
                    tweet = f"{tweet}\n\n{self.github_url}"
            
            # Ensure it's within character limit
            # Note: Twitter counts links as 23 chars regardless of actual length
            tweet_length = len(tweet)
            if self.github_url and self.github_url in tweet:
                # Adjust for Twitter's link shortening
                tweet_length = tweet_length - len(self.github_url) + self.twitter_link_length
            
            if tweet_length > self.max_length:
                # Need to truncate
                if self.github_url and self.github_url in tweet:
                    # Remove link temporarily, truncate text, add link back
                    tweet_without_link = tweet.replace(f"\n\n{self.github_url}", "")
                    max_text_length = self.max_length - self.twitter_link_length - 2 - 3  # -3 for "..."
                    tweet = f"{tweet_without_link[:max_text_length]}...\n\n{self.github_url}"
                else:
                    tweet = tweet[:self.max_length - 3] + "..."
            
            # Check for duplicates
            if self._is_duplicate(tweet):
                logger.info("Generated tweet is too similar to previous tweets")
                return None, None
            
            logger.info(f"LLM generated tweet: {tweet}")
            return tweet, metadata
            
        except Exception as e:
            logger.error(f"Error generating tweet with LLM: {e}")
            return None, None
    
    def mark_as_posted(self, tweet: str, metadata: Dict[str, Any], timestamp: str):
        """Mark a tweet as posted with timestamp"""
        self._save_posted_tweet(tweet, metadata)
        if self.posted_tweets:
            self.posted_tweets[-1]['timestamp'] = timestamp
            with open(self.posted_tweets_file, 'w') as f:
                json.dump(self.posted_tweets, f, indent=2)
