# routes/karaoke.py

from fastapi import APIRouter, Form
from pydantic import BaseModel
import os
from services.ffmpeg_mixer import mix_selected_stems

router = APIRouter()

class KaraokeRequest(BaseModel):
    filename: str
    selected_stems: list

@router.post("/")
def generate_karaoke(request: KaraokeRequest):
    base_name = request.filename.replace(".mp3", "").replace(".wav", "")
    input_dir = f"outputs/{base_name}/separated_stems"
    output_path = f"outputs/{base_name}_karaoke.wav"

    success = mix_selected_stems(input_dir, request.selected_stems, output_path)

    if success:
        return {"message": "Karaoke created!", "karaoke_path": output_path}
    else:
        return {"error": "Failed to generate karaoke. Check stem files."}
