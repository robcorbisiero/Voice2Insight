# Voice2Insight — audio-processing prototype

A work-in-progress Python audio-processing experiment with transcription, limited pattern-based redaction, and optional generated claim summaries.

**Status: incomplete integration.** This repository is not currently a verified end-to-end claims application. The active Vite entry point is the starter TypeScript page; a React dashboard draft exists but is not wired into that entry point. Supabase persistence and real-time updates are not implemented.

## Code available for review

| Area | Current implementation |
| --- | --- |
| Upload API | FastAPI endpoint accepts WAV/MP3 and writes a temporary input file |
| Transcription | faster-whisper base.en model on CPU; downloading model files may be required |
| Redaction | Regex matches for some phone/card number formats with timestamp-based audio beeps |
| Analysis | Google GenAI call with a legacy model identifier; live-provider compatibility is not verified |
| Browser UI | Vite TypeScript scaffold plus an unconnected React draft |
| Storage | Supabase-related configuration is present; no upload or database persistence path is active |

## Known blockers

- The container launches main:app, while backend modules use relative imports that need a consistent package layout.
- The redaction export path uses an invalid format name and can fall back to the original audio on failure.
- Derived audio files are not reliably cleaned up; the upload response does not serve playable redacted audio.
- Missing transcription models return an error string rather than a failed processing result.
- Redaction patterns do not cover names, addresses, or all sensitive identifiers. This is not a privacy or compliance guarantee.
- Authentication, bounded uploads, dependency refresh, automated tests, and a completed UI/API walkthrough remain unfinished.

## Development inspection

```bash
git clone https://github.com/robcorbisiero/Voice2Insight.git
cd Voice2Insight
```

Inspect backend/main.py, audio_processor.py, redaction.py, and frontend/src/main.ts before attempting a full run. Docker Compose is a development scaffold, not a verified one-command demo. Do not supply real claims, personal recordings, production Supabase credentials, or paid AI keys to this prototype while these blockers remain.

## Completion order

1. Make backend startup and the frontend entry point consistent.
2. Fail processing when transcription/redaction fails; test audio output and cleanup.
3. Add isolated tests using synthetic recordings and mocked model responses.
4. Verify the complete local upload flow, then consider persistence and authentication.

For currently demonstrated infrastructure work, see the [homelab evidence index](https://github.com/robcorbisiero/enterprise-infrastructure-homelab/blob/main/PORTFOLIO.md). This prototype should not be presented as a production system.
