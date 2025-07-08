from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import subprocess
import uuid

router = APIRouter()

@router.post("/separate/")
async def separate_audio(file: UploadFile = File(...)):
    # 1. Save uploaded file
    file_id = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    input_path = f"uploads/{file_id}_{file.filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Run Demucs
    output_dir = "separated"
    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run([
            "demucs",
            "--two-stems=vocals",
            "-o", output_dir,
            input_path
        ], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Demucs failed to process audio."}

    # 3. Locate vocals.wav
    filename_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    demucs_folder = os.path.join(output_dir, "htdemucs", f"{filename_no_ext}")
    vocal_path = os.path.join(demucs_folder, "vocals.wav")

    if not os.path.exists(vocal_path):
        return {"error": "Vocals file not found."}

    return FileResponse(vocal_path, media_type="audio/wav", filename="vocals.wav")
