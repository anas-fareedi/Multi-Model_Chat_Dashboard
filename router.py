import os
import requests

import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded key:", os.getenv("OPENROUTER_API_KEY"))


OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_model(model, messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)
    return response.json()
