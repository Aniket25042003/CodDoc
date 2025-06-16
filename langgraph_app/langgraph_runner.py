from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging
import traceback
from .agents.repo_analyzer import RepoAnalyzerAgent
from .agents.readme_writer import ReadmeWriterAgent
from .agents.supervisor_agent import SupervisorAgent

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    """Simplified state schema for the LangGraph workflow."""
    repo_url: str
    repo_path: str
    repo_structure: Dict[str, Any]
    dependencies: Dict[str, Any]
    sample_files: Dict[str, str]
    repo_analysis: Dict[str, Any]
    readme: str
    log: List[str]
    decisions: List[Dict[str, Any]]
    current_agent: str
    validation: Dict[str, Any]

async def run_langgraph(state: Dict[str, Any]) -> Dict[str, Any]:
    """Run the simplified LangGraph workflow for README generation."""
    
    try:
        logger.info("Initializing simplified workflow with 2 agents...")
        # Initialize agents
        repo_analyzer = RepoAnalyzerAgent()
        readme_writer = ReadmeWriterAgent()
        supervisor = SupervisorAgent()
        logger.info("All agents initialized successfully")
        
        # Create the graph with simplified state schema
        logger.info("Creating simplified StateGraph...")
        workflow = StateGraph(GraphState)
        
        # Define nodes (only 2 main agents + supervisor)
        logger.info("Adding nodes to graph...")
        workflow.add_node("repo_analyzer", repo_analyzer.process)
        workflow.add_node("readme_writer", readme_writer.process)
        workflow.add_node("supervisor", supervisor.process)
        
        # Define simple sequential edges
        logger.info("Adding simplified edges...")
        workflow.add_edge("repo_analyzer", "supervisor")
        workflow.add_edge("readme_writer", "supervisor")
        
        # Add conditional edges from supervisor
        def should_continue(state: GraphState) -> str:
            logger.info(f"should_continue called with state keys: {list(state.keys())}")
            
            # Get current workflow state
            decisions = state.get("decisions", [])
            validation = state.get("validation", {})
            decision = validation.get("decision", "continue")
            
            logger.info(f"Decision: {decision}, Number of decisions: {len(decisions)}")
            
            # Determine last agent from decisions
            last_agent = None
            if decisions:
                for dec in reversed(decisions):
                    agent_name = dec.get("agent", "")
                    if "RepoAnalyzer" in agent_name or "repo_analyzer" in agent_name:
                        last_agent = "repo_analyzer"
                        break
                    elif "ReadmeWriter" in agent_name or "readme_writer" in agent_name:
                        last_agent = "readme_writer"
                        break
            
            logger.info(f"Last agent: {last_agent}")
            
            if decision == "continue":
                if last_agent is None or last_agent == "repo_analyzer":
                    logger.info("Routing to readme_writer")
                    return "readme_writer"
                elif last_agent == "readme_writer":
                    logger.info("Workflow complete, routing to END")
                    return END
                else:
                    # Safety fallback
                    logger.warning(f"Unknown last agent: {last_agent}, defaulting to readme_writer")
                    return "readme_writer"
            else:
                # Redo the last agent
                logger.info(f"Redoing agent: {last_agent}")
                if last_agent == "repo_analyzer":
                    return "repo_analyzer"
                elif last_agent == "readme_writer":
                    return "readme_writer"
                else:
                    # Default fallback
                    logger.warning(f"Unknown agent for redo: {last_agent}, defaulting to repo_analyzer")
                    return "repo_analyzer"
                
        workflow.add_conditional_edges(
            "supervisor",
            should_continue,
            {
                "readme_writer": "readme_writer",
                "repo_analyzer": "repo_analyzer",
                END: END
            }
        )
        
        # Set entry point
        logger.info("Setting entry point to repo_analyzer...")
        workflow.set_entry_point("repo_analyzer")
        
        # Initialize memory saver for state persistence
        logger.info("Initializing memory saver...")
        memory_saver = MemorySaver()
        
        # Compile the graph with memory management
        logger.info("Compiling simplified graph...")
        app = workflow.compile(checkpointer=memory_saver)
        
        # Generate a unique thread ID for this run
        thread_id = state.get("repo_url", "").replace("/", "_").replace(":", "_").replace(".", "_")
        logger.info(f"Generated thread ID: {thread_id}")
        
        # Run the workflow with thread configuration
        logger.info("Starting simplified workflow execution...")
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50  # Much lower limit since we only have 2 agents
        }
        result = await app.ainvoke(state, config=config)
        logger.info("Simplified workflow execution completed")
        
        # Store the thread ID in the result for future reference
        result["thread_id"] = thread_id
        
        logger.info("Simplified LangGraph workflow completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in run_langgraph: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise 