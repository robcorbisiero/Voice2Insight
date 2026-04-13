import os
from faster_whisper import WhisperModel
from .redaction import redact_text_and_get_timestamps, apply_redaction_to_audio

# Load model once on startup
# Using base.en for speed and acceptable accuracy. Small/Medium can be used for better accuracy.
try:
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
except Exception as e:
    print(f"Warning: could not load Whisper model. Error: {e}")
    model = None

def process_audio(audio_path: str):
    """
    Transcribes audio, performs PII redaction, saves redacted audio.
    Returns: (redacted_audio_path, redacted_transcript)
    """
    if model is None:
        return audio_path, "Error: Whisper model not loaded."

    print(f"Processing audio {audio_path}...")
    # transcribe with word timestamps
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    # We must iterate segments to get the words
    segments_list = list(segments)
    
    # Identify PII and get mute ranges
    redacted_transcript, mute_ranges = redact_text_and_get_timestamps(segments_list)
    print(f"Mute ranges identified: {mute_ranges}")
    
    base_name, _ = os.path.splitext(audio_path)
    # Output always to .mp3 for web playback compatibility
    redacted_audio_path = f"{base_name}_redacted.mp3"
    
    if mute_ranges:
        success = apply_redaction_to_audio(audio_path, redacted_audio_path, mute_ranges)
        if not success:
            redacted_audio_path = audio_path
    else:
        # If no redaction needed, just convert to mp3 if needed or return original
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_path)
        audio.export(redacted_audio_path, format="mp3")
        
    return redacted_audio_path, redacted_transcript
