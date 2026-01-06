"""
Tweet Generator Module
Generates engaging tweets from code analysis insights
"""
import random
import json
import os
from typing import Dict, List, Any


class TweetGenerator:
    def __init__(self, posted_tweets_file: str = 'posted_tweets.json'):
        self.posted_tweets_file = posted_tweets_file
        self.posted_tweets = self._load_posted_tweets()
        self.max_length = 280
        
        # Templates for different types of tweets
        self.templates = {
            'feature': [
                "Just shipped {feature}\n{description}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "New feature live: {feature}\n{description}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Implemented {feature}\n{description}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'class': [
                "Built {class_name} class\n- {method_count} methods\n- {purpose}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Architecting {class_name}\n{purpose}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "{class_name} is taking shape\n{purpose}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'function': [
                "Wrote {function_name}()\n{purpose}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "New function: {function_name}()\n{purpose}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'milestone': [
                "Milestone unlocked\n{achievement}\n{stats}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Progress update:\n- {achievement}\n- {stats}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Hit a milestone\n{achievement}\n{stats}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'challenge': [
                "Solving: {challenge}\n{approach}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Challenge: {challenge}\nSolution: {approach}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'tech_stack': [
                "Using {tech} for {purpose}\n{benefit}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Tech choice: {tech}\n{benefit}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ],
            'insight': [
                "Learned: {lesson}\n{context}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
                "Key insight:\n{lesson}\n{context}\n\n#BuildInPublic #{hashtag1} #{hashtag2}",
            ]
        }
        
        # Hashtag mapping for different technologies/concepts
        self.hashtag_map = {
            'async': ['AsyncProgramming', 'Python'],
            'api': ['API', 'DevTools'],
            'web': ['WebDev', 'Python'],
            'scraper': ['WebScraping', 'Automation'],
            'data': ['DataScience', 'Python'],
            'database': ['Database', 'Backend'],
            'pandas': ['DataScience', 'Python'],
            'requests': ['API', 'Python'],
            'flask': ['WebDev', 'Python'],
            'django': ['Django', 'WebDev'],
            'fastapi': ['FastAPI', 'Python'],
            'machine': ['MachineLearning', 'AI'],
            'neural': ['DeepLearning', 'AI'],
            'test': ['Testing', 'QA'],
            'docker': ['Docker', 'DevOps'],
            'kubernetes': ['K8s', 'DevOps'],
            'aws': ['AWS', 'Cloud'],
            'azure': ['Azure', 'Cloud'],
            'microservice': ['Microservices', 'Architecture'],
            'algorithm': ['Algorithms', 'ComputerScience'],
            'optimization': ['Performance', 'Engineering'],
            'security': ['Security', 'CyberSecurity'],
            'authentication': ['Auth', 'Security'],
            'cache': ['Performance', 'Backend'],
            'queue': ['MessageQueue', 'Backend'],
            'logging': ['Observability', 'DevOps'],
            'monitoring': ['Monitoring', 'DevOps'],
            'graphql': ['GraphQL', 'API'],
            'rest': ['REST', 'API'],
            'react': ['React', 'Frontend'],
            'typescript': ['TypeScript', 'JavaScript'],
            'node': ['NodeJS', 'Backend'],
        }
    
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
            'timestamp': None  # Will be set when actually posted
        })
        with open(self.posted_tweets_file, 'w') as f:
            json.dump(self.posted_tweets, f, indent=2)
    
    def _is_duplicate(self, tweet: str) -> bool:
        """Check if a similar tweet has been posted before"""
        # Simple duplicate check - you can make this more sophisticated
        for posted in self.posted_tweets:
            if posted['tweet'] == tweet:
                return True
            # Check for high similarity (basic approach)
            if self._similarity(tweet, posted['tweet']) > 0.8:
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
    
    def _truncate(self, text: str) -> str:
        """Truncate text to fit Twitter's character limit"""
        if len(text) <= self.max_length:
            return text
        return text[:self.max_length - 3] + "..."
    
    def _get_relevant_hashtags(self, context: str) -> tuple:
        """Get relevant hashtags based on context"""
        context_lower = context.lower()
        
        # Find matching hashtags
        matched_tags = []
        for key, tags in self.hashtag_map.items():
            if key in context_lower:
                matched_tags.extend(tags)
        
        # Default hashtags if no matches
        if not matched_tags:
            matched_tags = ['Python', 'Coding']
        
        # Remove duplicates and return top 2
        unique_tags = list(dict.fromkeys(matched_tags))
        return (unique_tags[0] if len(unique_tags) > 0 else 'Python',
                unique_tags[1] if len(unique_tags) > 1 else 'Coding')
    
    def generate_from_file_analysis(self, file_insights: Dict[str, Any]) -> str:
        """Generate a tweet from file analysis insights"""
        filename = file_insights['filename']
        
        # Create context for hashtag selection
        context = f"{filename} {' '.join(file_insights.get('imports', []))} {' '.join(file_insights.get('complexity_indicators', []))}"
        
        # Generate tweets about classes
        if file_insights['classes']:
            for cls in file_insights['classes']:
                hashtag1, hashtag2 = self._get_relevant_hashtags(
                    f"{cls['name']} {cls.get('docstring', '')} {context}"
                )
                tweet_data = {
                    'class_name': cls['name'],
                    'method_count': len(cls['methods']),
                    'purpose': (cls['docstring'][:80] if cls['docstring'] else "Core functionality").replace('\n', ' '),
                    'hashtag1': hashtag1,
                    'hashtag2': hashtag2
                }
                template = random.choice(self.templates['class'])
                tweet = self._truncate(template.format(**tweet_data))
                if not self._is_duplicate(tweet):
                    return tweet, {'type': 'class', 'file': filename, 'class': cls['name']}
        
        # Generate tweets about functions
        if file_insights['functions']:
            for func in file_insights['functions']:
                if not func['name'].startswith('_'):  # Skip private functions
                    hashtag1, hashtag2 = self._get_relevant_hashtags(
                        f"{func['name']} {func.get('docstring', '')} {context}"
                    )
                    tweet_data = {
                        'function_name': func['name'],
                        'purpose': (func['docstring'][:100] if func['docstring'] else "Solve a key problem").replace('\n', ' '),
                        'hashtag1': hashtag1,
                        'hashtag2': hashtag2
                    }
                    template = random.choice(self.templates['function'])
                    tweet = self._truncate(template.format(**tweet_data))
                    if not self._is_duplicate(tweet):
                        return tweet, {'type': 'function', 'file': filename, 'function': func['name']}
        
        # Generate tweets about complexity indicators
        if file_insights['complexity_indicators']:
            indicator = random.choice(file_insights['complexity_indicators'])
            hashtag1, hashtag2 = self._get_relevant_hashtags(f"{indicator} {context}")
            tweet_data = {
                'feature': indicator,
                'description': f"Making it robust and scalable",
                'hashtag1': hashtag1,
                'hashtag2': hashtag2
            }
            template = random.choice(self.templates['feature'])
            tweet = self._truncate(template.format(**tweet_data))
            if not self._is_duplicate(tweet):
                return tweet, {'type': 'feature', 'file': filename, 'feature': indicator}
        
        return None, None
    
    def generate_milestone_tweet(self, overview: Dict[str, Any]) -> str:
        """Generate a milestone tweet from codebase overview"""
        achievements = [
            (f"{overview['total_files']} files, {overview['total_lines']} lines", 
             f"Built with {overview['unique_imports']} libraries"),
            (f"{overview['total_classes']} classes, {overview['total_functions']} functions",
             "Architecture taking shape"),
            (f"Codebase at {overview['total_lines']} lines",
             f"{overview['total_files']} modules and growing"),
        ]
        
        achievement, stats = random.choice(achievements)
        hashtag1, hashtag2 = self._get_relevant_hashtags(f"milestone progress {achievement}")
        tweet_data = {
            'achievement': achievement,
            'stats': stats,
            'hashtag1': hashtag1,
            'hashtag2': hashtag2
        }
        template = random.choice(self.templates['milestone'])
        tweet = self._truncate(template.format(**tweet_data))
        
        if not self._is_duplicate(tweet):
            return tweet, {'type': 'milestone', 'stats': overview}
        return None, None
    
    def generate_tech_stack_tweet(self, imports: List[str]) -> str:
        """Generate a tweet about technology stack"""
        if not imports:
            return None, None
        
        interesting_imports = [imp for imp in imports if not imp.startswith('_')]
        if not interesting_imports:
            return None, None
        
        tech = random.choice(interesting_imports)
        hashtag1, hashtag2 = self._get_relevant_hashtags(tech)
        
        purposes = [
            "boost performance",
            "improve code quality",
            "enhance functionality",
            "simplify architecture",
            "scale better"
        ]
        benefits = [
            "Makes the system more robust",
            "Improves reliability",
            "Enables powerful features",
            "Streamlines development",
            "Better performance"
        ]
        
        tweet_data = {
            'tech': tech,
            'purpose': random.choice(purposes),
            'benefit': random.choice(benefits),
            'hashtag1': hashtag1,
            'hashtag2': hashtag2
        }
        template = random.choice(self.templates['tech_stack'])
        tweet = self._truncate(template.format(**tweet_data))
        
        if not self._is_duplicate(tweet):
            return tweet, {'type': 'tech_stack', 'library': tech}
        return None, None
    
    def mark_as_posted(self, tweet: str, metadata: Dict[str, Any], timestamp: str):
        """Mark a tweet as posted with timestamp"""
        self._save_posted_tweet(tweet, metadata)
        # Update the last entry with timestamp
        if self.posted_tweets:
            self.posted_tweets[-1]['timestamp'] = timestamp
            with open(self.posted_tweets_file, 'w') as f:
                json.dump(self.posted_tweets, f, indent=2)
