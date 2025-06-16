import os
import json
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class DependencyExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Analyze the following dependency files and extract the tech stack:
        
        {dependency_files}
        
        Please provide a structured analysis of:
        1. Main programming languages
        2. Key frameworks and libraries
        3. Development tools
        4. Build and deployment tools
        
        Format the response as a structured JSON with these keys:
        - languages: List of programming languages
        - frameworks: List of frameworks
        - libraries: List of key libraries
        - tools: List of development and build tools
        """
        
    def find_dependency_files(self, repo_path: str) -> Dict[str, str]:
        """Find and read dependency files in the repository."""
        dependency_files = {}
        common_files = {
            'requirements.txt': 'python',
            'package.json': 'javascript',
            'pom.xml': 'java',
            'build.gradle': 'java',
            'Gemfile': 'ruby',
            'composer.json': 'php',
            'go.mod': 'go',
            'Cargo.toml': 'rust'
        }
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file in common_files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            dependency_files[file] = {
                                'type': common_files[file],
                                'content': content
                            }
                    except Exception as e:
                        print(f"Error reading {file}: {str(e)}")
                        
        return dependency_files

    def extract_npm_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from package.json."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            dependencies = {}
            if 'dependencies' in data:
                dependencies['dependencies'] = data['dependencies']
            if 'devDependencies' in data:
                dependencies['devDependencies'] = data['devDependencies']
            if 'scripts' in data:
                dependencies['scripts'] = data['scripts']
                
            return dependencies
        except Exception as e:
            self.log_decision({}, f"Error parsing package.json: {str(e)}")
            return {}

    def extract_pip_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from requirements.txt."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    dependencies.append(line)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing requirements.txt: {str(e)}")
            return {}

    def extract_pipenv_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from Pipfile."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic parsing for Pipfile (TOML-like format)
            dependencies = {'dependencies': [], 'dev_dependencies': []}
            current_section = None
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('[packages]'):
                    current_section = 'dependencies'
                elif line.startswith('[dev-packages]'):
                    current_section = 'dev_dependencies'
                elif '=' in line and current_section:
                    package = line.split('=')[0].strip()
                    dependencies[current_section].append(package)
            
            return dependencies
        except Exception as e:
            self.log_decision({}, f"Error parsing Pipfile: {str(e)}")
            return {}

    def extract_poetry_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from poetry.lock."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract package names from poetry.lock
            dependencies = []
            lines = content.split('\n')
            for line in lines:
                if line.startswith('name = '):
                    package_name = line.split('"')[1]
                    dependencies.append(package_name)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing poetry.lock: {str(e)}")
            return {}

    def extract_maven_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from pom.xml."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex to find dependencies
            dependencies = []
            artifact_pattern = r'<artifactId>(.*?)</artifactId>'
            artifacts = re.findall(artifact_pattern, content)
            dependencies.extend(artifacts)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing pom.xml: {str(e)}")
            return {}

    def extract_gradle_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from build.gradle."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = []
            # Simple pattern to find implementation/compile dependencies
            dep_patterns = [
                r"implementation\s+['\"]([^'\"]+)['\"]",
                r"compile\s+['\"]([^'\"]+)['\"]",
                r"api\s+['\"]([^'\"]+)['\"]"
            ]
            
            for pattern in dep_patterns:
                deps = re.findall(pattern, content)
                dependencies.extend(deps)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing build.gradle: {str(e)}")
            return {}

    def extract_go_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from go.mod."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = []
            lines = content.split('\n')
            in_require = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('require ('):
                    in_require = True
                    continue
                elif line == ')' and in_require:
                    in_require = False
                    continue
                elif in_require and line:
                    dep = line.split()[0] if line.split() else ''
                    if dep:
                        dependencies.append(dep)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing go.mod: {str(e)}")
            return {}

    def extract_cargo_dependencies(self, file_path: str) -> Dict[str, Any]:
        """Extract dependencies from Cargo.toml."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = []
            lines = content.split('\n')
            in_dependencies = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('[dependencies]'):
                    in_dependencies = True
                    continue
                elif line.startswith('[') and in_dependencies:
                    in_dependencies = False
                    continue
                elif in_dependencies and '=' in line:
                    dep = line.split('=')[0].strip()
                    dependencies.append(dep)
            
            return {'dependencies': dependencies}
        except Exception as e:
            self.log_decision({}, f"Error parsing Cargo.toml: {str(e)}")
            return {}
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract dependencies from the repository."""
        # Call parent process to initialize state
        state = super().process(state)
        
        repo_path = state["repo_path"]
        dependencies = {}
        
        # Check for various dependency files
        dependency_files = {
            "package.json": self.extract_npm_dependencies,
            "requirements.txt": self.extract_pip_dependencies,
            "Pipfile": self.extract_pipenv_dependencies,
            "poetry.lock": self.extract_poetry_dependencies,
            "pom.xml": self.extract_maven_dependencies,
            "build.gradle": self.extract_gradle_dependencies,
            "go.mod": self.extract_go_dependencies,
            "Cargo.toml": self.extract_cargo_dependencies
        }
        
        for dep_file, extractor in dependency_files.items():
            file_path = os.path.join(repo_path, dep_file)
            if os.path.exists(file_path):
                deps = extractor(file_path)
                if deps:
                    dependencies[dep_file] = deps
        
        # Update state
        state["dependencies"] = dependencies
        
        self.log_decision(state, f"Extracted dependencies from {len(dependencies)} files")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the dependency extraction output."""
        required_keys = ["languages", "frameworks", "libraries", "tools"]
        return all(key in output.get("dependencies", {}) for key in required_keys) 