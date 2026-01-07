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
    
    def _is_duplicate(self, tweet: str, commit_hash: str = None) -> bool:
        """Check if a similar tweet has been posted before"""
        # Check exact match
        for posted in self.posted_tweets:
            if posted['tweet'] == tweet:
                return True
            
            # Check if same commit was already tweeted
            if commit_hash and posted.get('metadata', {}).get('hash') == commit_hash:
                logger.info(f"Skipping duplicate commit: {commit_hash}")
                return True
            
            # Check semantic similarity (lower threshold for better detection)
            if self._similarity(tweet, posted['tweet']) > 0.65:
                logger.info(f"Skipping similar tweet (similarity > 0.65)")
                return True
        return False
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Advanced similarity check using multiple metrics"""
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())
        if not words1 or not words2:
            return 0
        
        # Jaccard similarity (word overlap)
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        jaccard = len(intersection) / len(union)
        
        # Simple Levenshtein-like similarity (character level)
        # Check if one string is a substring of another
        str1_lower = str1.lower()
        str2_lower = str2.lower()
        if str1_lower in str2_lower or str2_lower in str1_lower:
            return 0.9
        
        # Check for very similar structure (same length, many same chars)
        if abs(len(str1) - len(str2)) < 10:
            same_chars = sum(1 for a, b in zip(str1_lower, str2_lower) if a == b)
            char_similarity = same_chars / max(len(str1), len(str2))
            if char_similarity > 0.8:
                return char_similarity
        
        return jaccard
    
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
- Be specific and technical - mention actual technologies/patterns used
- Show genuine progress and IMPACT (what users/developers gain)
- Use natural language, no emojis
- Must include #BuildInPublic hashtag
- Add 1-2 relevant technical hashtags based on the tech used
- Include GitHub link at the end if provided
- Maximum 280 characters (note: Twitter shortens links to 23 chars)
- Use line breaks for readability
- Focus on WHY it matters, not just WHAT was built
- Be concise but impactful - every word counts

Examples of great tweets:

"Eventara: Building open-source observability

Just shipped real-time analytics
- Kafka-powered event streaming
- Self-hosted, deploy in 5 mins

https://github.com/user/eventara

#BuildInPublic #OpenSource #Kafka"

"Eventara: Solved a tricky race condition

Added distributed locking with Redis
- Prevents duplicate event processing
- 99.9% consistency at scale

https://github.com/user/eventara

#BuildInPublic #DistributedSystems"

"Eventara: Milestone unlocked

10K events/sec throughput
- Optimized database queries
- Added connection pooling
- 40% latency reduction

https://github.com/user/eventara

#BuildInPublic #Performance"

Key principles:
1. Lead with the achievement/insight
2. Add technical specifics
3. Show measurable impact
4. End with project link
"""
        
        if tweet_type == 'commit':
            tech = ' '.join(insights.get('tech_stack', []))
            
            # Check if we have LLM insights
            llm_insights = insights.get('llm_insights', {})
            
            if llm_insights:
                # Use rich LLM insights for better tweets
                return f"""{base_context}

Commit analysis:
- Original message: {insights['message']}
- What was built: {llm_insights.get('what_built', 'N/A')}
- Technical implementation: {llm_insights.get('technical_detail', 'N/A')}
- Real-world impact: {llm_insights.get('impact', 'N/A')}
- Hook/angle: {llm_insights.get('hook', 'N/A')}
- Technologies: {tech if tech else 'Various technologies'}
- Scale: {insights['files_changed']} files changed

Task: Generate a compelling tweet that:
1. Opens with project name and the achievement/insight
2. Explains the technical approach in 1-2 bullet points
3. Shows the impact/benefit (performance gain, new capability, problem solved)
4. Uses specific numbers/metrics when available
5. Ends with GitHub link

Make it sound like a real developer sharing progress, not a product announcement. Focus on the technical journey and lessons learned."""
            else:
                # Fallback to basic info
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
        """Generate tweet using Groq LLM with quality checks"""
        max_retries = 3
        commit_hash = metadata.get('hash')
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a software developer who tweets about your coding journey. Write authentic, engaging tweets that show real progress and technical insights. Focus on IMPACT and specific technical details. No emojis. Always include #BuildInPublic. Start with project name and end with GitHub link when provided. Be concise and punchy - every word must add value."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7 + (attempt * 0.1),  # Increase temperature on retries for variety
                    max_tokens=250,
                    top_p=0.9,
                    presence_penalty=0.6,  # Encourage diverse vocabulary
                    frequency_penalty=0.3  # Reduce repetition
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
                
                # Check for duplicates with commit hash awareness
                if self._is_duplicate(tweet, commit_hash):
                    if attempt < max_retries - 1:
                        logger.info(f"Generated tweet is duplicate, retrying (attempt {attempt + 1}/{max_retries})")
                        continue
                    else:
                        logger.info("All retry attempts produced duplicates")
                        return None, None
                
                # Quality checks
                quality_score = self._evaluate_tweet_quality(tweet)
                if quality_score < 0.6 and attempt < max_retries - 1:
                    logger.info(f"Tweet quality score {quality_score:.2f} too low, retrying...")
                    continue
                
                logger.info(f"LLM generated tweet (quality: {quality_score:.2f}): {tweet}")
                return tweet, metadata
                
            except Exception as e:
                logger.error(f"Error generating tweet with LLM (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    continue
                return None, None
        
        return None, None
    
    def _evaluate_tweet_quality(self, tweet: str) -> float:
        """Evaluate tweet quality based on various metrics"""
        score = 1.0
        
        # Check for project name
        if self.project_name and self.project_name.lower() not in tweet.lower():
            score -= 0.1
        
        # Check for hashtags
        if '#BuildInPublic' not in tweet:
            score -= 0.3
        hashtag_count = tweet.count('#')
        if hashtag_count < 2:
            score -= 0.1
        
        # Check for GitHub link
        if self.github_url and self.github_url not in tweet:
            score -= 0.2
        
        # Check for technical specificity (bullet points, numbers, tech terms)
        has_bullets = '-' in tweet or '•' in tweet
        has_numbers = any(char.isdigit() for char in tweet)
        if has_bullets:
            score += 0.1
        if has_numbers:
            score += 0.1
        
        # Penalize very short tweets (likely incomplete)
        if len(tweet) < 100:
            score -= 0.2
        
        # Check for generic words that indicate low quality
        generic_words = ['implemented', 'created', 'updated', 'improved']
        generic_count = sum(1 for word in generic_words if word.lower() in tweet.lower())
        if generic_count > 1:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def mark_as_posted(self, tweet: str, metadata: Dict[str, Any], timestamp: str):
        """Mark a tweet as posted with timestamp"""
        self._save_posted_tweet(tweet, metadata)
        if self.posted_tweets:
            self.posted_tweets[-1]['timestamp'] = timestamp
            with open(self.posted_tweets_file, 'w') as f:
                json.dump(self.posted_tweets, f, indent=2)
