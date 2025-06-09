# Facebook Messenger Chatbot

A FastAPI-based chatbot that uses OpenAI's GPT to respond to Facebook messages.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
FB_PAGE_TOKEN=your_facebook_page_token_here
VERIFY_TOKEN=your_verify_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

Start the server:
```bash
python run.py
```

The server will start at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Webhook Setup

1. Set up a Facebook Page and get the Page Access Token
2. Create a Facebook App and configure the webhook
3. Use the webhook URL: `https://your-domain.com/webhook`
4. Set the Verify Token to match your `VERIFY_TOKEN` in the `.env` file

## Project Structure

```
/app
  ├── __init__.py
  ├── main.py
  ├── config.py
  ├── routers/
  │   └── webhook.py
  └── services/
      └── messenger.py
/run.py
/requirements.txt
/.env
/README.md
``` 