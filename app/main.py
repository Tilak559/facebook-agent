from fastapi import FastAPI
from app.routers import webhook

app = FastAPI(
    title="Facebook Messenger Chatbot",
    description="A chatbot that uses OpenAI's GPT to respond to Facebook messages",
    version="1.0.0"
)

# Include routers
app.include_router(webhook.router, tags=["webhook"])

@app.get("/")
async def root():
    """Root endpoint to verify the API is running."""
    return {"status": "ok", "message": "Facebook Messenger Chatbot is running"} 