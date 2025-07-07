from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, separate, karaoke
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MUSIC_ANALYZER")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router, prefix="/upload")
app.include_router(separate.router, prefix="/separate")
app.include_router(karaoke.router, prefix="/karaoke")

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")