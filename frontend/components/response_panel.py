"""Response display component."""
import streamlit as st
from datetime import datetime
import base64


class ResponsePanel:
    """Displays AI responses with formatting and audio playback."""
    
    @staticmethod
    def display(response_item: dict) -> None:
        """
        Display a response item.
        
        Args:
            response_item: Dictionary containing response data
        """
        if not response_item:
            return
        
        # Response content
        response_text = response_item.get("content", "")
        
        if response_text:
            st.markdown(
                f"""
                <div class="response-box">
                    <p><strong>Assistant Response:</strong></p>
                    <p>{response_text}</p>
                    <small style="color: #666;">
                        {response_item.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}
                    </small>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Audio playback
        audio_data = response_item.get("audio")
        if audio_data:
            st.markdown("**🔊 Audio Response:**")
            st.audio(audio_data, format="audio/wav")
        
        # Copy response button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Response", use_container_width=True):
                st.write(response_text)
                st.success("Response copied to clipboard!")
        
        with col2:
            if st.button("💾 Save Response", use_container_width=True):
                # Save to file
                timestamp = response_item.get('timestamp', datetime.now()).strftime('%Y%m%d_%H%M%S')
                filename = f"response_{timestamp}.txt"
                
                with open(filename, 'w') as f:
                    f.write(response_text)
                
                st.success(f"Response saved to {filename}")
