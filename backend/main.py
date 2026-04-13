import os
import uuid
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .audio_processor import process_audio
from .ai_analysis import analyze_transcript
# from .supabase_client import upload_file, insert_claim # Will mock for now if no keys

load_dotenv()

app = FastAPI(title="Voice-to-Insight (V2I) API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Voice-to-Insight API is running"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Only .wav or .mp3 files are supported")

    # generate a unique claim ID
    claim_id = str(uuid.uuid4())

    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    try:
        # 1. Process audio & redact
        redacted_audio_path, transcript = process_audio(temp_audio_path)

        # 2. Analyze transcript with Gemini
        insights = analyze_transcript(transcript)

        # In a real app with Supabase tokens provided, we would upload the files, get URLs, 
        # and insert into the `claims` table.
        # For demonstration context, we'll return the parsed data to the frontend to mock real-time
        
        return {
            "id": claim_id,
            "transcript": transcript,
            "insights": insights,
            "status": "success",
            "message": "File processed and redacted successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup original temp file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
