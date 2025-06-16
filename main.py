from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import traceback
import logging
from dotenv import load_dotenv
from langgraph_app.langgraph_runner import run_langgraph
from langgraph_app.tools.git_utils import clone_repo
from langgraph.checkpoint.memory import MemorySaver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI README Generator",
    description="Generate comprehensive README.md files using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize memory saver
memory_saver = MemorySaver()

class RepoRequest(BaseModel):
    repo_url: str

class ReadmeResponse(BaseModel):
    readme: str
    log: List[str]
    decisions: List[Dict]
    thread_id: str

@app.post("/generate-readme", response_model=ReadmeResponse)
async def generate_readme(request: RepoRequest):
    try:
        logger.info(f"Received request for repo: {request.repo_url}")
        
        # Validate API key
        if not os.getenv("GEMINI_API_KEY"):
            logger.error("GEMINI_API_KEY not found in environment")
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable is required")
        
        # Clone the repository
        logger.info("Cloning repository...")
        repo_path = clone_repo(request.repo_url)
        logger.info(f"Repository cloned to: {repo_path}")
        
        # Initialize state
        state = {
            "repo_url": request.repo_url,
            "repo_path": repo_path,
            "repo_structure": {},
            "dependencies": {},
            "important_files": [],
            "code_summaries": {},
            "doc_summaries": {},
            "readme": "",
            "log": [],
            "decisions": []
        }
        
        logger.info("Starting LangGraph workflow...")
        # Run the LangGraph workflow
        result = await run_langgraph(state)
        logger.info("LangGraph workflow completed successfully")
        
        return ReadmeResponse(
            readme=result.get("readme", ""),
            log=result.get("log", []),
            decisions=result.get("decisions", []),
            thread_id=result.get("thread_id", "")
        )
        
    except Exception as e:
        logger.error(f"Error in generate_readme: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/readme/{thread_id}", response_model=ReadmeResponse)
async def get_readme(thread_id: str):
    """Retrieve a previously generated README using its thread ID."""
    try:
        # Get the state from memory
        state = memory_saver.get(thread_id)
        if not state:
            raise HTTPException(status_code=404, detail="README not found")
            
        return ReadmeResponse(
            readme=state["readme"],
            log=state["log"],
            decisions=state["decisions"],
            thread_id=thread_id
        )
        
    except Exception as e:
        logger.error(f"Error in get_readme: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "api_key_configured": bool(os.getenv("GEMINI_API_KEY"))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000))) 