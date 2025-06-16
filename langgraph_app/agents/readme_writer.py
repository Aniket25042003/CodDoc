import json
from typing import Dict, Any
from .base_agent import BaseAgent

class ReadmeWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Generate a comprehensive README.md for the following project:
        
        Repository URL: {repo_url}
        
        Repository Structure:
        {repo_structure}
        
        Dependencies:
        {dependencies}
        
        Code Summaries:
        {code_summaries}
        
        Docstring Summaries:
        {doc_summaries}
        
        Please create a README.md that includes:
        1. Project title and description based on the repository URL and structure
        2. Installation instructions based on the dependencies found
        3. Usage examples inferred from the code structure
        4. Tech stack and dependencies listing
        5. Project structure overview
        6. Key features and functionality based on code analysis
        7. Contributing guidelines (standard)
        8. License information (mention if found, otherwise add standard note)
        
        Format the response as a proper markdown document with appropriate headers, sections, and formatting.
        Make sure to:
        - Extract the project name from the repository URL
        - Use the dependencies to suggest installation methods (pip, npm, etc.)
        - Include code examples based on main files found
        - Make it professional and comprehensive
        - Return ONLY the markdown content without wrapping it in code blocks
        - Do NOT start with ```markdown or end with ```
        """
        
    def format_data_for_prompt(self, data: Any) -> str:
        """Format data for inclusion in the prompt."""
        if isinstance(data, dict):
            if not data:
                return "None found"
            return json.dumps(data, indent=2)
        elif isinstance(data, list):
            if not data:
                return "None found"
            return "\n".join([f"- {item}" for item in data])
        else:
            return str(data) if data else "None found"
    
    def clean_markdown_response(self, response: str) -> str:
        """Clean up LLM response by removing markdown code block wrapping."""
        response = response.strip()
        
        # Check if response starts with ```markdown or ``` and ends with ```
        if response.startswith('```markdown'):
            # Remove opening ```markdown
            response = response[11:].strip()
        elif response.startswith('```'):
            # Remove opening ```
            response = response[3:].strip()
        
        # Remove closing ``` if present at the end
        if response.endswith('```'):
            response = response[:-3].strip()
        
        return response
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive README.md file."""
        # Call parent process to initialize state
        state = super().process(state)
        
        # Extract information from state
        repo_url = state.get("repo_url", "Unknown repository")
        repo_structure = self.format_data_for_prompt(state.get("repo_structure", {}))
        dependencies = self.format_data_for_prompt(state.get("dependencies", {}))
        code_summaries = self.format_data_for_prompt(state.get("code_summaries", {}))
        doc_summaries = self.format_data_for_prompt(state.get("doc_summaries", {}))
        
        # Generate README
        prompt_text = self.prompt_template.format(
            repo_url=repo_url,
            repo_structure=repo_structure,
            dependencies=dependencies,
            code_summaries=code_summaries,
            doc_summaries=doc_summaries
        )
        
        try:
            response = self.invoke_llm(prompt_text)
            
            # Clean up the response - remove markdown code block wrapping if present
            response = self.clean_markdown_response(response)
            
            # Ensure response is a proper README
            if not response.strip().startswith('#'):
                # Add a default title if LLM didn't include one
                project_name = repo_url.split('/')[-1].replace('.git', '') if repo_url != "Unknown repository" else "Project"
                response = f"# {project_name}\n\n{response}"
            
        except Exception as e:
            # Fallback README if LLM fails
            project_name = repo_url.split('/')[-1].replace('.git', '') if repo_url != "Unknown repository" else "Project"
            response = self.generate_fallback_readme(project_name, state)
        
        # Update state
        state["readme"] = response
        
        self.log_decision(state, f"Generated README with {len(response)} characters")
        
        return state
    
    def generate_fallback_readme(self, project_name: str, state: Dict[str, Any]) -> str:
        """Generate a basic README if LLM fails."""
        return f"""# {project_name}

## Description
This project was analyzed automatically. Please refer to the source code for detailed information.

## Installation
Please check the dependencies listed in the project files for installation instructions.

## Dependencies
{self.format_data_for_prompt(state.get("dependencies", {}))}

## Project Structure
{self.format_data_for_prompt(state.get("repo_structure", {}))}

## Usage
Please refer to the main files in the project for usage examples.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
Please check the project files for license information.
"""
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the README generation output."""
        return (
            "readme" in output and
            bool(output["readme"]) and
            "# " in output["readme"]  # Should have at least one heading
        ) 