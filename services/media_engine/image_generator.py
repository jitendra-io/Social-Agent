"""
Zero-Cost AI Image Generator for Social Media Reels & Shorts.
Uses Pollinations.ai (FLUX) and Hugging Face free inference, with PIL gradient fallbacks.
Produces vertical 9:16 (1080x1920) assets.
"""

import os
import uuid
import random
import urllib.parse
import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger("media_engine.images")

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
HF_FLUX_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def create_synthetic_fallback_image(prompt: str, output_path: str, width: int = 1080, height: int = 1920) -> str:
    """Generate a sleek, dark-mode gradient visual fallback if external APIs are unreachable."""
    image = Image.new("RGB", (width, height), color=(15, 23, 42)) # Deep slate
    draw = ImageDraw.Draw(image)
    
    # Draw futuristic neon gradient circles
    colors = [
        (99, 102, 241, 60),  # Indigo
        (168, 85, 247, 50),  # Purple
        (236, 72, 153, 40),  # Pink
        (56, 189, 248, 50)   # Sky blue
    ]
    
    for _ in range(4):
        cx = random.randint(100, width - 100)
        cy = random.randint(200, height - 200)
        radius = random.randint(300, 600)
        color = random.choice(colors)
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color[:3])
        
    # Apply soft blur
    image = image.filter(ImageFilter.GaussianBlur(radius=80))
    image.save(output_path, "JPEG", quality=90)
    logger.info(f"Synthetic fallback visual created at {output_path}")
    return output_path

async def fetch_single_image(
    prompt: str,
    output_path: str,
    session: aiohttp.ClientSession,
    hf_token: Optional[str] = None,
    width: int = 1080,
    height: int = 1920,
    seed: Optional[int] = None
) -> str:
    """Download vertical AI visual for a single prompt."""
    if seed is None:
        seed = random.randint(1000, 999999)
        
    enhanced_prompt = f"{prompt}, cinematic lighting, 8k resolution, highly detailed, photorealistic, vertical wallpaper, hyper-modern aesthetic"
    encoded = urllib.parse.quote(enhanced_prompt)
    pollinations_url = f"{POLLINATIONS_BASE_URL}/{encoded}?width={width}&height={height}&model=flux&nologo=true&seed={seed}"
    
    # 1. Try Pollinations.ai FLUX endpoint
    try:
        logger.info(f"Fetching visual from Pollinations for prompt: '{prompt[:40]}...'")
        async with session.get(pollinations_url, timeout=aiohttp.ClientTimeout(total=45)) as resp:
            if resp.status == 200:
                data = await resp.read()
                with open(output_path, "wb") as f:
                    f.write(data)
                logger.info(f"Successfully saved Pollinations image to {output_path}")
                return output_path
            else:
                logger.warning(f"Pollinations returned status {resp.status}. Trying fallback.")
    except Exception as e:
        logger.warning(f"Pollinations fetch failed: {e}. Attempting secondary source.")

    # 2. Try Hugging Face FLUX inference if token available
    if hf_token:
        try:
            logger.info("Attempting Hugging Face FLUX inference...")
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {"inputs": enhanced_prompt, "parameters": {"width": width, "height": height}}
            async with session.post(HF_FLUX_URL, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    with open(output_path, "wb") as f:
                        f.write(data)
                    logger.info(f"Saved Hugging Face FLUX image to {output_path}")
                    return output_path
        except Exception as e:
            logger.warning(f"Hugging Face FLUX fetch failed: {e}")

    # 3. Resilient Local Synthetic Fallback
    logger.info("Using local synthetic gradient fallback generator.")
    return create_synthetic_fallback_image(prompt, output_path, width, height)

async def generate_images_batch(
    prompts: List[str],
    output_dir: str = "/app/output",
    hf_token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generate multiple vertical scenes in parallel or sequential batch.
    """
    os.makedirs(output_dir, exist_ok=True)
    batch_id = str(uuid.uuid4())[:8]
    results = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, prompt in enumerate(prompts):
            filename = f"frame_{batch_id}_{index + 1}.jpg"
            filepath = os.path.join(output_dir, filename)
            tasks.append(fetch_single_image(prompt, filepath, session, hf_token))
            
        generated_paths = await asyncio.gather(*tasks, return_exceptions=False)
        
        for idx, (path, prompt) in enumerate(zip(generated_paths, prompts)):
            results.append({
                "index": idx + 1,
                "prompt": prompt,
                "filepath": path,
                "filename": os.path.basename(path)
            })
            
    logger.info(f"Generated {len(results)} visual scenes for batch {batch_id}.")
    return results
