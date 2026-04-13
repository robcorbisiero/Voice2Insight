# PII Redaction module
import re
from pydub import AudioSegment
from pydub.generators import Sine

# Regex patterns for basic Credit Card and Phone numbers
CC_PATTERN = r'\b(?:\d[ -]*?){13,16}\b'
PHONE_PATTERN = r'\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'

def redact_text_and_get_timestamps(segments_with_words):
    """
    Given faster-whisper word segments, identify PII words.
    returns final redacted transcript, and a list of mute ranges [(start_sec, end_sec)].
    """
    mute_ranges = []
    final_text = ""
    
    # We will reconstruct the text from word objects
    # word object has: word, start, end, probability
    
    current_transcript = ""
    # Map raw index to word object for later
    word_map = []
    
    for segment in segments_with_words:
        for word in segment.words:
            w_text = word.word
            start_off = len(current_transcript)
            current_transcript += w_text
            end_off = len(current_transcript)
            word_map.append({"word": word, "start_char": start_off, "end_char": end_off})

    # Search for PII in the full transcript
    redacted_transcript = current_transcript
    
    # Find all CC and Phone matches
    matches = []
    for match in re.finditer(CC_PATTERN, current_transcript):
        matches.append((match.start(), match.end(), "CC"))
    for match in re.finditer(PHONE_PATTERN, current_transcript):
        matches.append((match.start(), match.end(), "PHONE"))
        
    # Process matches: find which words fall into these ranges
    for start_char, end_char, ptype in matches:
        # redact in transcript
        original_len = end_char - start_char
        redacted_transcript = redacted_transcript[:start_char] + ("[BEEP]" * max(1, original_len // 6)).ljust(original_len, " ") + redacted_transcript[end_char:]
        
        # find matching words for timestamps
        s_time = None
        e_time = None
        for w in word_map:
            # if word overlaps with match range
            if max(w["start_char"], start_char) < min(w["end_char"], end_char):
                if s_time is None:
                    s_time = w["word"].start
                e_time = w["word"].end
                
        if s_time is not None and e_time is not None:
             # add slight padding
             mute_ranges.append((max(0, s_time - 0.1), e_time + 0.1))
             
    # Cleanup redacted_transcript
    redacted_transcript = re.sub(r'\[BEEP\](?:\s*\[BEEP\])+', '[BEEP]', redacted_transcript)

    return redacted_transcript, mute_ranges

def apply_redaction_to_audio(audio_path, output_path, mute_ranges):
    """
    Applies silence to the specified ranges in the audio file.
    mute_ranges are in seconds.
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        
        for start_sec, end_sec in mute_ranges:
            start_ms = int(start_sec * 1000)
            end_ms = int(end_sec * 1000)
            
            # create 1000Hz beep chunk
            beep = Sine(1000).to_audio_segment(duration=end_ms - start_ms).apply_gain(-10)
            
            # overlay the beep onto the audio, reducing the original audio gain to -120dB during the beep 
            audio = audio.overlay(beep, position=start_ms, gain_during_overlay=-120)
            
        audio.export(output_path, format="map", parameters=["-q:a", "0"] if audio_path.endswith('.mp3') else [])
        if not output_path.endswith('.mp3'):
             audio.export(output_path, format="mp3") # Ensure export type

        return True
    except Exception as e:
        print(f"Error applying audio redaction: {e}")
        return False
