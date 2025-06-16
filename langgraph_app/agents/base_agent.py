from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from ..tools.gemini_client import GeminiClient
import time

class BaseAgent:
    def __init__(self):
        """Initialize the base agent with Gemini model."""
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Initialize direct Gemini client as fallback
        self.gemini_client = GeminiClient()
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                temperature=0.7,
                google_api_key=api_key,
                # Add these parameters to fix serialization issues
                convert_system_message_to_human=True,
                verbose=False
            )
            self.use_langchain = True
        except Exception as e:
            print(f"Warning: LangChain Gemini initialization failed: {e}")
            print("Falling back to direct Gemini API client")
            self.use_langchain = False
        
    def invoke_llm(self, prompt: str) -> str:
        """Invoke the LLM with fallback handling."""
        # Removed delay to speed up processing
        
        if self.use_langchain:
            try:
                response = self.llm.invoke(prompt)
                return response.content
            except Exception as e:
                print(f"LangChain invocation failed: {e}, falling back to direct API")
                self.use_langchain = False
        
        # Use direct Gemini client (which has retry logic)
        return self.gemini_client.generate_content(prompt)
        
    def create_prompt(self, template: str) -> ChatPromptTemplate:
        """Create a chat prompt template."""
        return ChatPromptTemplate.from_template(template)
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the current state and return updates.
        To be implemented by child classes.
        """
        # Initialize state fields if they don't exist
        if "log" not in state:
            state["log"] = []
        if "decisions" not in state:
            state["decisions"] = []
        if "validation" not in state:
            state["validation"] = {}
            
        # Set current agent
        agent_name = self.__class__.__name__.replace("Agent", "").lower()
        state["current_agent"] = agent_name
        
        # Child classes should call super().process(state) and then implement their logic
        return state
        
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate the agent's output.
        To be implemented by child classes.
        """
        raise NotImplementedError("Child classes must implement validate_output()")
        
    def log_decision(self, state: Dict[str, Any], decision: str) -> None:
        """Log a decision to the state."""
        state["log"].append(f"{self.__class__.__name__}: {decision}")
        state["decisions"].append({
            "agent": self.__class__.__name__,
            "decision": decision
        }) 