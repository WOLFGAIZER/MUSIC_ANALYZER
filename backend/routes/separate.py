# routes/separate.py

from fastapi import APIRouter, UploadFile, File
from services.hf_demucs import run_demucs_hf
import shutil
import os
import uuid
import subprocess

router = APIRouter()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@router.post("/")
async def separate_stems(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    original_filename = file.filename
    input_path = f"uploads/{unique_id}_{original_filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert to WAV if needed
    if not original_filename.endswith(".wav"):
        wav_path = input_path.rsplit(".", 1)[0] + ".wav"
        try:
            subprocess.run(["ffmpeg", "-y", "-i", input_path, wav_path], check=True)
            input_path = wav_path
        except subprocess.CalledProcessError as e:
            return {"error": f"FFmpeg conversion failed: {e}"}

    # Call HuggingFace Demucs (returns ZIP but we'll handle later)
    result = run_demucs_hf(input_path)

    if result:
        # Save to temporary file
        output_file = f"outputs/{unique_id}_demucs_output.zip"
        with open(output_file, "wb") as f:
            f.write(result)

        return {
            "message": "Stems separated (ZIP output ready)",
            "zip_path": output_file,
            "note": "Stem preview not implemented in this version"
        }

    return {"error": "Stem separation failed"}
