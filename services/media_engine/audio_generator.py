"""
Zero-Cost Neural Audio Generator using Microsoft Edge-TTS.
Produces broadcast-quality speech and word-level timestamp markers for dynamic subtitle burning.
"""

import os
import uuid
import edge_tts
import subprocess
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("media_engine.audio")

# Curated list of high-retention neural voices
SUPPORTED_VOICES = {
    "christopher": "en-US-ChristopherNeural",  # Authoritative, documentary, deep
    "eric": "en-US-EricNeural",                # Energetic, dynamic, social media
    "guy": "en-US-GuyNeural",                  # Casual, conversational
    "sonia": "en-GB-SoniaNeural",              # British, refined, luxury/agency
    "ryan": "en-GB-RyanNeural",                # British male, tech/educational
    "natasha": "en-AU-NatashaNeural"           # Australian, friendly
}

def get_audio_duration(file_path: str) -> float:
    """Extract precise duration of an audio file in seconds via ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0.0))
    except Exception as e:
        logger.warning(f"Could not probe audio duration via ffprobe: {e}. Falling back to default.")
        return 30.0

async def generate_speech_with_subtitles(
    text: str,
    voice: Optional[str] = None,
    rate: str = "+0%",
    pitch: str = "+0Hz",
    output_dir: str = "/app/output"
) -> Dict[str, Any]:
    """
    Synthesize speech from text and generate corresponding SRT subtitle cues.
    
    Args:
        text: Script to synthesize.
        voice: Voice name key (e.g. 'christopher') or full Edge-TTS voice identifier.
        rate: Speed modifier (e.g. '+0%', '+10%').
        pitch: Pitch modifier (e.g. '+0Hz').
        output_dir: Directory to save generated assets.
        
    Returns:
        Dict with audio_path, srt_path, duration_seconds, voice_used, word_count.
    """
    os.makedirs(output_dir, exist_ok=True)
    job_id = str(uuid.uuid4())[:8]
    
    # Resolve voice identifier
    selected_voice = SUPPORTED_VOICES.get(voice.lower() if voice else "christopher", voice or "en-US-ChristopherNeural")
    
    audio_filename = f"audio_{job_id}.mp3"
    srt_filename = f"subs_{job_id}.srt"
    
    audio_path = os.path.join(output_dir, audio_filename)
    srt_path = os.path.join(output_dir, srt_filename)
    
    logger.info(f"Generating speech with voice '{selected_voice}' for job '{job_id}'...")
    
    communicate = edge_tts.Communicate(text=text, voice=selected_voice, rate=rate, pitch=pitch)
    submaker = edge_tts.SubMaker()
    
    # Stream audio and feed word boundaries into subtitle generator
    with open(audio_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    # Write subtitles to SRT
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_content = submaker.get_srt()
        # Fallback if text was too short for word boundaries
        if not srt_content.strip():
            srt_content = f"1\n00:00:00,000 --> 00:00:10,000\n{text}\n"
        srt_file.write(srt_content)
        
    duration = get_audio_duration(audio_path)
    word_count = len(text.split())
    
    logger.info(f"Audio generated successfully: {audio_path} ({duration:.2f}s, {word_count} words)")
    
    return {
        "job_id": job_id,
        "audio_path": audio_path,
        "audio_filename": audio_filename,
        "srt_path": srt_path,
        "srt_filename": srt_filename,
        "duration_seconds": duration,
        "voice_used": selected_voice,
        "word_count": word_count
    }
