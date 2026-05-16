"""Conversation history display component."""
import streamlit as st
from datetime import datetime


class HistoryPanel:
    """Displays conversation history."""
    
    @staticmethod
    def display(history: list) -> None:
        """
        Display conversation history.
        
        Args:
            history: List of history items
        """
        if not history:
            st.info("No conversation history yet.")
            return
        
        # Create tabs for different views
        view_tab1, view_tab2 = st.tabs(["📜 Timeline", "📊 Statistics"])
        
        with view_tab1:
            # Display history in reverse order (most recent first)
            for idx, item in enumerate(reversed(history), 1):
                HistoryPanel._display_item(item, idx, len(history))
        
        with view_tab2:
            HistoryPanel._display_statistics(history)
    
    @staticmethod
    def _display_item(item: dict, idx: int, total: int) -> None:
        """Display a single history item."""
        item_type = item.get("type", "unknown")
        timestamp = item.get("timestamp", datetime.now())
        
        col1, col2, col3 = st.columns([0.5, 3, 1])
        
        with col1:
            st.markdown(f"**{idx}/{total}**")
        
        with col2:
            if item_type == "text":
                text_input = item.get("input", "")
                st.markdown(f"""
                    <div class="history-item">
                        <strong>📝 Text Input</strong><br>
                        {text_input[:100]}{'...' if len(text_input) > 100 else ''}
                    </div>
                    """, unsafe_allow_html=True)
            
            elif item_type == "audio":
                st.markdown(f"""
                    <div class="history-item">
                        <strong>🎙️ Audio Input</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif item_type == "response":
                response_text = item.get("content", "")
                st.markdown(f"""
                    <div class="history-item" style="border-left-color: #28a745;">
                        <strong>✅ AI Response</strong><br>
                        {response_text[:100]}{'...' if len(response_text) > 100 else ''}
                    </div>
                    """, unsafe_allow_html=True)
        
        with col3:
            st.caption(timestamp.strftime('%H:%M:%S'))
    
    @staticmethod
    def _display_statistics(history: list) -> None:
        """Display conversation statistics."""
        stats = {
            "total_interactions": len(history),
            "text_inputs": 0,
            "audio_inputs": 0,
            "responses": 0
        }
        
        for item in history:
            item_type = item.get("type")
            if item_type == "text":
                stats["text_inputs"] += 1
            elif item_type == "audio":
                stats["audio_inputs"] += 1
            elif item_type == "response":
                stats["responses"] += 1
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Interactions", stats["total_interactions"])
        
        with col2:
            st.metric("Text Inputs", stats["text_inputs"])
        
        with col3:
            st.metric("Audio Inputs", stats["audio_inputs"])
        
        with col4:
            st.metric("Responses", stats["responses"])
        
        # Timeline visualization
        st.markdown("### Interaction Timeline")
        
        timeline_data = []
        for item in history:
            item_type = item.get("type")
            emoji = "📝" if item_type == "text" else "🎙️" if item_type == "audio" else "✅"
            timestamp = item.get("timestamp", datetime.now())
            timeline_data.append({
                "time": timestamp.strftime('%H:%M:%S'),
                "type": f"{emoji} {item_type.upper()}",
                "length": len(item.get("input", item.get("content", "")))
            })
        
        if timeline_data:
            st.dataframe(
                timeline_data,
                use_container_width=True,
                hide_index=True
            )
