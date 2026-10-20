"""
FastAPI Microservice for Zero-Cost Media Generation.
Provides HTTP APIs for Edge-TTS voice synthesis, Pollinations/FLUX image creation,
and programmatic FFmpeg video assembly.
"""

import os
import uuid
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from audio_generator import generate_speech_with_subtitles, SUPPORTED_VOICES
from image_generator import generate_images_batch
from video_assembler import assemble_vertical_video

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("media_engine")

OUTPUT_DIR = os.getenv("SHARED_MEDIA_DIR", "/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="Zero-Cost Programmatic Media Engine",
    description="Microservice for neural voiceover synthesis, 9:16 AI image generation, and FFmpeg video compositing.",
    version="1.0.0"
)

# Enable CORS for local cross-container interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount shared media folder for direct HTTP asset retrieval
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

# ---------------------------------------------------------------------
# Pydantic Request Models
# ---------------------------------------------------------------------
class VoiceRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Script content to synthesize into neural speech")
    voice: Optional[str] = Field("christopher", description="Neural voice key or full Edge-TTS voice identifier")
    rate: Optional[str] = Field("+0%", description="Speaking speed rate modification")
    pitch: Optional[str] = Field("+0Hz", description="Voice pitch modification")

class ImagesRequest(BaseModel):
    prompts: List[str] = Field(..., min_items=1, description="List of visual scene prompts to generate")
    hf_token: Optional[str] = Field(None, description="Optional Hugging Face user access token")

class RenderRequest(BaseModel):
    image_paths: List[str] = Field(..., min_items=1, description="Paths to images to concatenate")
    audio_path: str = Field(..., description="Path to voiceover MP3 file")
    srt_path: Optional[str] = Field(None, description="Path to SRT subtitle file for dynamic burning")
    output_filename: Optional[str] = Field(None, description="Desired name of output MP4 file")

class FullPipelineRequest(BaseModel):
    script: str = Field(..., min_length=10, description="Full script for voiceover and subtitles")
    visual_prompts: List[str] = Field(..., min_items=1, description="Sequential visual scene prompts")
    voice: Optional[str] = Field("christopher", description="Voice identifier")

# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Healthcheck endpoint for Docker container readiness checks."""
    return {
        "status": "healthy",
        "service": "media-engine",
        "output_dir": OUTPUT_DIR,
        "supported_voices": list(SUPPORTED_VOICES.keys())
    }

@app.post("/api/generate-voice", status_code=status.HTTP_200_OK)
async def api_generate_voice(payload: VoiceRequest):
    """Synthesize neural audio and extract word-level subtitle cues."""
    try:
        result = await generate_speech_with_subtitles(
            text=payload.text,
            voice=payload.voice,
            rate=payload.rate or "+0%",
            pitch=payload.pitch or "+0Hz",
            output_dir=OUTPUT_DIR
        )
        return {
            "status": "success",
            "data": result,
            "preview_url": f"/output/{result['audio_filename']}"
        }
    except Exception as e:
        logger.error(f"Voice generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fetch-images", status_code=status.HTTP_200_OK)
async def api_fetch_images(payload: ImagesRequest):
    """Generate 9:16 vertical images for multiple scene prompts."""
    try:
        results = await generate_images_batch(
            prompts=payload.prompts,
            output_dir=OUTPUT_DIR,
            hf_token=payload.hf_token or os.getenv("HF_TOKEN")
        )
        return {
            "status": "success",
            "count": len(results),
            "data": results
        }
    except Exception as e:
        logger.error(f"Image generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/render-video", status_code=status.HTTP_200_OK)
async def api_render_video(payload: RenderRequest):
    """Assemble vertical images, voiceover audio, and subtitles into a 1080x1920 MP4."""
    try:
        output_name = payload.output_filename or f"reel_{uuid.uuid4().hex[:8]}.mp4"
        if not output_name.endswith(".mp4"):
            output_name += ".mp4"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        render_info = assemble_vertical_video(
            image_paths=payload.image_paths,
            audio_path=payload.audio_path,
            output_path=output_path,
            srt_path=payload.srt_path
        )
        return {
            "status": "success",
            "data": render_info,
            "stream_url": f"/output/{output_name}"
        }
    except Exception as e:
        logger.error(f"Video assembly failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-full-video", status_code=status.HTTP_200_OK)
async def api_generate_full_video(payload: FullPipelineRequest):
    """
    End-to-end convenience pipeline for n8n orchestrator:
    1. Generates voiceover audio and SRT subtitle cues.
    2. Generates vertical scene visuals in parallel.
    3. Composites video with Ken Burns zoom and burned subtitles.
    """
    try:
        job_id = str(uuid.uuid4())[:8]
        logger.info(f"Starting complete media pipeline for job {job_id}...")

        # 1. Voiceover
        voice_result = await generate_speech_with_subtitles(
            text=payload.script,
            voice=payload.voice,
            output_dir=OUTPUT_DIR
        )

        # 2. Visuals
        image_results = await generate_images_batch(
            prompts=payload.visual_prompts,
            output_dir=OUTPUT_DIR,
            hf_token=os.getenv("HF_TOKEN")
        )
        image_paths = [img["filepath"] for img in image_results]

        # 3. Video Assembly
        video_filename = f"video_{job_id}.mp4"
        video_path = os.path.join(OUTPUT_DIR, video_filename)
        video_result = assemble_vertical_video(
            image_paths=image_paths,
            audio_path=voice_result["audio_path"],
            output_path=video_path,
            srt_path=voice_result["srt_path"]
        )

        return {
            "status": "success",
            "job_id": job_id,
            "video_path": video_result["output_path"],
            "video_filename": video_filename,
            "duration_seconds": video_result["duration_seconds"],
            "file_size_mb": video_result["file_size_mb"],
            "preview_url": f"/output/{video_filename}",
            "audio": voice_result,
            "images": image_results
        }
    except Exception as e:
        logger.error(f"Full video generation pipeline failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
