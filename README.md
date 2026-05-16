# Voice Agentic AI

A production-ready voice assistant with CrewAI orchestration, ChromaDB memory, and Streamlit UI.

## 🚀 Quick Start

### One-Command Setup
```bash
python quickstart.py
```

### Manual Setup

**Backend:**
```bash
cd voice_assitant/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend** (new terminal):
```bash
cd voice_assitant/frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Access:**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 📋 Architecture Overview

```
                ┌────────────────────┐
                │  Streamlit UI      │
                │  (Frontend)        │
                └─────────┬──────────┘
                          │
                ┌─────────▼──────────┐
                │   API Client       │
                │   (requests)       │
                └─────────┬──────────┘
                          │
                ┌─────────▼──────────────────────────┐
                │     FastAPI Backend                │
                │  (/api/v1/process)                 │
                └─────────┬──────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
    STT Service      Intent Classifier    Memory Service
    (Speech to       (Pydantic Output)    (ChromaDB Search)
     Text)                                    
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                ┌─────────▼──────────────────┐
                │   CrewAI Parent Agent      │
                │  (Orchestrator)            │
                └─────────┬──────────────────┘
                          │
        ┌─────────────────┼──────────────────┬────────────┐
        │                 │                  │            │
        ▼                 ▼                  ▼            ▼
    Save Tool       Summary Tool       Search Tool    Memory Tool
    (CSV Store)     (Summarize)        (History)      (RAG)
        │                 │                  │            │
        └─────────────────┼──────────────────┴────────────┘
                          │
                ┌─────────▼──────────────────┐
                │   Gemini LLM Response      │
                │   (google-generativeai)    │
                └─────────┬──────────────────┘
                          │
                ┌─────────▼──────────────────┐
                │   CSV Persistence         │
                │  (parent_conversations)   │
                │  (child_context)          │
                └─────────┬──────────────────┘
                          │
                ┌─────────▼──────────────────┐
                │   TTS Service              │
                │  (gTTS)         │
                └────────────────────────────┘
```

## 🎯 Core Features

| Feature | Implementation | Purpose |
|---------|-----------------|---------|
| **Voice Input** | SpeechRecognition | Convert speech to text |
| **Agent Orchestration** | CrewAI | Manage workflow and tools |
| **Tool Calling** | Dynamic tools | Save, summarize, search |
| **Memory/RAG** | ChromaDB | Context awareness |
| **LLM** | Gemini Flash | Response generation |
| **Persistence** | CSV | Data storage |
| **Speech Output** | pyttsx3 | Text to speech |
| **Frontend** | Streamlit | User interface |

## 📁 Project Structure

```
voice_assitant/
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── api/
│   │   │   └── routes.py           # API endpoints
│   │   ├── core/
│   │   │   ├── config.py           # Configuration
│   │   │   ├── logger.py           # Logging setup
│   │   │   └── constants.py        # Constants
│   │   ├── crew/
│   │   │   ├── crew_setup.py       # CrewAI setup
│   │   │   ├── agents.py           # Parent agent
│   │   │   ├── tasks.py            # Agent tasks
│   │   │   └── tools/              # Dynamic tools
│   │   ├── models/
│   │   │   ├── intent_model.py     # Intent classification
│   │   │   ├── request_model.py    # Request schemas
│   │   │   └── response_model.py   # Response schemas
│   │   ├── services/
│   │   │   ├── stt_service.py      # Speech to text
│   │   │   ├── tts_service.py      # Text to speech
│   │   │   ├── llm_service.py      # LLM integration
│   │   │   ├── rag_service.py      # RAG operations
│   │   │   ├── csv_service.py      # CSV operations
│   │   │   └── memory_service.py   # Memory management
│   │   ├── rag/
│   │   │   ├── embeddings.py       # Embedding functions
│   │   │   └── retriever.py        # Retrieval logic
│   │   ├── utils/
│   │   │   ├── validators.py       # Data validation
│   │   │   ├── file_utils.py       # File operations
│   │   │   └── regex_utils.py      # Regex utilities
│   │   ├── data/
│   │   │   ├── parent_conversations.csv
│   │   │   └── child_context.csv
│   │   └── prompts/
│   │       └── system_prompt.txt
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py           # Main Streamlit app
│   ├── components/
│   │   ├── audio_recorder.py      # Audio input
│   │   ├── response_panel.py      # Response display
│   │   └── history_panel.py       # History view
│   ├── services/
│   │   └── api_client.py          # API communication
│   ├── utils/
│   │   └── chroma_client.py       # ChromaDB integration
│   ├── config.py                  # Configuration
│   └── requirements.txt
│
└── docs/
    ├── ARCHITECTURE.md            # Architecture details
    └── API.md                      # API documentation
```

## 🔌 API Endpoints

