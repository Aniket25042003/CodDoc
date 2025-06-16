import os
import tempfile
from git import Repo
from typing import Optional

def clone_repo(repo_url: str) -> str:
    """
    Clone a git repository to a temporary directory.
    
    Args:
        repo_url (str): The URL of the git repository to clone
        
    Returns:
        str: Path to the cloned repository
        
    Raises:
        Exception: If cloning fails
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Clone the repository
        Repo.clone_from(repo_url, temp_dir)
        
        return temp_dir
    except Exception as e:
        raise Exception(f"Failed to clone repository: {str(e)}")

def cleanup_repo(repo_path: str) -> None:
    """
    Clean up the cloned repository directory.
    
    Args:
        repo_path (str): Path to the repository directory
    """
    try:
        import shutil
        shutil.rmtree(repo_path)
    except Exception as e:
        print(f"Warning: Failed to cleanup repository: {str(e)}") 