import os
import requests
import json
import time
from typing import Dict, Any, Optional

class GeminiClient:
    """Simple Gemini API client to avoid LangChain serialization issues."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.0-flash-lite"
        self.max_retries = 2  # Reduced retries for faster failure
        self.base_delay = 1  # Reduced delay
    
    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate content using Gemini API directly with retry logic."""
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 1024,  # Reduced for faster response
            }
        }
        
        params = {"key": self.api_key}
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, params=params, timeout=30)  # 30 second timeout
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limit hit, waiting {retry_delay} seconds before retry {attempt + 1}/{self.max_retries}")
                    time.sleep(retry_delay)
                    continue
                
                response.raise_for_status()
                
                result = response.json()
                
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        return candidate["content"]["parts"][0]["text"]
                
                # Fallback if structure is different
                return "Error: Unable to parse response from Gemini API"
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    return f"Error calling Gemini API after {self.max_retries} attempts: {str(e)}"
                
                # Wait before retrying
                retry_delay = self.base_delay * (2 ** attempt)
                print(f"Request failed, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(retry_delay)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Error processing Gemini response after {self.max_retries} attempts: {str(e)}"
                
                retry_delay = self.base_delay * (2 ** attempt)
                time.sleep(retry_delay)
        
        return "Error: Failed to get response after all retries" 