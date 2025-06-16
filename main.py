from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import traceback
import logging
from dotenv import load_dotenv
from langgraph_app.tools.git_utils import clone_repo
from langgraph_app.agents.repo_analyzer import RepoAnalyzerAgent
from langgraph_app.agents.readme_writer import ReadmeWriterAgent

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
        
        # Initialize simplified state
        state = {
            "repo_url": request.repo_url,
            "repo_path": repo_path,
            "repo_structure": {},
            "dependencies": {},
            "sample_files": {},
            "repo_analysis": {},
            "readme": "",
            "log": [],
            "decisions": []
        }
        
        logger.info("Starting simplified workflow...")
        
        # Step 1: Analyze repository
        logger.info("Running repo analyzer...")
        repo_analyzer = RepoAnalyzerAgent()
        state = repo_analyzer.process(state)
        logger.info("Repo analysis completed")
        
        # Step 2: Generate README
        logger.info("Running readme writer...")
        readme_writer = ReadmeWriterAgent()
        state = readme_writer.process(state)
        logger.info("README generation completed")
        
        # Clean up
        try:
            from langgraph_app.tools.git_utils import cleanup_repo
            cleanup_repo(repo_path)
        except:
            pass
        
        return ReadmeResponse(
            readme=state.get("readme", ""),
            log=state.get("log", []),
            decisions=state.get("decisions", []),
            thread_id="simplified_workflow"
        )
        
    except Exception as e:
        logger.error(f"Error in generate_readme: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 