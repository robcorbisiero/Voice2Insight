import os
import json
from google import genai
from pydantic import BaseModel

# Initialize Gemini Client
# It will automatically use GEMINI_API_KEY from environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: could not initialize Gemini client. Key missing? Error: {e}")
    client = None

class AnalysisInsights(BaseModel):
    sentiment: str
    urgency_score: int
    claimant_name: str | None
    location: str | None
    incident_time: str | None

def analyze_transcript(transcript: str) -> dict:
    """
    Uses Gemini 1.5 Pro to extract insights from the transcript.
    """
    if client is None:
        return {
            "sentiment": "Unknown",
            "urgency_score": 0,
            "claimant_name": None,
            "location": None,
            "incident_time": None,
            "error": "Gemini API key missing or client not initialized."
        }

    prompt = f"""
You are an insurance claims analysis assistant.
Analyze the following transcript from an insurance claim call.

Extract the following information:
1. Sentiment Analysis (Must be one of: Calm, Frustrated, Distressed)
2. Urgency Score (1-10 scale based on the description of damage/danger)
3. Claimant name (if mentioned)
4. Location of incident (if mentioned)
5. Time of incident (if mentioned)

Return the extraction EXACTLY as a valid JSON object matching this schema:
{{
    "sentiment": "Calm|Frustrated|Distressed",
    "urgency_score": 1-10,
    "claimant_name": "Name or null",
    "location": "Location or null",
    "incident_time": "Time or null"
}}

Transcript:
{transcript}
"""

    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt,
        )
        
        # Parse JSON from response
        text = response.text
        # Clean up possible markdown blocls
        if text.startswith("```json"):
            text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
        elif text.startswith("```"):
            text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
        
        return json.loads(text.strip())
        
    except Exception as e:
        print(f"Failed to analyze transcript: {e}")
        return {
            "sentiment": "Error",
            "urgency_score": 0,
            "claimant_name": None,
            "location": None,
            "incident_time": None,
            "error": str(e)
        }
