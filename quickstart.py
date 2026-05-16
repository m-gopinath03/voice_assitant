"""
Quick start guide for the Voice Agentic AI system.
Run this to set up and start everything.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python():
    """Check Python version."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or version.minor < 9:
        print("⚠ Warning: Python 3.9+ recommended")
    return True


def create_env_files():
    """Create .env files from examples."""
    print_header("Creating Environment Files")
    
    backend_env = Path("voice_assitant/backend/.env")
    frontend_env = Path("voice_assitant/frontend/.env")
    
    if not backend_env.exists():
        print("Creating backend/.env...")
        # Create basic backend env
        with open(backend_env, "w") as f:
            f.write("""# Backend Environment Configuration
API_HOST=localhost
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:8501", "http://localhost:3000"]

# LLM Configuration
GEMINI_API_KEY=your_api_key_here

# ChromaDB
CHROMA_DB_PATH=./chroma_data

# Features
ENABLE_RAG=true
ENABLE_MEMORY=true
""")
        print("✓ backend/.env created")
    else:
        print("✓ backend/.env already exists")
    
    if not frontend_env.exists():
        print("Creating frontend/.env...")
        with open(frontend_env, "w") as f:
            f.write("""# Frontend Environment Configuration
API_BASE_URL=http://localhost:8000
ENABLE_MEMORY_RAG=true
ENABLE_SPEECH_RESPONSE=true
ENABLE_AUDIO_INPUT=true
""")
        print("✓ frontend/.env created")
    else:
        print("✓ frontend/.env already exists")


def install_dependencies():
    """Install dependencies."""
    print_header("Installing Dependencies")
    
    # Backend dependencies
    print("Installing backend dependencies...")
    backend_req = Path("voice_assitant/backend/requirements.txt")
    if backend_req.exists():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(backend_req)],
            check=False
        )
        print("✓ Backend dependencies installed")
    
    # Frontend dependencies
    print("\nInstalling frontend dependencies...")
    frontend_req = Path("voice_assitant/frontend/requirements.txt")
    if frontend_req.exists():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(frontend_req)],
            check=False
        )
        print("✓ Frontend dependencies installed")


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")
    
    dirs = [
        "voice_assitant/backend/data",
        "voice_assitant/backend/chroma_data",
        "voice_assitant/backend/logs",
        "voice_assitant/frontend/logs"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ {dir_path}")


def print_instructions():
    """Print setup instructions."""
    print_header("Setup Instructions")
    
    print("""
1. UPDATE CONFIGURATION
   - Edit voice_assitant/backend/.env
   - Add your Gemini API key
   - Configure API endpoints

2. START BACKEND
   cd voice_assitant/backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

3. START FRONTEND (in new terminal)
   cd voice_assitant/frontend
   streamlit run streamlit_app.py

4. ACCESS FRONTEND
   Open: http://localhost:8501

5. API DOCUMENTATION
   Backend: http://localhost:8000/docs
""")


def main():
    """Run setup."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     Voice Agentic AI - Quick Start Setup                  ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Run setup steps
    check_python()
    create_env_files()
    create_directories()
    install_dependencies()
    print_instructions()
    
    print_header("Setup Complete!")
    print("✓ Ready to start development\n")


if __name__ == "__main__":
    main()
