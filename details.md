# TASK SPECIFICATION & ARCHITECTURAL BLUEPRINT
## Autonomous AI Agency & Multi-Platform Automation Operating System

### 1. MISSION OVERVIEW & ROLE
You are operating as an Autonomous Staff Systems Architect and Full-Stack Engineering Agent. Your mission is to build and deploy an end-to-end autonomous business operations engine combining:
1. **n8n (Self-Hosted/Docker)** as the event router, scheduler, webhook listener, and social API coordinator.
2. **Google Antigravity** as the autonomous software engineer that writes, tests, and deploys custom landing pages/websites via Git.
3. **Telegram Bot API** as the primary executive mobile interface (command center, preview cards, interactive inline buttons, and strategic advisories).
4. **Local Microservices (Python/FFmpeg/Edge-TTS)** for zero-cost media generation and programmatic video rendering.
5. **WhatsApp Business Cloud API** for automated inbound client qualification and project intake.

You will create all required codebase files, workflow definition files, microservice endpoints, Docker orchestration configs, and integration bridges directly in this workspace.

---

### 2. CORE ARCHITECTURE & SYSTEM TOPOLOGY

┌─────────────────────────────────────────┐
                │      Executive Command UI (Telegram)    │
                │   Commands | Approvals | Next-Step Tips │
                └───────────────────▲─────────────────────┘
                                    │
                     Bidirectional Webhook Bridge
                                    │
                                    ▼
                ┌─────────────────────────────────────────┐
                │            n8n Orchestrator             │
                │       (Docker Container / Port 5678)    │
                └───────┬───────────┬─────────────┬───────┘
                        │           │             │
    ┌───────────────────┘           │             └───────────────────┐
    ▼                               ▼                                 ▼
    ┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
│ Media Engine (Python) │   │ Social & Chat Routing │   │ Dev Agent Bridge      │
│ • Pollinations/FLUX   │   │ • YouTube / X / IG    │   │ • Local webhook agent │
│ • Edge-TTS Voiceover  │   │ • WhatsApp Cloud API  │   │ • Triggers Antigravity│
│ • FFmpeg Video Render │   │ • Supabase / Postgres │   │ • Git commit & push   │
└───────────────────────┘   └───────────────────────┘   └───────────┬───────────┘
│
▼
┌───────────────────────┐
│ Auto-Deployment Cloud │
│ (Render / Vercel CLI) │
└───────────────────────┘

---

### 3. IMPLEMENTATION WORKSTREAMS

#### Workstream A: Containerized Infrastructure Setup
Create a production-ready `docker-compose.yml` file establishing the local operating stack:
1. **Service: `n8n`**
   - Image: `n8nio/n8n:latest`
   - Ports: `5678:5678`
   - Volumes: Local volume mount for persistent workflows and credentials (`./n8n_data:/home/node/.n8n`), plus a shared asset volume (`./shared_media:/data/shared`).
   - Environment: `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`, `WEBHOOK_URL=http://localhost:5678/`.
2. **Service: `media-engine`**
   - Build context: `./services/media_engine` (Python 3.11).
   - Exposed Port: `8000:8000`.
   - Dependencies: `fastapi`, `uvicorn`, `edge-tts`, `moviepy`, `ffmpeg-python`, `requests`, `pydantic`.
   - Volumes: `./shared_media:/app/output`.
3. **Service: `database`**
   - Image: `postgres:16-alpine`
   - Ports: `5432:5432`
   - Schema Initialization Script (`init.sql`) tracking:
     - `posts` table (`id`, `platform`, `topic`, `caption`, `media_url`, `status`, `scheduled_at`, `analytics_data`).
     - `leads` table (`id`, `source`, `business_name`, `phone`, `email`, `requirements`, `site_status`, `site_url`).
     - `conversations` table (`session_id`, `user_id`, `context_history`, `last_state`).

#### Workstream B: Python Programmatic Video & Asset Pipeline (`services/media_engine`)
Create a FastAPI microservice containing the following endpoints:
1. `POST /api/generate-voice`:
   - Accepts text script, language, and voice model (e.g., `en-US-ChristopherNeural` or `en-US-EricNeural` via `edge-tts`).
   - Generates and outputs an MP3 file with precise word-level timestamps.
2. `POST /api/fetch-images`:
   - Uses zero-cost AI image endpoints (Pollinations API / Hugging Face FLUX inference) using prompt-engineered visual descriptions to generate 9:16 vertical images.
3. `POST /api/render-video`:
   - Accepts image paths, audio path, script text, and subtitle styling rules.
   - Uses FFmpeg/MoviePy to:
     - Combine images with smooth zoom/pan (Ken Burns effect).
     - Layer the voiceover audio track.
     - Automatically render high-contrast, center-aligned dynamic subtitles.
     - Export vertical MP4 (`1080x1920`) to the shared media volume.
4. `GET /health`: Basic healthcheck endpoint.

