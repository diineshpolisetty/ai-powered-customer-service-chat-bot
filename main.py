from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Customer Support Chatbot")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple chat history storage
chat_history = {}

@app.get("/")
async def root():
    return {"message": "AI Customer Support Chatbot API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(message: dict):
    """Simple chat endpoint"""
    try:
        user_message = message.get("message", "")
        session_id = message.get("session_id", "default")
        
        if not user_message:
            return {"error": "No message provided"}
        
        # Get or create chat history for session
        if session_id not in chat_history:
            chat_history[session_id] = []
        
        # Add user message to history
        chat_history[session_id].append({"role": "user", "content": user_message})
        
        # Generate AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant. Be friendly and professional."},
                *chat_history[session_id][-10:],  # Last 10 messages for context
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to history
        chat_history[session_id].append({"role": "assistant", "content": ai_response})
        
        return {"response": ai_response, "session_id": session_id}
        
    except Exception as e:
        return {"error": f"Failed to process message: {str(e)}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = "websocket_session"
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            # Get or create chat history
            if session_id not in chat_history:
                chat_history[session_id] = []
            
            # Add user message
            chat_history[session_id].append({"role": "user", "content": user_message})
            
            # Generate AI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant. Be friendly and professional."},
                    *chat_history[session_id][-10:],
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            chat_history[session_id].append({"role": "assistant", "content": ai_response})
            
            # Send response back
            await websocket.send_text(json.dumps({
                "type": "response",
                "message": ai_response,
                "session_id": session_id
            }))
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
