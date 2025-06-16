import os
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class DocstringSummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Analyze and summarize the following docstrings:
        
        {docstrings}
        
        Please provide:
        1. A clear summary of each function/class
        2. Key parameters and return values
        3. Important notes or warnings
        4. Usage examples if present
        
        Format the response as a structured JSON with these keys:
        - summaries: List of summaries for each docstring
        - parameters: List of parameter descriptions
        - notes: List of important notes
        - examples: List of usage examples
        """
        
    def extract_docstrings(self, file_path: str) -> List[Dict[str, str]]:
        """Extract docstrings from a file."""
        docstrings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Python docstring patterns
            python_patterns = [
                r'def\s+(\w+)\s*\([^)]*\):\s*"""(.*?)"""',  # Function docstrings
                r'class\s+(\w+)\s*\([^)]*\):\s*"""(.*?)"""'  # Class docstrings
            ]
            
            # JavaScript/TypeScript docstring patterns
            js_patterns = [
                r'/\*\*\s*\n\s*\*\s*(.*?)\s*\n\s*\*/\s*\n\s*(?:export\s+)?(?:async\s+)?(?:function|const)\s+(\w+)',  # Function JSDoc
                r'/\*\*\s*\n\s*\*\s*(.*?)\s*\n\s*\*/\s*\n\s*class\s+(\w+)'  # Class JSDoc
            ]
            
            # Try Python patterns
            for pattern in python_patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    name, doc = match.groups()
                    docstrings.append({
                        'name': name,
                        'type': 'python',
                        'docstring': doc.strip()
                    })
                    
            # Try JavaScript patterns
            for pattern in js_patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    doc, name = match.groups()
                    docstrings.append({
                        'name': name,
                        'type': 'javascript',
                        'docstring': doc.strip()
                    })
                    
        except Exception as e:
            print(f"Error extracting docstrings from {file_path}: {str(e)}")
            
        return docstrings
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and summarize docstrings from important files."""
        # Call parent process to initialize state
        state = super().process(state)
        
        important_files = state.get("important_files", [])
        doc_summaries = {}
        
        for file_path in important_files:
            try:
                # Extract docstrings
                docstrings = self.extract_docstrings(file_path)
                
                if docstrings:
                    # Summarize docstrings
                    summary = self.summarize_docstrings(docstrings)
                    relative_path = os.path.relpath(file_path, state["repo_path"])
                    doc_summaries[relative_path] = summary
                    
            except Exception as e:
                print(f"Error processing docstrings in {file_path}: {e}")
        
        # Update state
        state["doc_summaries"] = doc_summaries
        
        self.log_decision(state, f"Extracted docstrings from {len(doc_summaries)} files")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the docstring summarization output."""
        required_keys = ["summaries", "parameters", "notes", "examples"]
        return all(key in output.get("doc_summaries", {}) for key in required_keys) 