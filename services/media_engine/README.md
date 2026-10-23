# 🎬 Programmatic Media Engine
### Zero-Marginal-Cost Audio, Visual & Video Rendering Microservice

The **Media Engine** is a high-performance Python FastAPI service responsible for end-to-end programmatic generation of vertical short-form video assets (9:16 aspect ratio) for YouTube Shorts and Instagram Reels.

---

## ⚡ Core Capabilities

1. **Neural Voiceover Generation (`/api/generate-voice`)**:
   - Uses `edge-tts` to generate human-grade AI speech.
   - Outputs word-level and sentence-level timing markers for synchronized subtitles.
   - Zero commercial API costs or token constraints.
   - Default Voice: `en-US-ChristopherNeural` (configurable via `DEFAULT_VOICE_MODEL`).

2. **AI Visual Generation (`/api/fetch-images`)**:
   - Queries Pollinations.ai / Hugging Face FLUX inference endpoints.
   - Generates high-resolution vertical visuals (`1080x1920`) from prompt descriptions.

3. **FFmpeg & MoviePy Compositor (`/api/render-video`)**:
   - Automatically stitches background images with smooth dynamic zoom/pan (Ken Burns effect).
   - Normalizes and overlays voiceover audio.
   - Renders center-aligned, high-contrast dynamic burned subtitles.
   - Exports compressed vertical MP4 (`1080x1920`) directly to `./shared_media` volume.

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Healthcheck returning service status. |
| `POST` | `/api/generate-voice` | Ingests `{ "script": "...", "voice": "en-US-ChristopherNeural" }`, produces MP3 and timing metadata. |
| `POST` | `/api/fetch-images` | Ingests `{ "prompts": ["..."] }`, returns array of saved vertical image paths. |
| `POST` | `/api/render-video` | Ingests `{ "images": [...], "audio_path": "...", "script": "..." }`, returns completed MP4 video path. |

---

## 🐳 Docker Deployment

The media engine runs within the `agency-media-engine` container defined in `docker-compose.yml`:

```bash
docker compose up -d media-engine
```

- **Container Port**: `8000`
- **Host Port**: `8000`
- **Shared Volume**: `./shared_media:/app/output`
