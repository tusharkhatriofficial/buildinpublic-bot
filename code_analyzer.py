"""
Code Analyzer Module
Analyzes Python code files and extracts interesting insights
"""
import os
import ast
import re
from typing import List, Dict, Any


class CodeAnalyzer:
    def __init__(self, code_folder: str):
        self.code_folder = code_folder
        self.files_analyzed = []
        
    def get_all_python_files(self) -> List[str]:
        """Get all Python files from the code folder"""
        python_files = []
        for root, dirs, files in os.walk(self.code_folder):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules']]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files
    
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a single Python file and extract interesting information"""
        insights = {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'classes': [],
            'functions': [],
            'imports': [],
            'decorators': [],
            'docstrings': [],
            'complexity_indicators': [],
            'line_count': 0,
            'comments': []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                insights['line_count'] = len(content.split('\n'))
                
            # Parse the AST
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Extract classes
                if isinstance(node, ast.ClassDef):
                    insights['classes'].append({
                        'name': node.name,
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        'bases': [self._get_name(base) for base in node.bases],
                        'docstring': ast.get_docstring(node)
                    })
                
                # Extract functions
                elif isinstance(node, ast.FunctionDef):
                    insights['functions'].append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'decorators': [self._get_name(dec) for dec in node.decorator_list],
                        'is_async': isinstance(node, ast.AsyncFunctionDef),
                        'docstring': ast.get_docstring(node)
                    })
                
                # Extract imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        insights['imports'].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        insights['imports'].append(node.module)
            
            # Extract comments
            for line in content.split('\n'):
                stripped = line.strip()
                if stripped.startswith('#') and not stripped.startswith('#!'):
                    insights['comments'].append(stripped[1:].strip())
            
            # Detect complexity indicators
            if 'async' in content or 'await' in content:
                insights['complexity_indicators'].append('asynchronous programming')
            if 'class ' in content and 'def __init__' in content:
                insights['complexity_indicators'].append('object-oriented design')
            if re.search(r'@\w+', content):
                insights['complexity_indicators'].append('decorators')
            if 'threading' in content or 'multiprocessing' in content:
                insights['complexity_indicators'].append('concurrency')
            if 'try:' in content and 'except' in content:
                insights['complexity_indicators'].append('error handling')
                
        except Exception as e:
            insights['error'] = str(e)
        
        return insights
    
    def _get_name(self, node):
        """Helper to get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)
    
    def get_codebase_overview(self) -> Dict[str, Any]:
        """Get overview of entire codebase"""
        files = self.get_all_python_files()
        total_lines = 0
        total_classes = 0
        total_functions = 0
        all_imports = set()
        
        for file in files:
            insights = self.analyze_file(file)
            total_lines += insights['line_count']
            total_classes += len(insights['classes'])
            total_functions += len(insights['functions'])
            all_imports.update(insights['imports'])
        
        return {
            'total_files': len(files),
            'total_lines': total_lines,
            'total_classes': total_classes,
            'total_functions': total_functions,
            'unique_imports': len(all_imports),
            'files': files
        }
