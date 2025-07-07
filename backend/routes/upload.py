# routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.file_manager import save_uploaded_file

router = APIRouter()

@router.post("/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp3", ".wav", ".flac")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    file_path = await save_uploaded_file(file)
    return {"message": "File uploaded successfully", "file_path": file_path}