### Process Audio/Text
```http
POST /api/v1/process
Content-Type: application/json

{
  "text": "User input",
  "generate_speech": true,
  "user_id": "user123",
  "session_id": "session123"
}
```

### Transcribe Audio
```http
POST /api/v1/transcribe
Content-Type: multipart/form-data

file: <audio.wav>
```

### Get History
```http
GET /api/v1/history/{conversation_id}
```

### Health Check
```http
GET /health
```

## 🧠 Memory/RAG System

### ChromaDB Integration

The system uses ChromaDB for lightweight vector storage:

```python
from utils.chroma_client import ChromaMemoryClient

# Initialize
chroma = ChromaMemoryClient()

# Add to memory
chroma.add_to_memory(
    text="User input",
    response="AI response",
    user_id="user123",
    metadata={"type": "text"}
)

# Search similar
similar = chroma.search("query", k=3, user_id="user123")

# Get statistics
stats = chroma.get_memory_stats(user_id="user123")
```

### Data Flow

1. **User Input** → Converted to embeddings
2. **Storage** → Stored in ChromaDB with metadata
3. **Retrieval** → Similar memories retrieved based on query
4. **Context Injection** → Memories passed to Gemini prompt
5. **Response** → AI generates contextual response

## 🚦 Workflow

### Text Processing Flow
```
Input Text
    ↓
Intent Classification (Pydantic)
    ↓
CrewAI Agent receives intent
    ↓
Tool selection based on intent
    ↓
Memory retrieval (if needed)
    ↓
Tool execution (save/search/summarize)
    ↓
Gemini generates response
    ↓
CSV update (persistence)
    ↓
TTS generation (optional)
    ↓
Response to user
```

### Audio Processing Flow
```
Audio File
    ↓
STT Transcription
    ↓
[Same as Text Processing Flow]
```

## 📊 CSV Storage Design

### Parent Conversations (Main Table)
```csv
conversation_id,user_input,intent,response,timestamp
conv_001,What's the plan?,QUERY,Here's the summary...,2024-01-01T10:00:00
```

### Child Context (Metadata Table)
```csv
conversation_id,tool_used,summary,entities,metadata
conv_001,search_tool,Found 3 related docs,["meeting","plan"],{"type":"search"}
```

## 🔐 Configuration

### Backend (.env)
```env
API_HOST=localhost
API_PORT=8000
GEMINI_API_KEY=your_key_here
CHROMA_DB_PATH=./chroma_data
ENABLE_RAG=true
LOG_LEVEL=INFO
```

### Frontend (.env)
```env
API_BASE_URL=http://localhost:8000
ENABLE_MEMORY_RAG=true
ENABLE_SPEECH_RESPONSE=true
ENABLE_AUDIO_INPUT=true
```

## 🚀 Deployment

### Docker Compose
```bash
docker-compose up -d
```

### Individual Services
```bash
# Backend
cd backend
docker build -t voice-ai-backend -f ../backend.Dockerfile .
docker run -p 8000:8000 voice-ai-backend

# Frontend
cd frontend
docker build -t voice-ai-frontend -f ../frontend.Dockerfile .
docker run -p 8501:8501 voice-ai-frontend
```

## 🧪 Testing

### Test Backend
```bash
cd backend
pytest tests/
```

### Test Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```

## 📈 Performance Metrics

| Metric | Target | Status |
|--------|--------|--------|
| STT latency | < 2s | ✓ |
| Intent classification | < 500ms | ✓ |
| Memory retrieval | < 1s | ✓ |
| Total response time | < 5s | ✓ |
| UI responsiveness | < 100ms | ✓ |

## 🛠️ Development

### Setup Development Environment
```bash
python quickstart.py
```

### Run with Hot Reload
```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
streamlit run streamlit_app.py --logger.level=debug
```

### Code Quality
```bash
# Format
black voice_assitant/

# Lint
flake8 voice_assitant/

# Type check
mypy voice_assitant/
```

## 🎯 Use Cases

1. **Personal Assistant**
   - Note-taking
   - Task management
   - Information retrieval

2. **Customer Support**
   - Query resolution
   - Context-aware responses
   - Issue tracking

3. **Meeting Assistant**
   - Meeting summary
   - Action item extraction
   - Follow-up generation

4. **Learning Assistant**
   - Concept explanation
   - Question answering
   - Topic suggestions

## 🔮 Future Enhancements

- [ ] Multi-user support with authentication
- [ ] Advanced analytics dashboard
- [ ] Integration with external APIs
- [ ] Custom tool creation UI
- [ ] Fine-tuning capabilities
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] Voice command shortcuts

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Gemini API Documentation](https://ai.google.dev)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License

## 🙋 Support

For issues or questions:
- Check documentation in `/docs`
- Review API docs at `/api/v1/docs`
- Check ChromaDB setup in frontend utils
- Review logs in respective services

---

**Built with 🤖 CrewAI, 🧠 Gemini, and ❤️ for the hackathon**
