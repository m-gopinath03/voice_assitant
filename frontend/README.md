# Voice Assistant Frontend

Complete Streamlit frontend for the Voice Agentic AI system with ChromaDB integration.

## Features

✨ **Core Features**
- 🎤 Audio recording and playback
- 📝 Text input processing
- 🎙️ Speech-to-Text support
- 🔊 Text-to-Speech response generation
- 💬 Conversation history tracking
- 🧠 ChromaDB memory/RAG integration
- 📊 Conversation statistics

## Architecture

```
Frontend (Streamlit)
    ↓
API Client
    ↓
FastAPI Backend
    ↓
CrewAI Agent
    ↓
ChromaDB Memory
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
API_BASE_URL=http://localhost:8000
ENABLE_MEMORY_RAG=true
```

### 3. Run Frontend

```bash
streamlit run streamlit_app.py
```

Frontend will open at `http://localhost:8501`

## Components

### 📁 Structure

```
frontend/
├── streamlit_app.py           # Main Streamlit application
├── components/
│   ├── audio_recorder.py      # Audio recording component
│   ├── response_panel.py      # Response display component
│   └── history_panel.py       # Conversation history component
├── services/
│   └── api_client.py          # Backend API client
├── utils/
│   └── chroma_client.py       # ChromaDB memory client
└── requirements.txt           # Frontend dependencies
```

### 🎙️ Audio Recorder Component

Handles audio input via microphone:
- Real-time recording
- WAV format support
- Fallback method support

Usage:
```python
from components.audio_recorder import AudioRecorder

recorder = AudioRecorder(sample_rate=16000, duration=10)
audio_data = recorder.record_audio()
```

### 📤 Response Panel Component

Displays AI responses with formatting:
- Text response display
- Audio playback
- Response copying/saving

Usage:
```python
from components.response_panel import ResponsePanel

panel = ResponsePanel()
panel.display(response_item)
```

### 💬 History Panel Component

Shows conversation history:
- Timeline view
- Statistics view
- Interaction metrics

Usage:
```python
from components.history_panel import HistoryPanel

panel = HistoryPanel()
panel.display(history_list)
```

### 🔌 API Client

Communicates with FastAPI backend:

```python
from services.api_client import APIClient

client = APIClient(base_url="http://localhost:8000")

# Process text
response = client.process_text(
    text="Hello, how are you?",
    generate_speech=True,
    user_id="user123"
)

# Process audio
response = client.process_audio(
    audio_data=audio_bytes,
    generate_speech=True,
    user_id="user123"
)

# Get history
history = client.get_history(conversation_id="conv123")

# Health check
is_healthy = client.health_check()
```

### 🧠 ChromaDB Memory Client

Easy vector database integration:

```python
from utils.chroma_client import ChromaMemoryClient

chroma = ChromaMemoryClient()

# Add to memory
chroma.add_to_memory(
    text="User input",
    response="AI response",
    user_id="user123",
    metadata={"type": "text_input"}
)

# Search memory
similar = chroma.search(
    query="similar query",
    k=3,
    user_id="user123"
)

# Get all memories
all_memories = chroma.get_all_memories(user_id="user123")

# Get statistics
stats = chroma.get_memory_stats(user_id="user123")

# Clear user memories
chroma.clear_user_memories(user_id="user123")

# Rebuild index
chroma.rebuild_index()
```

## Workflow

### Text Input Flow
```
User enters text
    ↓
Process Text button clicked
    ↓
API client sends to backend
    ↓
Backend processes via CrewAI
    ↓
Response received
    ↓
Stored in ChromaDB (if enabled)
    ↓
Display response + audio (if enabled)
```

### Audio Input Flow
```
User records audio
    ↓
Process Audio button clicked
    ↓
Audio sent to backend
    ↓
Backend transcribes + processes
    ↓
Response generated
    ↓
Stored in ChromaDB
    ↓
Display response + audio
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| API_BASE_URL | http://localhost:8000 | Backend API URL |
| ENABLE_MEMORY_RAG | true | Enable ChromaDB memory |
| ENABLE_SPEECH_RESPONSE | true | Generate audio responses |
| ENABLE_AUDIO_INPUT | true | Enable audio recording |
| CHROMA_DB_PATH | ~/.voice_assistant | ChromaDB storage path |

## UI Features

### Sidebar
- API configuration
- User ID management
- Voice settings
- Memory controls
- Statistics

### Main View
- Text input tab
- Audio input tab
- Response display
- Memory insights

### History Panel
- Timeline view
- Interaction statistics
- Interaction metrics

## Error Handling

All components include error handling:
- API connection errors
- Audio recording errors
- ChromaDB errors
- Invalid input validation

Errors are displayed as Streamlit alerts.

## Performance Tips

1. **Memory Management**
   - Regularly clear old memories
   - Use user_id filtering for searches
   - Rebuild index periodically

2. **API Optimization**
   - Set appropriate timeouts
   - Use connection pooling
   - Cache responses when possible

3. **UI Responsiveness**
   - Use session state efficiently
   - Minimize reruns
   - Cache expensive computations

## Troubleshooting

### ChromaDB Connection Issues
```python
# Rebuild index
chroma_client.rebuild_index()

# Check stats
stats = chroma_client.get_memory_stats()
```

### API Connection Errors
```python
# Check backend health
is_healthy = api_client.health_check()

# Verify API URL
api_url = os.getenv("API_BASE_URL")
```

### Audio Recording Issues
```python
# Check microphone permissions
# Use fallback recording method
# Verify audio format (WAV)
```

## Future Enhancements

- 📊 Advanced analytics dashboard
- 🔍 Full-text search in memory
- 🎯 Intent classification UI
- 📈 Memory visualization
- 🔐 User authentication
- 🌍 Multi-language support
- 📱 Mobile-responsive design

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend Framework | Streamlit |
| Audio Input | streamlit-audio-recorder |
| Audio Processing | librosa, sounddevice |
| API Client | requests |
| Vector DB | ChromaDB |
| Embeddings | Sentence Transformers |

## License

MIT License

## Support

For issues or questions:
1. Check error messages in Streamlit console
2. Review ChromaDB logs
3. Verify backend is running
4. Check configuration in `.env`
