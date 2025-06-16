import os
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent

class RepoAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Analyze the following repository and provide a comprehensive analysis:
        
        Repository URL: {repo_url}
        
        Repository Structure:
        {repo_structure}
        
        Dependencies Found:
        {dependencies}
        
        Sample Code Files:
        {sample_files}
        
        Please provide a comprehensive analysis including:
        1. Project type and main programming languages
        2. Key frameworks and dependencies
        3. Main components and architecture
        4. Entry points and important files
        5. Project purpose and functionality
        
        Format the response as a structured JSON with these keys:
        - project_type: Type of project (web app, library, etc.)
        - languages: List of programming languages used
        - frameworks: List of frameworks and libraries
        - components: List of main components
        - entry_points: List of key entry points
        - purpose: Brief description of project purpose
        - features: List of key features
        """
        
    def get_file_extensions(self, repo_path: str) -> Dict[str, int]:
        """Get count of files by extension."""
        extensions = {}
        for root, _, files in os.walk(repo_path):
            if '/.git/' in root or '/node_modules/' in root or '/__pycache__/' in root:
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:
                    extensions[ext] = extensions.get(ext, 0) + 1
        return extensions
        
    def find_dependencies(self, repo_path: str) -> Dict[str, Any]:
        """Find and parse dependency files."""
        dependencies = {}
        
        dependency_files = {
            'package.json': self.parse_package_json,
            'requirements.txt': self.parse_requirements_txt,
            'pom.xml': self.parse_pom_xml,
            'Cargo.toml': self.parse_cargo_toml,
            'go.mod': self.parse_go_mod
        }
        
        for filename, parser in dependency_files.items():
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                try:
                    deps = parser(filepath)
                    if deps:
                        dependencies[filename] = deps
                except Exception as e:
                    print(f"Error parsing {filename}: {e}")
        
        return dependencies
    
    def parse_package_json(self, filepath: str) -> Dict[str, Any]:
        """Parse package.json file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return {
            'dependencies': data.get('dependencies', {}),
            'devDependencies': data.get('devDependencies', {}),
            'scripts': data.get('scripts', {})
        }
    
    def parse_requirements_txt(self, filepath: str) -> List[str]:
        """Parse requirements.txt file."""
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    def parse_pom_xml(self, filepath: str) -> List[str]:
        """Parse pom.xml file (basic)."""
        with open(filepath, 'r') as f:
            content = f.read()
        # Simple regex to find artifact IDs
        import re
        artifacts = re.findall(r'<artifactId>(.*?)</artifactId>', content)
        return artifacts
    
    def parse_cargo_toml(self, filepath: str) -> List[str]:
        """Parse Cargo.toml file (basic)."""
        dependencies = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        in_deps = False
        for line in lines:
            line = line.strip()
            if line == '[dependencies]':
                in_deps = True
            elif line.startswith('[') and in_deps:
                break
            elif in_deps and '=' in line:
                dep = line.split('=')[0].strip()
                dependencies.append(dep)
        return dependencies
    
    def parse_go_mod(self, filepath: str) -> List[str]:
        """Parse go.mod file (basic)."""
        dependencies = []
        with open(filepath, 'r') as f:
            content = f.read()
        lines = content.split('\n')
        in_require = False
        for line in lines:
            line = line.strip()
            if line.startswith('require ('):
                in_require = True
            elif line == ')' and in_require:
                break
            elif in_require and line:
                dep = line.split()[0] if line.split() else ''
                if dep:
                    dependencies.append(dep)
        return dependencies
        
    def sample_code_files(self, repo_path: str, max_files: int = 5) -> Dict[str, str]:
        """Get content from a few important code files."""
        important_files = []
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.go', '.rs', '.rb', '.php'}
        
        # Look for main files first
        priority_files = ['main.py', 'app.py', 'index.js', 'index.ts', 'main.js', 'server.js']
        
        for priority_file in priority_files:
            filepath = os.path.join(repo_path, priority_file)
            if os.path.exists(filepath):
                important_files.append(filepath)
        
        # Add other code files
        for root, _, files in os.walk(repo_path):
            if len(important_files) >= max_files:
                break
            if '/.git/' in root or '/node_modules/' in root or '/__pycache__/' in root:
                continue
            for file in files:
                if len(important_files) >= max_files:
                    break
                ext = os.path.splitext(file)[1].lower()
                if ext in code_extensions:
                    filepath = os.path.join(root, file)
                    if filepath not in important_files:
                        important_files.append(filepath)
        
        # Read file contents
        file_contents = {}
        for filepath in important_files[:max_files]:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Truncate if too long
                if len(content) > 1000:
                    content = content[:1000] + "\n... (truncated)"
                relative_path = os.path.relpath(filepath, repo_path)
                file_contents[relative_path] = content
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
        
        return file_contents
        
    def build_repo_structure(self, repo_path: str) -> Dict[str, Any]:
        """Build a simplified repository structure."""
        structure = {"directories": [], "files": []}
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common non-essential directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.env', 'venv']]
            
            relative_root = os.path.relpath(root, repo_path)
            if relative_root != '.':
                structure["directories"].append(relative_root)
            
            for file in files:
                if not file.startswith('.') and not file.endswith(('.pyc', '.log')):
                    relative_path = os.path.relpath(os.path.join(root, file), repo_path)
                    structure["files"].append(relative_path)
        
        return structure
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the repository and analyze everything in one go."""
        # Call parent process to initialize state
        state = super().process(state)
        
        repo_path = state["repo_path"]
        repo_url = state["repo_url"]
        
        # Gather all information
        repo_structure = self.build_repo_structure(repo_path)
        dependencies = self.find_dependencies(repo_path)
        sample_files = self.sample_code_files(repo_path)
        
        # Format for LLM
        prompt_text = self.prompt_template.format(
            repo_url=repo_url,
            repo_structure=json.dumps(repo_structure, indent=2),
            dependencies=json.dumps(dependencies, indent=2),
            sample_files=json.dumps(sample_files, indent=2)
        )
        
        try:
            response = self.invoke_llm(prompt_text)
            
            # Try to parse as JSON
            try:
                analysis = json.loads(response)
            except:
                # Fallback if JSON parsing fails
                analysis = {
                    "project_type": "Unknown",
                    "languages": ["Multiple"],
                    "frameworks": ["Various"],
                    "components": ["Main application"],
                    "entry_points": ["Main files"],
                    "purpose": "Code repository analysis",
                    "features": ["Core functionality"],
                    "raw_analysis": response
                }
            
        except Exception as e:
            # Fallback analysis
            analysis = {
                "project_type": "Unknown",
                "languages": list(self.get_file_extensions(repo_path).keys())[:3],
                "frameworks": list(dependencies.keys()) if dependencies else [],
                "components": ["Main application"],
                "entry_points": ["Source files"],
                "purpose": "Code repository",
                "features": ["Core functionality"],
                "error": str(e)
            }
        
        # Update state with all the gathered information
        state["repo_structure"] = repo_structure
        state["dependencies"] = dependencies
        state["sample_files"] = sample_files
        state["repo_analysis"] = analysis
        
        self.log_decision(state, f"Analyzed repository with {len(sample_files)} files")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the repository analysis output."""
        required_keys = ["repo_structure", "dependencies", "repo_analysis"]
        return all(key in output for key in required_keys) 