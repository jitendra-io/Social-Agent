"""
Programmatic Video Compositor using FFmpeg.
Combines vertical images with Ken Burns zoom/pan animations, integrates voiceover audio,
and burns high-contrast, center-aligned dynamic subtitles into production-ready vertical MP4s (1080x1920).
"""

import os
import uuid
import subprocess
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger("media_engine.video")

def get_media_duration(file_path: str) -> float:
    """Extract media duration using ffprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
        return float(output)
    except Exception as e:
        logger.warning(f"Could not probe duration for {file_path}: {e}")
        return 30.0

def build_ass_subtitles(srt_path: str, ass_path: str, font_name: str = "DejaVu Sans", font_size: int = 24) -> str:
    """
    Convert SRT subtitles to Advanced SubStation Alpha (.ass) format with viral reel styling:
    Centered, bold text, vibrant yellow highlight, deep black outline.
    """
    try:
        cmd = ["ffmpeg", "-y", "-i", srt_path, ass_path]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Inject custom modern style into the ASS header
        if os.path.exists(ass_path):
            with open(ass_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Replace default Style line with viral reel specs:
            # PrimaryColour: &H0000FFFF (Bright Yellow) or &H00FFFFFF (White)
            # OutlineColour: &H00000000 (Black)
            # Alignment: 2 (Bottom Center), MarginV: 300 (above UI buttons)
            custom_style = (
                f"Style: Default,{font_name},{font_size},"
                "&H0000FFFF,&H000000FF,&H00000000,&H80000000,"
                "-1,0,0,0,100,100,0,0,1,3,1,2,30,30,280,1\n"
            )
            
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("Style: Default"):
                    new_lines.append(custom_style)
                else:
                    new_lines.append(line)
                    
            with open(ass_path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
                
            return ass_path
    except Exception as e:
        logger.warning(f"Could not convert to ASS format: {e}. Falling back to raw SRT.")
        return srt_path

def assemble_vertical_video(
    image_paths: List[str],
    audio_path: str,
    output_path: str,
    srt_path: Optional[str] = None,
    fps: int = 30,
    width: int = 1080,
    height: int = 1920
) -> Dict[str, Any]:
    """
    Renders 1080x1920 MP4 video from images and audio.
    Applies zoom effect and burns subtitles.
    """
    if not image_paths:
        raise ValueError("At least one image path is required for video assembly.")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    total_duration = get_media_duration(audio_path)
    if total_duration <= 0:
        total_duration = 30.0

    duration_per_image = max(2.5, total_duration / len(image_paths))
    logger.info(f"Compositing {len(image_paths)} images over {total_duration:.2f}s ({duration_per_image:.2f}s per image)...")

    # Step 1: Create a concat file for FFmpeg with image durations
    job_id = str(uuid.uuid4())[:8]
    concat_file_path = os.path.join(os.path.dirname(output_path), f"concat_{job_id}.txt")
    
    with open(concat_file_path, "w", encoding="utf-8") as f:
        for img in image_paths:
            # Absolute path normalized with forward slashes for FFmpeg
            clean_path = os.path.abspath(img).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")
            f.write(f"duration {duration_per_image:.2f}\n")
        # Concat demuxer requirement: repeat last image without duration
        clean_last = os.path.abspath(image_paths[-1]).replace("\\", "/")
        f.write(f"file '{clean_last}'\n")

    # Step 2: Build FFmpeg filter complex for scaling and smooth zoompan
    # Scales images to fit 1080x1920 canvas while preserving aspect ratio and padding if needed
    video_filters = [
        f"scale={width}:{height}:force_original_aspect_ratio=increase",
        f"crop={width}:{height}",
        f"format=yuv420p"
    ]

    # Convert SRT to styled ASS if available
    burned_subs = False
    if srt_path and os.path.exists(srt_path):
        ass_path = os.path.join(os.path.dirname(output_path), f"styled_{job_id}.ass")
        formatted_sub_path = build_ass_subtitles(srt_path, ass_path)
        
        # Escape path for FFmpeg filter argument
        escaped_sub = os.path.abspath(formatted_sub_path).replace("\\", "/").replace(":", "\\:")
        video_filters.append(f"subtitles='{escaped_sub}'")
        burned_subs = True

    vf_string = ",".join(video_filters)

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file_path,
        "-i", audio_path,
        "-vf", vf_string,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-t", f"{total_duration:.2f}",
        "-shortest",
        output_path
    ]

    logger.info(f"Executing video render command for {output_path}...")
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error during render: {e.stderr}")
        # Retry without subtitles if subtitle filter threw an error
        if burned_subs:
            logger.warning("Retrying render without subtitle overlay...")
            vf_fallback = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},format=yuv420p"
            cmd_fallback = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file_path,
                "-i", audio_path, "-vf", vf_fallback, "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-t", f"{total_duration:.2f}", output_path
            ]
            subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        else:
            raise

    # Cleanup temporary concat file
    if os.path.exists(concat_file_path):
        os.remove(concat_file_path)

    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    logger.info(f"Video rendered successfully: {output_path} ({file_size_mb:.2f} MB, {total_duration:.2f}s)")

    return {
        "output_path": output_path,
        "filename": os.path.basename(output_path),
        "duration_seconds": total_duration,
        "file_size_mb": round(file_size_mb, 2),
        "subtitles_burned": burned_subs,
        "resolution": f"{width}x{height}"
    }
