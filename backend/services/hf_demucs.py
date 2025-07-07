# services/hf_demucs.py

import os
import requests
from config import HF_API_TOKEN  # load this from .env via config.py

API_URL = "https://api-inference.huggingface.co/models/facebook/demucs"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def run_demucs_hf(audio_path: str) -> bytes | None:
    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        response = requests.post(API_URL, headers=headers, data=audio_data)

        if response.status_code == 200:
            return response.content
        else:
            print("HF API Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error running Hugging Face Demucs:", str(e))
        return None
