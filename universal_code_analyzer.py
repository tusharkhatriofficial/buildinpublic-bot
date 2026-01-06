"""
Universal Code Analyzer
Analyzes any codebase (Java, Python, JavaScript, TypeScript, etc.) and extracts insights
Uses git history to understand development chronology
Uses LLM for deep code understanding
"""
import os
import subprocess
import re
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import logging
from groq import Groq

logger = logging.getLogger(__name__)


class UniversalCodeAnalyzer:
    def __init__(self, code_folder: str):
        self.code_folder = code_folder
        self.is_git_repo = os.path.exists(os.path.join(code_folder, '.git'))
        self.cache_file = os.path.join(os.path.dirname(code_folder), 'commit_insights.json')
        
        # Initialize LLM for deep analysis
        groq_api_key = os.getenv('GROQ_API_KEY')
        self.use_llm = groq_api_key and groq_api_key != 'your_groq_api_key_here'
        
        if self.use_llm:
            try:
                self.groq_client = Groq(api_key=groq_api_key)
                logger.info("LLM initialized for deep code analysis")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM for analysis: {e}")
                self.use_llm = False
        
        self.supported_extensions = {
            '.py': 'Python', '.js': 'JavaScript', '.jsx': 'React',
            '.ts': 'TypeScript', '.tsx': 'React', '.java': 'Java',
            '.kt': 'Kotlin', '.go': 'Go', '.rs': 'Rust',
            '.cpp': 'C++', '.c': 'C', '.rb': 'Ruby',
            '.php': 'PHP', '.swift': 'Swift', '.scala': 'Scala'
        }
        
    def get_git_commits(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get git commit history with file changes"""
        if not self.is_git_repo:
            return []
        
        try:
            # Get commit history with stats
            cmd = [
                'git', '-C', self.code_folder, 'log',
                '--pretty=format:%H|%an|%ae|%at|%s',
                '--stat', '--name-only',
                f'-{limit}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return []
            
            commits = []
            lines = result.stdout.split('\n')
            current_commit = None
            
            for line in lines:
                if '|' in line and len(line.split('|')) == 5:
                    if current_commit:
                        commits.append(current_commit)
                    
                    parts = line.split('|')
                    current_commit = {
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'timestamp': int(parts[3]),
                        'message': parts[4],
                        'files': []
                    }
                elif current_commit and line.strip() and not line.startswith(' '):
                    # File path
                    current_commit['files'].append(line.strip())
            
            if current_commit:
                commits.append(current_commit)
            
            return commits
        except Exception as e:
            print(f"Error getting git commits: {e}")
            return []
    
    def analyze_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single commit to extract insights with LLM enhancement"""
        message = commit['message'].lower()
        files = commit['files']
        
        # Get basic categorization
        categories = []
        if any(word in message for word in ['add', 'implement', 'create', 'new']):
            categories.append('feature')
        if any(word in message for word in ['fix', 'bug', 'issue', 'resolve']):
            categories.append('bugfix')
        if any(word in message for word in ['refactor', 'cleanup', 'improve', 'optimize']):
            categories.append('refactor')
        if any(word in message for word in ['test', 'spec']):
            categories.append('test')
        if any(word in message for word in ['doc', 'readme', 'comment']):
            categories.append('documentation')
        if any(word in message for word in ['api', 'endpoint', 'route']):
            categories.append('api')
        if any(word in message for word in ['ui', 'frontend', 'component', 'design']):
            categories.append('frontend')
        if any(word in message for word in ['database', 'migration', 'schema', 'model']):
            categories.append('database')
        
        # Detect technologies from file paths
        tech_stack = set()
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.java']:
                tech_stack.add('Java')
            elif ext in ['.py']:
                tech_stack.add('Python')
            elif ext in ['.js', '.jsx']:
                tech_stack.add('JavaScript')
            elif ext in ['.ts', '.tsx']:
                tech_stack.add('TypeScript')
            elif ext in ['.sql']:
                tech_stack.add('SQL')
            elif ext in ['.yaml', '.yml']:
                tech_stack.add('YAML')
            elif file == 'Dockerfile':
                tech_stack.add('Docker')
            elif file == 'docker-compose.yaml':
                tech_stack.add('Docker Compose')
            elif file == 'pom.xml':
                tech_stack.add('Maven')
            elif file == 'package.json':
                tech_stack.add('npm')
            
            # Framework detection
            if 'spring' in file.lower():
                tech_stack.add('Spring Boot')
            if 'react' in file.lower() or 'src/components' in file:
                tech_stack.add('React')
            if 'kafka' in file.lower():
                tech_stack.add('Kafka')
        
        analyzed = {
            'hash': commit['hash'][:8],
            'timestamp': commit['timestamp'],
            'date': datetime.fromtimestamp(commit['timestamp']).strftime('%Y-%m-%d'),
            'message': commit['message'],
            'categories': categories if categories else ['general'],
            'tech_stack': list(tech_stack),
            'files_changed': len(files),
            'files': files[:10]
        }
        
        # Use LLM for deeper analysis
        if self.use_llm and len(files) > 0:
            llm_insights = self._analyze_commit_with_llm(commit, analyzed)
            if llm_insights:
                analyzed['llm_insights'] = llm_insights
        
        return analyzed
    
    def _analyze_commit_with_llm(self, commit: Dict[str, Any], basic_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Use LLM to deeply understand commit context and impact"""
        if not self.use_llm or not self.groq_client:
            return None
        
        try:
            files_summary = ", ".join(basic_analysis['tech_stack'][:5])
            
            prompt = f"""Analyze this git commit for a developer building in public. Extract key insights for an engaging Twitter post.

Commit: {commit['message']}
Files changed: {basic_analysis['files_changed']} ({files_summary})
Categories: {', '.join(basic_analysis['categories'])}
Date: {basic_analysis['date']}

Provide JSON with:
- "what_built": Concise description of what was created/fixed (15 words max)
- "technical_detail": One interesting technical aspect
- "impact": Why this matters (10 words max)
- "hook": Engaging tweet opening (10 words max)

Focus on what developers would find interesting."""

            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            insights = json.loads(response.choices[0].message.content)
            logger.info(f"LLM insights: {insights.get('what_built', 'N/A')}")
            return insights
            
        except Exception as e:
            logger.warning(f"LLM analysis failed: {e}")
            return None
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get project name and GitHub repository URL"""
        project_info = {
            'name': None,
            'github_url': None
        }
        
        # Try to get from git remote
        if self.is_git_repo:
            try:
                cmd = ['git', '-C', self.code_folder, 'config', '--get', 'remote.origin.url']
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
                    
                    # Parse GitHub URL
                    if 'github.com' in remote_url:
                        # Handle both HTTPS and SSH formats
                        if remote_url.startswith('https://'):
                            # https://github.com/user/repo.git
                            project_info['github_url'] = remote_url.replace('.git', '')
                        elif remote_url.startswith('git@'):
                            # git@github.com:user/repo.git
                            remote_url = remote_url.replace('git@github.com:', 'https://github.com/')
                            project_info['github_url'] = remote_url.replace('.git', '')
                        
                        # Extract project name from URL
                        if project_info['github_url']:
                            project_info['name'] = project_info['github_url'].split('/')[-1]
            except:
                pass
        
        # Fallback: use folder name
        if not project_info['name']:
            project_info['name'] = os.path.basename(self.code_folder)
        
        return project_info
    
    def get_project_overview(self) -> Dict[str, Any]:
        """Get overview of the entire project"""
        overview = {
            'is_git_repo': self.is_git_repo,
            'languages': set(),
            'frameworks': set(),
            'total_files': 0,
            'file_types': {}
        }
        
        # Add project info
        project_info = self.get_project_info()
        overview['project_name'] = project_info['name']
        overview['github_url'] = project_info['github_url']
        
        # Walk through directory
        for root, dirs, files in os.walk(self.code_folder):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in [
                '.git', 'node_modules', 'target', 'build', 'dist', 
                '__pycache__', '.idea', 'venv', '.mvn'
            ]]
            
            for file in files:
                overview['total_files'] += 1
                ext = os.path.splitext(file)[1].lower()
                
                if ext:
                    overview['file_types'][ext] = overview['file_types'].get(ext, 0) + 1
                
                # Detect languages
                if ext in ['.java']:
                    overview['languages'].add('Java')
                elif ext in ['.py']:
                    overview['languages'].add('Python')
                elif ext in ['.js', '.jsx']:
                    overview['languages'].add('JavaScript')
                elif ext in ['.ts', '.tsx']:
                    overview['languages'].add('TypeScript')
                elif ext in ['.go']:
                    overview['languages'].add('Go')
                elif ext in ['.rs']:
                    overview['languages'].add('Rust')
                
                # Detect frameworks
                if file == 'pom.xml':
                    overview['frameworks'].add('Maven/Spring Boot')
                elif file == 'package.json':
                    overview['frameworks'].add('Node.js')
                elif file == 'requirements.txt':
                    overview['frameworks'].add('Python')
                elif file == 'Dockerfile':
                    overview['frameworks'].add('Docker')
                elif file == 'docker-compose.yaml':
                    overview['frameworks'].add('Docker Compose')
        
        overview['languages'] = list(overview['languages'])
        overview['frameworks'] = list(overview['frameworks'])
        
        return overview
    
    def get_chronological_insights(self) -> List[Dict[str, Any]]:
        """Get insights ordered chronologically (oldest to newest)"""
        commits = self.get_git_commits()
        
        # Reverse to get oldest first
        commits.reverse()
        
        insights = []
        for commit in commits:
            analyzed = self.analyze_commit(commit)
            insights.append(analyzed)
        
        return insights
    
    def build_knowledge_base(self) -> bool:
        """Build and cache LLM insights for all commits (run once to avoid rate limits)"""
        if not self.use_llm:
            print("❌ LLM not available. Please set GROQ_API_KEY in .env file.")
            return False
        
        print("🔍 Analyzing codebase with LLM (this may take a few minutes)...")
        print("⏳ Building knowledge base to avoid future rate limits...\n")
        
        commits = self.get_git_commits()
        commits.reverse()  # Oldest first
        
        cached_insights = []
        
        for idx, commit in enumerate(commits, 1):
            print(f"📊 [{idx}/{len(commits)}] Analyzing: {commit['message'][:60]}...")
            
            try:
                analyzed = self.analyze_commit(commit)
                cached_insights.append(analyzed)
                
                # Add delay to avoid rate limits (2 seconds between requests)
                if idx < len(commits):
                    time.sleep(2)
                    
            except Exception as e:
                logging.error(f"Error analyzing commit {commit['hash'][:8]}: {e}")
                print(f"  ⚠️  Skipped due to error")
        
        # Save to cache file
        try:
            cache_data = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_commits': len(cached_insights),
                'commits': cached_insights
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            print(f"\n✅ Knowledge base created successfully!")
            print(f"📁 Cached {len(cached_insights)} commits to: commit_insights.json")
            print(f"💡 Now run 'python bot.py test' or 'python bot.py post-now' without hitting rate limits.\n")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save cache: {e}")
            print(f"❌ Failed to save knowledge base: {e}")
            return False
    
    def load_from_cache(self) -> Optional[List[Dict[str, Any]]]:
        """Load pre-analyzed insights from cache"""
        if not os.path.exists(self.cache_file):
            return None
        
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            logger.info(f"✅ Loaded {cache_data['total_commits']} commits from cache (generated at {cache_data['generated_at']})")
            return cache_data['commits']
            
        except Exception as e:
            logging.error(f"Failed to load cache: {e}")
            return None
    
    def read_readme(self) -> Optional[str]:
        """Read README file if it exists"""
        readme_files = ['README.md', 'readme.md', 'README.txt', 'README']
        
        for readme in readme_files:
            path = os.path.join(self.code_folder, readme)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                except:
                    pass
        return None
