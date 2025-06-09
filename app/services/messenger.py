import requests
from app.config import get_settings
from openai import OpenAI

# In-memory user chat history (user_id -> list of messages)
user_histories = {}

def send_message(recipient_id: str, message_text: str) -> dict:
    """
    Send a message to a Facebook user.
    
    Args:
        recipient_id: The Facebook user ID to send the message to
        message_text: The text message to send
        
    Returns:
        dict: The response from Facebook's API
    """
    settings = get_settings()
    url = f"https://graph.facebook.com/v18.0/me/messages"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    
    headers = {
        "Authorization": f"Bearer {settings.FB_PAGE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_gpt_reply(user_id: str, message_text: str) -> str:
    settings = get_settings()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Get or create the user's history
    history = user_histories.get(user_id, [])
    # Add the new user message
    history.append({"role": "user", "content": message_text})

    # Always start with the system prompt
    messages = [
        {"role": "system", "content": "You are a helpful and friendly real estate assistant. "
         "You specialize in helping users find apartments. Provide concise, clear, and relevant answers. "
         "Be polite and conversational. If details like location or budget are missing, ask for them."}
    ] + history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=256,
        temperature=0.7
    )

    # Add the assistant's reply to the history
    assistant_reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": assistant_reply})

    # Save updated history (keep only last 10 exchanges for context)
    user_histories[user_id] = history[-10:]

    return assistant_reply
