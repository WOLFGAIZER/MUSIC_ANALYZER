# utils/file_manager.py
import os
import aiofiles
from uuid import uuid4

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_file(file):
    file_ext = file.filename.split(".")[-1]
    unique_name = f"{uuid4().hex}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return file_path
