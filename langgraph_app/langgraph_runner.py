from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging
import traceback
from .agents.repo_analyzer import RepoAnalyzerAgent
from .agents.dependency_extractor import DependencyExtractorAgent
from .agents.code_understanding import CodeUnderstandingAgent
from .agents.docstring_summarizer import DocstringSummarizerAgent
from .agents.readme_writer import ReadmeWriterAgent
from .agents.supervisor_agent import SupervisorAgent

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    """State schema for the LangGraph workflow."""
    repo_url: str
    repo_path: str
    repo_structure: Dict[str, Any]
    dependencies: Dict[str, Any]
    important_files: List[str]
    code_summaries: Dict[str, str]
    doc_summaries: Dict[str, str]
    readme: str
    log: List[str]
    decisions: List[Dict[str, Any]]
    current_agent: str
    validation: Dict[str, Any]

async def run_langgraph(state: Dict[str, Any]) -> Dict[str, Any]:
    """Run the LangGraph workflow for README generation."""
    
    try:
        logger.info("Initializing agents...")
        # Initialize agents
        repo_analyzer = RepoAnalyzerAgent()
        dependency_extractor = DependencyExtractorAgent()
        code_understanding = CodeUnderstandingAgent()
        docstring_summarizer = DocstringSummarizerAgent()
        readme_writer = ReadmeWriterAgent()
        supervisor = SupervisorAgent()
        logger.info("All agents initialized successfully")
        
        # Create the graph with proper state schema
        logger.info("Creating StateGraph...")
        workflow = StateGraph(GraphState)
        
        # Define nodes
        logger.info("Adding nodes to graph...")
        workflow.add_node("repo_analyzer", repo_analyzer.process)
        workflow.add_node("dependency_extractor", dependency_extractor.process)
        workflow.add_node("code_understanding", code_understanding.process)
        workflow.add_node("docstring_summarizer", docstring_summarizer.process)
        workflow.add_node("readme_writer", readme_writer.process)
        workflow.add_node("supervisor", supervisor.process)
        
        # Define edges
        logger.info("Adding edges to graph...")
        workflow.add_edge("repo_analyzer", "supervisor")
        workflow.add_edge("dependency_extractor", "supervisor")
        workflow.add_edge("code_understanding", "supervisor")
        workflow.add_edge("docstring_summarizer", "supervisor")
        workflow.add_edge("readme_writer", "supervisor")
        
        # Add conditional edges from supervisor
        def should_continue(state: GraphState) -> str:
            logger.info(f"should_continue called with state keys: {list(state.keys())}")
            
            # Get the last agent that was executed (not supervisor)
            decisions = state.get("decisions", [])
            current_agent = state.get("current_agent", "")
            validation = state.get("validation", {})
            decision = validation.get("decision", "continue")
            
            logger.info(f"Current agent: {current_agent}, Decision: {decision}")
            logger.info(f"Number of decisions made: {len(decisions)}")
            
            # Determine what was the last actual work agent (not supervisor)
            last_work_agent = None
            if decisions:
                # Find the most recent non-supervisor agent
                for dec in reversed(decisions):
                    agent_name = dec.get("agent", "")
                    # Handle both class names and simple names, exclude supervisor variants
                    if agent_name not in ["supervisor", "SupervisorAgent"]:
                        # Normalize class names to simple names
                        if agent_name == "RepoAnalyzerAgent":
                            last_work_agent = "repo_analyzer"
                        elif agent_name == "DependencyExtractorAgent":
                            last_work_agent = "dependency_extractor"
                        elif agent_name == "CodeUnderstandingAgent":
                            last_work_agent = "code_understanding"
                        elif agent_name == "DocstringSummarizerAgent":
                            last_work_agent = "docstring_summarizer"
                        elif agent_name == "ReadmeWriterAgent":
                            last_work_agent = "readme_writer"
                        else:
                            last_work_agent = agent_name  # Use as-is if already simple name
                        break
            
            logger.info(f"Last work agent: {last_work_agent}")
            
            if decision == "continue":
                # Determine next agent based on workflow sequence
                if last_work_agent is None or last_work_agent == "repo_analyzer":
                    logger.info("Routing to dependency_extractor")
                    return "dependency_extractor"
                elif last_work_agent == "dependency_extractor":
                    logger.info("Routing to code_understanding")
                    return "code_understanding"
                elif last_work_agent == "code_understanding":
                    logger.info("Routing to docstring_summarizer")
                    return "docstring_summarizer"
                elif last_work_agent == "docstring_summarizer":
                    logger.info("Routing to readme_writer")
                    return "readme_writer"
                elif last_work_agent == "readme_writer":
                    logger.info("Workflow complete, routing to END")
                    return END
                else:
                    # Default case - check if we've been looping and break the cycle
                    if len(decisions) > 10:  # If we have many decisions, likely stuck in loop
                        logger.error(f"Too many decisions ({len(decisions)}), ending workflow to prevent infinite loop")
                        return END
                    # Default case - start workflow
                    logger.warning(f"Unknown last work agent: {last_work_agent}, starting workflow with dependency_extractor")
                    return "dependency_extractor"
            else:
                # Redo the last work agent
                logger.info(f"Redoing agent: {last_work_agent}")
                if last_work_agent == "repo_analyzer":
                    return "repo_analyzer"
                elif last_work_agent == "dependency_extractor":
                    return "dependency_extractor"
                elif last_work_agent == "code_understanding":
                    return "code_understanding"
                elif last_work_agent == "docstring_summarizer":
                    return "docstring_summarizer"
                elif last_work_agent == "readme_writer":
                    return "readme_writer"
                else:
                    # Default fallback
                    logger.warning(f"Unknown agent for redo: {last_work_agent}, defaulting to repo_analyzer")
                    return "repo_analyzer"
                
        workflow.add_conditional_edges(
            "supervisor",
            should_continue,
            {
                "dependency_extractor": "dependency_extractor",
                "code_understanding": "code_understanding",
                "docstring_summarizer": "docstring_summarizer",
                "readme_writer": "readme_writer",
                "repo_analyzer": "repo_analyzer",
                END: END
            }
        )
        
        # Set entry point
        logger.info("Setting entry point...")
        workflow.set_entry_point("repo_analyzer")
        
        # Initialize memory saver for state persistence
        logger.info("Initializing memory saver...")
        memory_saver = MemorySaver()
        
        # Compile the graph with memory management
        logger.info("Compiling graph...")
        app = workflow.compile(checkpointer=memory_saver)
        
        # Generate a unique thread ID for this run
        thread_id = state.get("repo_url", "").replace("/", "_").replace(":", "_").replace(".", "_")
        logger.info(f"Generated thread ID: {thread_id}")
        
        # Run the workflow with thread configuration and increased recursion limit
        logger.info("Starting workflow execution...")
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 500  # Increased limit for complex multi-agent workflow
        }
        result = await app.ainvoke(state, config=config)
        logger.info("Workflow execution completed")
        
        # Store the thread ID in the result for future reference
        result["thread_id"] = thread_id
        
        logger.info("LangGraph workflow completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in run_langgraph: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise 