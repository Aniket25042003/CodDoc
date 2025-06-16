import os
from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..tools.file_selector import select_important_files as file_selector

class CodeUnderstandingAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Analyze the following source code file and provide a summary:
        
        File: {file_path}
        Content:
        {file_content}
        
        Please provide:
        1. Main purpose of the file
        2. Key functions/classes and their purposes
        3. Important algorithms or patterns
        4. Dependencies and relationships
        
        Format the response as a structured JSON with these keys:
        - purpose: Main purpose of the file
        - components: List of key components with descriptions
        - patterns: List of important patterns
        - dependencies: List of dependencies
        """

    def select_important_files(self, repo_path: str, repo_structure: Dict[str, Any]) -> List[str]:
        """Select important files for code analysis."""
        try:
            # Use the file selector tool
            important_files = file_selector(repo_path, repo_structure)
            return important_files
        except Exception as e:
            print(f"Error selecting important files: {e}")
            # Fallback: manually select common important files
            return self._fallback_file_selection(repo_path)

    def _fallback_file_selection(self, repo_path: str) -> List[str]:
        """Fallback method to select important files manually."""
        important_files = []
        common_files = [
            'main.py', 'app.py', '__init__.py', 'setup.py',
            'requirements.txt', 'package.json', 'README.md',
            'config.py', 'settings.py', 'models.py', 'views.py'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.env']]
            
            for file in files:
                file_path = os.path.join(root, file)
                # Include files with common extensions or specific names
                if (file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb', '.php')) or
                    file in common_files):
                    important_files.append(file_path)
                    if len(important_files) >= 10:  # Limit to avoid too many files
                        break
            if len(important_files) >= 10:
                break
        
        return important_files

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file and return a summary."""
        try:
            content = self.read_file_content(file_path)
            if not content:
                return {"error": "Could not read file content"}
            
            # Truncate content if too long to avoid token limits
            if len(content) > 3000:
                content = content[:3000] + "\n... (truncated)"
            
            prompt = self.prompt_template.format(
                file_path=file_path,
                file_content=content
            )
            
            # Use the LLM to analyze the file
            response = self.invoke_llm(prompt)
            
            # Try to parse as JSON, fallback to text if parsing fails
            try:
                import json
                analysis = json.loads(response)
            except:
                # If JSON parsing fails, create a structured response
                analysis = {
                    "purpose": "Analysis of " + os.path.basename(file_path),
                    "components": ["Content analysis available"],
                    "patterns": ["File structure analysis"],
                    "dependencies": ["Dependencies found in file"],
                    "raw_analysis": response
                }
            
            return analysis
            
        except Exception as e:
            return {
                "error": f"Error analyzing file: {str(e)}",
                "purpose": "Error during analysis",
                "components": [],
                "patterns": [],
                "dependencies": []
            }
        
    def read_file_content(self, file_path: str) -> str:
        """Read the content of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return ""
            
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and understand the codebase."""
        # Call parent process to initialize state
        state = super().process(state)
        
        repo_path = state["repo_path"]
        repo_structure = state["repo_structure"]
        
        # Select important files for analysis
        important_files = self.select_important_files(repo_path, repo_structure)
        
        # Analyze selected files
        code_summaries = {}
        for file_path in important_files:
            try:
                summary = self.analyze_file(file_path)
                relative_path = os.path.relpath(file_path, repo_path)
                code_summaries[relative_path] = summary
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        # Update state
        state["important_files"] = important_files
        state["code_summaries"] = code_summaries
        
        self.log_decision(state, f"Analyzed {len(important_files)} important files")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the code understanding output."""
        return (
            "important_files" in output and
            "code_summaries" in output and
            len(output["code_summaries"]) > 0
        ) 