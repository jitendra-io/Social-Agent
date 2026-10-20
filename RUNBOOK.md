# OPERATIONAL RUNBOOK: AUTONOMOUS AI DIGITAL AGENCY OS

This runbook details how to boot, configure, test, and operate the autonomous digital agency ecosystem.

---

## 🛠️ 1. Architecture Stack At A Glance

- **Central Orchestrator:** n8n (Community Edition, Docker container on port `5678`)
- **Database:** MySQL 8.0 (InnoDB + native JSON, Docker container on port `3306`)
- **Zero-Cost Media Engine:** Python 3.11 + Edge-TTS + Pollinations.ai FLUX + FFmpeg (Docker container on port `8000`)
- **Autonomous Web Dev Bridge:** Python FastAPI service on host port `8050` (Scaffolds React/Vite/Tailwind landing pages + WhatsApp CTAs)
- **Executive Mobile UI:** Telegram Bot API (Inline cards: Approve, Edit Caption, Regenerate, Strategic Next Step)
- **Inbound Client Funnel:** Meta WhatsApp Business Cloud API (Automated qualification & build dispatch)

---

## 🚀 2. Quickstart Deployment Guide

### Step 1: Clone & Configure Secrets
Copy the environment template:
```bash
cp .env.example .env
```
Open `.env` and fill in:
1. `TELEGRAM_BOT_TOKEN`: From `@BotFather`
2. `TELEGRAM_ADMIN_ID`: Your Telegram numeric User ID from `@userinfobot`
3. `GEMINI_API_KEY`: Free key from Google AI Studio (`https://aistudio.google.com/`)
4. `MYSQL_ROOT_PASSWORD` & `MYSQL_PASSWORD`: Secure database passwords

---

### Step 2: Start the Core Containerized Stack
Run Docker Compose from the root workspace directory:
```bash
docker compose up -d --build
```
This automatically boots:
- `agency-database`: MySQL 8.0 with `init.sql` executed (creates `posts`, `leads`, `conversations`).
- `agency-media-engine`: Python 3.11 with FFmpeg and TTF fonts for video compositing.
- `agency-n8n`: Workflow automation orchestrator connected to MySQL.

Verify running containers:
```bash
docker compose ps
```

---

### Step 3: Start the Autonomous Web Dev Bridge
The Dev Bridge runs on your host machine so it has direct access to Git, Node, and local file scaffolding:
```bash
cd services/dev_bridge
pip install -r requirements.txt
python bridge_server.py
```
*The bridge will start listening on `http://localhost:8050`.*

---

### Step 4: Import Workflows into n8n
1. Open your browser to `http://localhost:5678`.
2. Complete the initial local account setup.
3. In the left navigation, click **Workflows** &rarr; **Add Workflow** &rarr; **Import from File**.
4. Import the 6 production workflow templates from the `workflows/` directory:
   - `telegram_dispatcher.json`
   - `social_pipeline.json`
   - `callback_handler.json`
   - `social_publisher.json`
   - `whatsapp_agent.json`
   - `analytics_feedback.json`
5. Activate each workflow using the toggle in the upper-right corner.

---

### Step 5: Configure Webhook Ingress (For Live Telegram & WhatsApp Events)
To receive inbound Meta WhatsApp and Telegram webhooks on your local machine, run a free tunnel (e.g. Cloudflare Tunnel or ngrok):
```bash
# Using ngrok:
ngrok http 5678
```
Set `WEBHOOK_URL` in your `.env` to your tunnel URL (e.g., `https://your-tunnel.ngrok-free.app/`) and restart n8n:
```bash
docker compose restart n8n
```

---

## 📱 3. Executive Operation Runbook (Telegram Commands)

As the Executive Director, you command the entire system via your personal Telegram chat:

| Command | Action | Description |
| :--- | :--- | :--- |
| `/status` | **System Health** | Checks MySQL connectivity, total post counts, and active services. |
| `/post <topic>` | **Content Generation** | Triggers AI scriptwriting, Edge-TTS audio, Pollinations FLUX images, and FFmpeg video compositing. |
| `/buildsite <name>` | **Autonomous Website** | Triggers the Dev Bridge to scaffold and compile a bespoke React + Tailwind landing page. |

### Interactive Approval Buttons
When a draft asset is ready, n8n sends a vertical video preview with one-tap inline controls:
- **`[ ✅ Approve & Post ]`**: Schedules immediate multi-channel distribution to YouTube Shorts, Instagram Reels, and X/Twitter.
- **`[ ✏️ Edit Caption ]`**: Activates a stateful listener; send your replacement caption in your next message.
- **`[ 🔄 Regenerate ]`**: Re-triggers media generation with fresh visual prompt seeds.
- **`[ 💡 Suggest Next Step ]`**: Asks Gemini for strategic repurposing recommendations (e.g., carousel slides, X thread).

---

## 🧪 4. Smoke Testing & Verification

A dedicated automated test script is provided in `test_system.py`:
```bash
python test_system.py
```
This tests:
1. `services/dev_bridge`: Scaffolds a complete responsive landing page into `./deployments/test-agency`.
2. `services/media_engine`: Validates synthetic speech generation and image fetching.
3. Database schema verification.
