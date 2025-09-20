# AI Customer Support Chatbot

A simple AI-powered customer support chatbot built with Python FastAPI and React.

## Features

- 🤖 **AI Chat**: Powered by OpenAI GPT-3.5
- 💬 **Real-time Chat**: Clean, modern interface
- 🌍 **Simple Setup**: Just Docker and an API key!

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key

### Setup

1. **Clone and setup:**
```bash
git clone <your-repo>
cd ai-customer-support-chatbot
```

2. **Add your OpenAI API key:**
```bash
# Copy the example environment file
cp backend/env.example backend/.env

# Edit backend/.env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

3. **Run with Docker:**
```bash
docker compose up --build
```

4. **Open your browser:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Usage

1. Open http://localhost:3000
2. Start chatting with the AI assistant!
3. The bot will remember your conversation during the session

## Stopping the Application

```bash
docker compose down
```

That's it! 🎉

## What's Included

- **Backend**: FastAPI server with OpenAI integration
- **Frontend**: React chat interface
- **Docker**: Easy containerized setup
- **API Docs**: Auto-generated documentation at `/docs`

## Customization

- Edit `backend/main.py` to modify the AI system prompt
- Edit `frontend/src/App.css` to change the styling
- The chat history is stored in memory (resets when server restarts)
