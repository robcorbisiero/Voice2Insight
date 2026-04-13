# Voice-to-Insight Claims Assistant

Voice-to-Insight (V2I) Claims Assistant is a full-stack application designed to process audio files for insurance claims. It provides an automated pipeline for transcription, PII redaction, and AI-driven analysis (including sentiment, urgency, and entity extraction), presenting the results on a real-time React dashboard.

## Features

- **Audio Processing**: Upload and transcribe audio files.
- **AI-Driven Analysis**: Uses Gemini 1.5 Pro to analyze transcribed audio for sentiment, urgency, and key entity extraction.
- **PII Redaction**: Automatically detects and redacts Personally Identifiable Information for security and compliance.
- **Real-Time Dashboard**: A React/TypeScript frontend to view claims, transcriptions, and actionable insights in real-time.
- **Containerized**: Built and deployed easily using Docker Compose.

## Tech Stack

- **Frontend**: React, TypeScript, Vite
- **Backend**: Python, FastAPI
- **Database/Storage**: Supabase
- **AI Processing**: Gemini 1.5 Pro
- **Infrastructure**: Docker & Docker Compose

## Setup & Execution

### Prerequisites

- Docker and Docker Compose installed
- Supabase project (for database/storage)
- Google Gemini API key

### Environment Variables

Create a `.env` file in the root directory and populate it with your configuration (you can refer to `.env.example` if available).

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GEMINI_API_KEY=your_gemini_api_key
```

### Running the Application

1. Ensure Docker is running on your system.
2. Build and start the services using Docker Compose from the root directory:

   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - **Frontend**: `http://localhost:5173`
   - **Backend API**: `http://localhost:8000`

## Structure

- `/frontend` - Contains the Vite-based React + TypeScript dashboard application.
- `/backend` - Contains the Python-based FastAPI services for handling file uploads, transcription, and data processing.
- `docker-compose.yml` - Configuration to orchestrate both the frontend and backend services together.

