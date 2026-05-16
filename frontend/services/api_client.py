"""API client for communicating with backend."""
import os
import requests
from typing import Optional, Dict, Any
import streamlit as st
from io import BytesIO


class APIClient:
    """Client for backend API calls."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Backend API base URL
        """
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.api_v1_prefix = f"{self.base_url}/api/v1"
    
    def process_text(
        self,
        text: str,
        generate_speech: bool = True,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process text input.
        
        Args:
            text: Input text
            generate_speech: Whether to generate speech response
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            Response dictionary
        """
        try:
            payload = {
                "text": text,
                "generate_speech": generate_speech,
                "user_id": user_id,
                "session_id": session_id
            }
            
            response = requests.post(
                f"{self.api_v1_prefix}/process",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"response": f"Error: {str(e)}", "status": "error"}
    
    def process_audio(
        self,
        audio_data: bytes,
        generate_speech: bool = True,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        filename: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process audio input.
        
        Args:
            audio_data: Audio data in bytes
            generate_speech: Whether to generate speech response
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            Response dictionary
        """
        try:
            # Prepare file object
            if isinstance(audio_data, bytes):
                fileobj = BytesIO(audio_data)
            else:
                # If file-like object (fallback), try to wrap
                fileobj = BytesIO(audio_data)

            # Use provided filename/mime if given, otherwise defaults
            filename = filename or getattr(audio_data, "name", "audio.wav")
            mime = mime_type or getattr(audio_data, "type", None) or "audio/wav"

            files = {"file": (filename, fileobj, mime)}
            data = {
                "generate_speech": generate_speech,
                "user_id": user_id,
                "session_id": session_id
            }
            
            response = requests.post(
                f"{self.api_v1_prefix}/process",
                files=files,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"response": f"Error: {str(e)}", "status": "error"}
    
    def get_history(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get conversation history.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            History data
        """
        try:
            response = requests.get(
                f"{self.api_v1_prefix}/history/{conversation_id}",
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """
        Check backend health.
        
        Returns:
            True if backend is healthy
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        
        except requests.exceptions.RequestException:
            return False
