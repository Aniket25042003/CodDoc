import os
import requests
import json
from typing import Dict, Any, Optional

class GeminiClient:
    """Simple Gemini API client to avoid LangChain serialization issues."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.0-flash-001"
    
    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate content using Gemini API directly."""
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
                "maxOutputTokens": 2048,
            }
        }
        
        params = {"key": self.api_key}
        
        try:
            response = requests.post(url, headers=headers, json=data, params=params)
            response.raise_for_status()
            
            result = response.json()
            
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]
            
            # Fallback if structure is different
            return "Error: Unable to parse response from Gemini API"
            
        except requests.exceptions.RequestException as e:
            return f"Error calling Gemini API: {str(e)}"
        except Exception as e:
            return f"Error processing Gemini response: {str(e)}" 