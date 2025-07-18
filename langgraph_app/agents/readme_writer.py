import json
from typing import Dict, Any
from .base_agent import BaseAgent

class ReadmeWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Generate a comprehensive README.md for the following project:
        
        Repository URL: {repo_url}
        
        Repository Analysis:
        {repo_analysis}
        
        Dependencies:
        {dependencies}
        
        Repository Structure:
        {repo_structure}

        Project Purpose:
        {project_purpose}

        
        Please create a professional README.md that includes:
        1. Project title (extract from repository URL)
        2. Brief description based on the analysis
        3. Features list based on the code analysis
        4. Installation instructions based on dependencies
        5. Usage examples inferred from code structure
        6. Tech stack and dependencies
        7. Project structure overview
        8. Contributing guidelines
        9. License section
        
        Format as proper markdown with:
        - Clear headers and sections
        - Professional tone
        - Proper markdown formatting (headers, lists, code blocks)
        - Installation commands based on detected dependencies
        - Usage examples based on entry points
        - DO NOT wrap in ```markdown or ``` code blocks
        - Return ONLY the markdown content
        """
        
    def extract_project_name(self, repo_url: str) -> str:
        """Extract project name from repository URL."""
        try:
            # Remove .git extension and extract last part
            name = repo_url.rstrip('/').split('/')[-1]
            if name.endswith('.git'):
                name = name[:-4]
            return name
        except:
            return "Project"
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive README.md file."""
        # Call parent process to initialize state
        state = super().process(state)
        
        # Extract information from state
        repo_url = state.get("repo_url", "Unknown repository")
        repo_analysis = state.get("repo_analysis", {})
        dependencies = state.get("dependencies", {})
        repo_structure = state.get("repo_structure", {})
        sample_files = state.get("sample_files", {})
        
        # Format data for prompt
        prompt_text = self.prompt_template.format(
            repo_url=repo_url,
            repo_analysis=json.dumps(repo_analysis, indent=2),
            dependencies=json.dumps(dependencies, indent=2),
            repo_structure=json.dumps(repo_structure, indent=2),
            project_purpose=json.dumps(sample_files, indent=2)
        )
        
        try:
            response = self.invoke_llm(prompt_text)
            
            # Clean up the response
            response = response.strip()
            
            # Remove markdown code block wrapping if present
            if response.startswith('```markdown'):
                response = response[11:].strip()
            elif response.startswith('```'):
                response = response[3:].strip()
            
            if response.endswith('```'):
                response = response[:-3].strip()
            
            # Ensure response starts with a header
            if not response.strip().startswith('#'):
                project_name = self.extract_project_name(repo_url)
                response = f"# {project_name}\n\n{response}"
            
        except Exception as e:
            # Fallback README if LLM fails
            project_name = self.extract_project_name(repo_url)
            response = self.generate_fallback_readme(project_name, state)
        
        # Update state
        state["readme"] = response
        
        self.log_decision(state, f"Generated README with {len(response)} characters")
        
        return state
    
    def generate_fallback_readme(self, project_name: str, state: Dict[str, Any]) -> str:
        """Generate a basic README if LLM fails."""
        repo_analysis = state.get("repo_analysis", {})
        dependencies = state.get("dependencies", {})
        
        # Extract some basic info
        languages = repo_analysis.get("languages", ["Unknown"])
        project_type = repo_analysis.get("project_type", "Application")
        
        # Determine installation command
        install_cmd = "# See project files for installation instructions"
        if "package.json" in dependencies:
            install_cmd = "npm install"
        elif "requirements.txt" in dependencies:
            install_cmd = "pip install -r requirements.txt"
        elif "Cargo.toml" in dependencies:
            install_cmd = "cargo build"
        elif "go.mod" in dependencies:
            install_cmd = "go mod tidy && go build"
        
        return f"""# {project_name}

## Description

{project_type} written in {', '.join(languages[:3])}.

## Installation

```bash
{install_cmd}
```

## Usage

Please refer to the source code for usage instructions.

## Tech Stack

- **Languages**: {', '.join(languages[:5])}
- **Dependencies**: {len(dependencies)} dependency files found

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