#### Workstream C: Telegram Executive Interface & Interactive n8n Workflows
Build and export standard JSON workflow templates ready to import into n8n:
1. **Workflow 1: Telegram Command Dispatcher (`telegram_dispatcher.json`)**
   - **Trigger:** Telegram Trigger node listening to messages.
   - **Security Filter:** Validates incoming message `from.id` against an authorized administrator `TELEGRAM_ADMIN_ID`.
   - **LLM Intent Classifier:** Routes commands (`/post`, `/leadgen`, `/buildsite`, or free text) to appropriate sub-workflows.
2. **Workflow 2: Social Media Content Creator & Review Gate (`social_pipeline.json`)**
   - **Trigger:** Daily Cron schedule (e.g., 09:00 AM) or Telegram manual trigger.
   - **Generation:** LLM produces 3 hook variations, video script, hashtags, and visual prompts.
   - **Rendering:** Calls the local `media-engine` container to assemble video/carousel assets.
   - **Interactive Telegram Card:** Sends the rendered media to Telegram using an Inline Keyboard markup:
     - Row 1: `[ ✅ Approve & Schedule ]` `[ ✏️ Edit Caption ]`
     - Row 2: `[ 🔄 Regenerate Video ]` `[ 💡 Suggest Next Step ]`
3. **Workflow 3: Telegram Callback Query Handler (`callback_handler.json`)**
   - **Trigger:** Telegram Trigger on `callback_query`.
   - **Acknowledgement:** Immediately fires `answerCallbackQuery` to clear the Telegram loading spinner.
   - **Switch Routing:**
     - `action_approve`: Updates Postgres status to `approved`, schedules posting node.
     - `action_edit`: Flags session state in Postgres to listen for next user message as the replacement caption.
     - `action_suggest`: Prompts LLM to analyze content and suggest repurposing ideas (e.g., turning a Reel into a LinkedIn text carousel).
4. **Workflow 4: Multi-Platform Publisher (`social_publisher.json`)**
   - Cron-triggered runner querying scheduled posts from Postgres.
   - **YouTube Shorts:** Uses YouTube Data API v3 (`videos.insert`) with media binary stream.
   - **Instagram Reels:** Uses Meta Graph API (creates media container -> checks upload status -> publishes container).
   - **Twitter/X:** Uses X API v2 (media upload chunked endpoint + tweet create endpoint).
   - Sends Telegram alert upon verified publication with live URLs.

#### Workstream D: WhatsApp Inbound AI Lead Qualifier (`whatsapp_agent.json`)
1. **Trigger:** Webhook receiver for Meta WhatsApp Cloud API events.
2. **Verification Handler:** Handles webhook challenge token verification (`hub.challenge`).
3. **Conversational Engine:**
   - Evaluates incoming message against conversation state in Postgres.
   - Extracts: Client business name, industry niche, requested features, color/brand preferences, and contact info.
4. **Handoff / Trigger:** Once requirements are gathered:
   - Saves lead with status `ready_for_build` in Postgres.
   - Dispatches a webhook to the Antigravity workspace bridge containing the project brief.
   - Sends notification to Telegram: *"New website build request received for [Business Name]. Starting Antigravity build..."*

#### Workstream E: Autonomous Antigravity Website Dev Bridge (`services/dev_bridge`)
Create a lightweight bridge script (`bridge_server.py`) running in this environment:
1. **Endpoint `POST /build-website`:**
   - Accepts JSON payload from n8n: `{ "client_name": "...", "niche": "...", "features": [...], "theme": "..." }`.
   - Generates a target workspace under `./deployments/<client_name>`.
2. **Antigravity Autonomous Task Invocation:**
   - Scaffolds a modern static site (Vite + React + Tailwind CSS or single-file interactive landing page).
   - Injects SEO meta tags, responsive mobile layouts, hero section, pricing table, and a functional WhatsApp direct-contact button.
   - Executes build check (`npm run build`).
3. **Auto-Deploy & Callback:**
   - Initializes Git, makes initial commit: `feat: initial automated client build`.
   - Pushes to GitHub via GitHub CLI / Personal Access Token or triggers Vercel/Render deployment CLI.
   - Emits an outbound webhook back to n8n:
     ```json
     {
       "status": "success",
       "client_name": "BrewLab",
       "live_url": "[https://brewlab-preview.onrender.com](https://brewlab-preview.onrender.com)"
     }
     ```
   - n8n receives this webhook and automatically messages both your Telegram and the client's WhatsApp with the live link.

---

### 4. DELIVERABLE REQUIREMENTS & DIRECTIVES

When fulfilling this task:
1. **Write clean, executable code** for all files (`docker-compose.yml`, Python FastAPI endpoints, FFmpeg rendering scripts, SQL schemas, and JSON workflow definitions).
2. **Include comprehensive error handling:** Implement API rate-limit delays, input validation via Pydantic, and fallback states if an API times out.
3. **Ensure strict environment variable isolation:** Create an `.env.example` file documenting every required secret (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_ID`, `YOUTUBE_API_KEY`, `META_ACCESS_TOKEN`, `TWITTER_API_KEYS`, `POSTGRES_CREDENTIALS`).
4. **Provide clear startup commands:** Include the exact terminal steps to bring up the containers, run the bridge server, and verify all webhook connections.

Proceed to scaffold and write the entire system implementation now.