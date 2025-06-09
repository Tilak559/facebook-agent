from fastapi import APIRouter, Request, Response, HTTPException, Query
from app.config import get_settings
from app.services.messenger import send_message, get_gpt_reply

router = APIRouter()

# Facebook webhook verification (GET)
@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
) -> Response:
    settings = get_settings()
    print("Verifying webhook...")
    if hub_mode == "subscribe" and hub_verify_token == settings.VERIFY_TOKEN:
        print("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")
    print("Verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")

# Handle incoming Facebook message events (POST)
@router.post("/webhook")
async def webhook(request: Request) -> dict:
    try:
        data = await request.json()
        print("Incoming Messenger data:", data)
    except Exception as e:
        print("Error parsing JSON:", e)
        return {"status": "invalid JSON"}

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                message_text = messaging_event.get("message", {}).get("text")

                if sender_id and message_text:
                    print(f"Message from {sender_id}: {message_text}")
                    reply = get_gpt_reply(sender_id, message_text)
                    print(f"GPT reply: {reply}")
                    send_message(sender_id, reply)
    return {"status": "ok"}
