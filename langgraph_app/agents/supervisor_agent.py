from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import json

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Simplified supervisor - no LLM needed for basic validation
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the current state and agent outputs quickly."""
        # Call parent process to initialize state
        state = super().process(state)
        
        current_agent = state.get("current_agent", "")
        
        # Define simplified validation rules for each agent
        validation_rules = {
            "repo_analyzer": ["repo_structure", "dependencies", "repo_analysis"],
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
            "decision" in output["validation"]
        ) 