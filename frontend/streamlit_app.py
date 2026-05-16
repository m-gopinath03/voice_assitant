"""Main Streamlit application for Voice Agentic AI."""
import streamlit as st
import os
from datetime import datetime
from components.audio_recorder import AudioRecorder
from components.response_panel import ResponsePanel
from components.history_panel import HistoryPanel
from services.api_client import APIClient
from utils.chroma_client import ChromaMemoryClient

# Page configuration
st.set_page_config(
    page_title="Voice Agentic AI",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .stAudio {
        margin: 10px 0;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .history-item {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 4px solid #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(datetime.now().timestamp())
if "user_id" not in st.session_state:
    st.session_state.user_id = "default_user"
if "history" not in st.session_state:
    st.session_state.history = []
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
if "chroma_client" not in st.session_state:
    st.session_state.chroma_client = ChromaMemoryClient()

# Header
st.markdown("# 🎤 Voice Agentic AI Assistant")
st.markdown("*Intelligent voice assistant with memory and context awareness*")
st.divider()

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Configuration
    api_url = st.text_input(
        "API Base URL",
        value=os.getenv("API_BASE_URL", "http://localhost:8000"),
        help="Backend API URL"
    )
    
    # User Configuration
    st.session_state.user_id = st.text_input(
        "User ID",
        value=st.session_state.user_id,
        help="Unique identifier for memory context"
    )
    
    # Settings
    st.markdown("### Voice Settings")
    generate_speech = st.checkbox("Generate speech response", value=True)
    enable_memory = st.checkbox("Enable memory/RAG", value=True)
    
    # Memory Management
    st.markdown("### 📚 Memory Management")
    if st.button("🗑️ Clear Conversation History"):
        st.session_state.history = []
        st.session_state.conversation_id = str(datetime.now().timestamp())
        st.success("History cleared!")
    
    if st.button("🔄 Refresh Memory Index"):
        try:
            st.session_state.chroma_client.rebuild_index()
            st.success("Memory index rebuilt!")
        except Exception as e:
            st.error(f"Error rebuilding index: {str(e)}")
    
    # Stats
    st.markdown("### 📊 Statistics")
    st.metric("Interactions", len(st.session_state.history))
    st.metric("Conversation ID", st.session_state.conversation_id[:8])
    
    # About
    st.markdown("---")
    st.markdown("""
    ### About
    **Voice Agentic AI** is an intelligent voice assistant powered by:
    - 🤖 CrewAI for agent orchestration
    - 🧠 Gemini for LLM capabilities
    - 📝 ChromaDB for memory/RAG
    - 🎙️ Speech-to-Text & Text-to-Speech
    """)

# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎙️ Input")
    
    # Text Input Tab
    input_tab1, input_tab2 = st.tabs(["📝 Text", "🎵 Audio"])
    
    with input_tab1:
        user_text = st.text_area(
            "Enter your message:",
            placeholder="Type your question or command here...",
            height=100,
            key="text_input"
        )
        
        if st.button("📤 Process Text", use_container_width=True):
            if user_text.strip():
                with st.spinner("Processing..."):
                    try:
                        # Add to history
                        st.session_state.history.append({
                            "type": "text",
                            "input": user_text,
                            "timestamp": datetime.now()
                        })
                        
                        # Call API
                        response = st.session_state.api_client.process_text(
                            text=user_text,
                            generate_speech=generate_speech,
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.conversation_id
                        )
                        
                        # Store in ChromaDB if memory enabled
                        if enable_memory:
                            st.session_state.chroma_client.add_to_memory(
                                text=user_text,
                                response=response.get("response", ""),
                                user_id=st.session_state.user_id,
                                metadata={"type": "text_input"}
                            )
                        
                        # Add response to history
                        st.session_state.history.append({
                            "type": "response",
                            "content": response.get("response", ""),
                            "audio": response.get("audio"),
                            "timestamp": datetime.now()
                        })
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter some text first.")
    
    with input_tab2:
        st.info("🎵 Audio input via microphone or upload")

        audio_recorder = AudioRecorder()

        col_rec, col_up = st.columns([1, 1])

        with col_rec:
            st.markdown("**Record from microphone**")
            recorded_audio = audio_recorder.record_audio()

        with col_up:
            st.markdown("**Or upload an audio file**")
            uploaded_file = st.file_uploader(
                "Upload audio file",
                type=["wav", "mp3", "m4a", "ogg", "flac"],
                accept_multiple_files=False,
                key="audio_uploader"
            )
            uploaded_bytes = None
            uploaded_mime = None
            uploaded_name = None
            if uploaded_file is not None:
                uploaded_bytes = uploaded_file.read()
                uploaded_mime = getattr(uploaded_file, "type", None)
                uploaded_name = getattr(uploaded_file, "name", "uploaded_audio")

        # Choose which audio to process (uploaded takes precedence)
        audio_to_process = None
        audio_format = None
        if uploaded_bytes:
            audio_to_process = uploaded_bytes
            audio_format = uploaded_mime
            st.audio(uploaded_bytes, format=audio_format)
        elif recorded_audio is not None:
            audio_to_process = recorded_audio
            audio_format = "audio/wav"
            st.audio(recorded_audio, format=audio_format)

        if audio_to_process is not None:
            if st.button("📤 Process Audio", use_container_width=True, key="process_audio"):
                with st.spinner("Transcribing and processing..."):
                    try:
                        # Add to history
                        st.session_state.history.append({
                            "type": "audio",
                            "timestamp": datetime.now()
                        })

                        # Call API (pass filename and mime when available)
                        response = st.session_state.api_client.process_audio(
                            audio_data=audio_to_process,
                            generate_speech=generate_speech,
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.conversation_id,
                            filename=uploaded_name if uploaded_bytes else "recording.wav",
                            mime_type=audio_format,
                        )

                        # Store in ChromaDB if memory enabled
                        if enable_memory and "transcribed_text" in response:
                            st.session_state.chroma_client.add_to_memory(
                                text=response.get("transcribed_text", ""),
                                response=response.get("response", ""),
                                user_id=st.session_state.user_id,
                                metadata={"type": "audio_input"}
                            )

                        # Add response to history
                        st.session_state.history.append({
                            "type": "response",
                            "content": response.get("response", ""),
                            "audio": response.get("audio"),
                            "timestamp": datetime.now()
                        })

                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

with col2:
    st.markdown("### 📤 Response")
    
    if st.session_state.history:
        # Get the last response
        response_item = None
        for item in reversed(st.session_state.history):
            if item.get("type") == "response":
                response_item = item
                break
        
        if response_item:
            response_panel = ResponsePanel()
            response_panel.display(response_item)
    else:
        st.info("👋 No responses yet. Start by entering text or recording audio!")
    
    # Memory Insights
    if enable_memory:
        st.markdown("### 🧠 Memory Insights")
        
        try:
            # Get similar memories
            if st.session_state.history:
                last_input = None
                for item in reversed(st.session_state.history):
                    if item.get("type") in ["text", "response"]:
                        last_input = item
                        break
                
                if last_input and last_input.get("type") == "response":
                    similar = st.session_state.chroma_client.search(
                        query=last_input.get("content", "")[:200],
                        k=3,
                        user_id=st.session_state.user_id
                    )
                    
                    if similar:
                        with st.expander("📚 Similar past interactions"):
                            for idx, result in enumerate(similar, 1):
                                st.markdown(f"**{idx}. Similar memory:**")
                                st.text(result)
                                st.divider()
        except Exception as e:
            st.warning(f"Memory retrieval: {str(e)}")

# Conversation History Panel
st.divider()
st.markdown("### 💬 Conversation History")

history_panel = HistoryPanel()
history_panel.display(st.session_state.history)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; padding: 20px;">
        <p>🚀 Voice Agentic AI | Powered by CrewAI, Gemini, and ChromaDB</p>
        <p>Session: {0} | User: {1}</p>
    </div>
    """.format(
        st.session_state.conversation_id[:8],
        st.session_state.user_id
    ), unsafe_allow_html=True)
