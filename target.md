# MISSION BRIEF: AUTONOMOUS AI DIGITAL AGENCY & OPERATIONS OS

Building all these for free.

## 1. Executive Objective
Your objective is to design, scaffold, and implement a fully automated digital business ecosystem. You are transitioning operational workflows from manual execution across disparate SaaS tools into a self-contained, zero-cost autonomous pipeline. In this ecosystem:
- You operate exclusively as the **Executive Director** through a personal Telegram chat interface.
- **n8n** serves as the central orchestrator, scheduler, webhook receiver, and integration bridge.
- **Google Antigravity** operates as the autonomous software engineering engine responsible for generating, testing, and shipping web applications.
- **Local containerized microservices** handle programmatic media generation (audio, images, and video rendering).
- **Meta's WhatsApp Business Cloud API** acts as the automated client acquisition and intake portal.

The entire architecture must rely strictly on open-source software, self-hosted containers, free-tier developer APIs (Gemini/Groq, Pollinations/Hugging Face), and open system utilities (FFmpeg, Edge-TTS).

---

## 2. Target Deliverables & System Components

### Component A: Unified Command & Approval UI (Telegram)
Build a two-way command interface using the Telegram Bot API:
1. **Administrative Security Gate:** Strict verification validating that incoming commands match an authorized administrative user ID (`TELEGRAM_ADMIN_ID`).
2. **Interactive Preview Cards:** Rather than blind auto-posting, the system must deliver draft assets (rendered vertical MP4 videos, carousel previews, and captions) directly to Telegram.
3. **Inline Action Engine:** Interactive keyboards providing one-tap controls:
   - `[ ✅ Approve & Post ]`: Updates database status to scheduled/published.
   - `[ ✏️ Edit Caption ]`: Activates a stateful listener to receive a revised text prompt.
   - `[ 🔄 Regenerate ]`: Retriggers asset generation with alternative parameters.
   - `[ 💡 Suggest Next Step ]`: Prompts the AI brain to analyze performance and suggest cross-platform repurposing strategies.

### Component B: Programmatic Media Engine (`services/media_engine`)
Scaffold a local Python FastAPI microservice capable of zero-marginal-cost asset production:
1. **Scripting & Prompt Generation:** LLM generation of viral hooks, 30–60 second scripts, hashtags, and visual prompts.
2. **Text-to-Speech (`edge-tts`):** Generate high-fidelity neural audio voiceovers with sentence- and word-level timing markers without commercial API rate limits.
3. **AI Image Generation:** Ingest prompts to produce vertical 9:16 background visuals via free endpoints (Pollinations.ai / Hugging Face FLUX inference).
4. **Programmatic Video Assembly (`FFmpeg` / `MoviePy`):** An automated pipeline that:
   - Concatenates visual assets with subtle pan/zoom animations.
   - Blends and normalizes the voiceover track.
   - Transcribes and burns high-contrast, center-aligned subtitles into the video container.
   - Renders production-ready vertical MP4s (`1080x1920`) saved to a shared Docker volume.

### Component C: Multi-Platform Publishing & Feedback Engine
Implement n8n workflows that distribute content across major platforms and close the performance loop:
1. **Multi-Channel Dispatch:**
   - **YouTube Shorts:** Binary upload via YouTube Data API v3 (`videos.insert`).
   - **Instagram Reels:** Container initialization, upload verification, and publishing via Meta Graph API.
   - **X (Twitter):** Chunked media upload and tweet distribution via X API v2.
2. **Feedback & Strategy Loop:**
   - A 24-hour cron job queries platform analytics (views, watch time, shares, saves).
   - An LLM evaluates performance against baseline historical metrics.
   - The engine sends an analytical debrief to Telegram detailing what succeeded and offering immediate next steps (e.g., converting a high-retention video into a multi-slide carousel).

### Component D: Inbound Client Funnel (WhatsApp Business)
Build an automated client intake pipeline powered by n8n:
1. Receive inbound prospect messages via the WhatsApp Business Cloud API.
2. Use an AI Agent node backed by conversational memory to qualify leads, introduce agency capabilities, and gather site requirements (business niche, target color schemes, required pages, and contact details).
3. Record the prospect record in PostgreSQL with a state flag: `ready_for_build`.
4. Package the client requirements into a structured JSON project brief.
5. Automatic messaging anyone through whatsaap.

### Component E: Autonomous Web Engineering Bridge (Antigravity)
Integrate Antigravity as the autonomous web developer:
1. **Bridge Server (`services/dev_bridge`):** A webhook listener that accepts the project brief from n8n.
2. **Workspace Scaffolding:** Initialize a modern frontend workspace (Vite + React + Tailwind CSS).
3. **Autonomous Execution:**
   - Antigravity ingests the brief, generates clean UI components, adds SEO meta tags, builds responsive layouts, and embeds a direct WhatsApp click-to-chat CTA.
   - Runs automated builds (`npm run build`) to verify compilation and UI integrity.
4. **Continuous Deployment:** Initializes a local Git repository, commits the code, pushes to a remote repository (GitHub), and triggers hosting deployment on platforms like Render or Vercel.
5. **Handoff Callback:** Emits a completion webhook back to n8n containing the production URL, prompting n8n to send the preview link simultaneously to your Telegram chat and to the client's WhatsApp thread.

---

## 3. Implementation Directives
- Generate complete, production-ready source files including `docker-compose.yml`, FastAPI microservice scripts, FFmpeg editing modules, database schemas (`init.sql`), and n8n workflow definitions.
- Provide clear deployment and startup procedures, ensuring all volume bindings, networking paths, and environment variable references are fully configured.
