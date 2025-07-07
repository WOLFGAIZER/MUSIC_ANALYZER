# routes/karaoke.py
from fastapi import APIRouter, Query
from typing import List
from services.ffmpeg_mixer import generate_karaoke_mix

router = APIRouter()

@router.post("/")
def make_karaoke(
    stems_path: str = Query(...),
    mute: List[str] = Query(default=["vocals"])  # e.g. ["vocals", "drums"]
):
    try:
        output_file = generate_karaoke_mix(stems_path, mute)
        return {
            "message": "Karaoke track created.",
            "file": output_file
        }
    except Exception as e:
        return {"error": str(e)}
