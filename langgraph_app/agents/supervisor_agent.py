from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import json

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt_template = """
        Review the following agent output and determine if it meets quality standards:
        
        Agent: {agent_name}
        Output: {agent_output}
        
        Current State: {current_state}
        
        Please analyze:
        1. Completeness of information
        2. Quality of analysis
        3. Missing critical details
        4. Potential improvements
        
        Format the response as a structured JSON with these keys:
        - is_valid: boolean
        - issues: List of issues found
        - improvements: List of suggested improvements
        - decision: "continue" or "redo"
        """
        
    def validate_agent_output(self, agent_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the output of a specific agent using LLM."""
        agent_output = state.get(f"{agent_name}_output", {})
        
        validation_prompt = self.prompt_template.format(
            agent_name=agent_name,
            agent_output=json.dumps(agent_output, indent=2),
            current_state=json.dumps({k: v for k, v in state.items() 
                                    if k not in ['log', 'decisions']}, indent=2)
        )
        
        response = self.invoke_llm(validation_prompt)
        
        try:
            # Try to parse as JSON
            validation_result = json.loads(response)
            return validation_result
        except json.JSONDecodeError:
            # Fallback if not valid JSON
            return {
                "decision": "continue",
                "agent": agent_name,
                "issues": [],
                "suggestions": [],
                "overall_quality": "acceptable"
            }
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the current state and agent outputs."""
        # Call parent process to initialize state
        state = super().process(state)
        
        current_agent = state.get("current_agent", "")
        
        # Define validation rules for each agent
        validation_rules = {
            "repo_analyzer": ["repo_structure", "analysis"],
            "dependency_extractor": ["dependencies"],
            "code_understanding": ["important_files", "code_summaries"],
            "docstring_summarizer": ["doc_summaries"],
            "readme_writer": ["readme"]
        }
        
        # Check if required outputs exist
        required_keys = validation_rules.get(current_agent, [])
        missing_keys = [key for key in required_keys if key not in state or not state[key]]
        
        if missing_keys:
            validation_result = {
                "decision": "redo",
                "agent": current_agent,
                "issues": f"Missing required outputs: {missing_keys}",
                "suggestions": f"Please ensure {current_agent} generates: {required_keys}"
            }
        else:
            # All required outputs are present, continue to next agent
            validation_result = {
                "decision": "continue",
                "agent": current_agent,
                "issues": [],
                "suggestions": [],
                "overall_quality": "acceptable"
            }
        
        # Update state with validation
        state["validation"] = validation_result
        
        self.log_decision(state, f"Validated {current_agent}: {validation_result['decision']}")
        
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the supervisor's output."""
        return (
            "validation" in output and
            "is_valid" in output["validation"] and
            "decision" in output["validation"]
        ) 