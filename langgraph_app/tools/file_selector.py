import os
from typing import List, Set
from pathlib import Path

# File extensions to analyze
CODE_EXTENSIONS = {
    '.py', '.js', '.java', '.cpp', '.c', '.h', '.hpp', 
    '.ts', '.tsx', '.jsx', '.rb', '.php', '.go', '.rs'
}

# Directories to exclude
EXCLUDED_DIRS = {
    'tests', 'test', '__tests__', '.git', 'node_modules',
    'venv', 'env', '.venv', '.env', 'dist', 'build',
    'coverage', '.github', 'docs', 'examples'
}

def is_important_file(file_path: str, min_lines: int = 15) -> bool:
    """
    Determine if a file is important based on its characteristics.
    
    Args:
        file_path (str): Path to the file
        min_lines (int): Minimum number of lines for a file to be considered important
        
    Returns:
        bool: True if the file is important, False otherwise
    """
    try:
        # Check if file has a relevant extension
        if not any(file_path.endswith(ext) for ext in CODE_EXTENSIONS):
            return False
            
        # Check if file is in an excluded directory
        path = Path(file_path)
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            return False
            
        # Check file size and line count
        with open(file_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
            return line_count >= min_lines
            
    except Exception:
        return False

def select_important_files(repo_path: str) -> List[str]:
    """
    Select important files from the repository.
    
    Args:
        repo_path (str): Path to the repository
        
    Returns:
        List[str]: List of paths to important files
    """
    important_files = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_important_file(file_path):
                important_files.append(file_path)
                
    return important_files 