import os
from typing import Dict, Any
from .base_agent import BaseAgent

class RepoAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Analyze the following repository structure and provide a summary:
        
        Repository Structure:
        {repo_structure}
        
        Please provide:
        1. Main components and their purposes
        2. Entry points and key files
        3. Overall architecture pattern
        4. Notable features or patterns
        
        Format the response as a structured JSON with these keys:
        - components: List of main components
        - entry_points: List of key entry points
        - architecture: Description of architecture
        - patterns: List of notable patterns
        """
        
    def build_repo_structure(self, repo_path: str) -> Dict[str, Any]:
        """Build a structured representation of the repository."""
        structure = {}
        
        for root, dirs, files in os.walk(repo_path):
            rel_path = os.path.relpath(root, repo_path)
            if rel_path == '.':
                rel_path = ''
                
            current = structure
            if rel_path:
                for part in rel_path.split(os.sep):
                    current = current.setdefault(part, {})
                    
            current['files'] = files
            current['dirs'] = dirs
            
        return structure
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the repository and analyze its structure."""
        # Call parent process to initialize state
        state = super().process(state)
        
        repo_path = state["repo_path"]
        
        # Build repository structure
        repo_structure = self.build_repo_structure(repo_path)
        
        # Get analysis from LLM
        prompt_text = self.prompt_template.format(repo_structure=repo_structure)
        response = self.invoke_llm(prompt_text)
        
        # Update state
        state["repo_structure"] = repo_structure
        state["analysis"] = response
        
        self.log_decision(state, f"Analyzed repository structure with {len(repo_structure)} top-level items")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the repository analysis output."""
        required_keys = ["repo_structure", "analysis"]
        return all(key in output for key in required_keys) and bool(output["analysis"]) 