# OPERATIONAL RUNBOOK: AUTONOMOUS AI DIGITAL AGENCY OS
### Complete Setup, Ingress, Publishing & Operational Guide

---

## 🛠️ 1. Architecture Stack At A Glance

- **Central Orchestrator:** n8n (Docker container `agency-n8n` on port `5678`)
- **Database:** MySQL 8.0 (Docker container `agency-database` on host port `3307` & container port `3306`)
- **Zero-Cost Media Engine:** Python 3.11 + Edge-TTS + Pollinations.ai FLUX + FFmpeg (Docker container `agency-media-engine` on port `8000`)
- **Autonomous Web Dev Bridge:** Python FastAPI service on host port `8050` (Scaffolds React/Vite/Tailwind landing pages + WhatsApp CTAs)
- **Executive Mobile UI:** Telegram Bot API (`@RJ_jitendrabot`, User Chat ID: `8226006494`)
- **Social Publishing:** YouTube Shorts (API v3) + Instagram Reels (`@spendwith.ai`, ID: `17841425833721941`)
- **Comment Auto-Responder:** Meta Webhook &rarr; Gemini AI Nova &rarr; Post IG Reply &rarr; MySQL Memory &rarr; Telegram Admin Alert

---

## 🚀 2. Quickstart Deployment Guide

### Step 1: Clone & Configure Secrets
Copy the environment template:
```bash
cp .env.example .env
```
Ensure the following are set in `.env`:
1. `TELEGRAM_BOT_TOKEN`: Token for `@RJ_jitendrabot` from `@BotFather`
2. `TELEGRAM_ADMIN_ID`: `8226006494`
3. `GEMINI_API_KEY`: API Key from Google AI Studio (see Section 5 below)
4. `INSTAGRAM_ACCOUNT_ID`: `17841425833721941`
5. `INSTAGRAM_ACCESS_TOKEN`: Valid Meta Graph API access token
6. `MYSQL_ROOT_PASSWORD` & `MYSQL_PASSWORD`: Passwords configured in `docker-compose.yml`

---

### Step 2: Start the Core Containerized Stack
Run Docker Compose from the root workspace directory:
```bash
docker compose up -d --build
```
This automatically boots:
- `agency-database`: MySQL 8.0 with `init.sql` executed (creates `posts`, `leads`, `conversations`, `executive_memory`).
- `agency-media-engine`: Python 3.11 with FFmpeg, Edge-TTS, and FLUX image generation.
- `agency-n8n`: Automation orchestrator running on `http://localhost:5678`.

Verify container status:
```bash
docker ps
```

---

### Step 3: Start the Autonomous Web Dev Bridge
The Dev Bridge runs on your host machine to directly control Git, Node, and local file scaffolding:
```bash
python services/dev_bridge/bridge_server.py
```
*Listens on `http://localhost:8050`.*

---

### Step 4: Start Cloudflare Webhook Ingress Tunnel
To receive live inbound Telegram, WhatsApp, and Meta Instagram webhooks on your local machine:
```powershell
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:5678
```
Take note of the resulting public URL (e.g. `https://<random-subdomain>.trycloudflare.com`).

#### Synchronize Telegram Webhook:
Run the following to route Telegram bot updates directly into n8n:
```bash
python -c "import os, urllib.request; from dotenv import load_dotenv; load_dotenv(); token=os.environ.get('TELEGRAM_BOT_TOKEN'); url = f'https://api.telegram.org/bot{token}/setWebhook?url=https://<your-tunnel-url>/webhook/tg-webhook-dispatcher/webhook'; print(urllib.request.urlopen(url).read().decode())"
```

---

## 📸 3. Meta Instagram Webhook Configuration (Comment Auto-Responder)

To enable Nova to automatically reply to comments on your Instagram Reels:

1. Open your **[Meta for Developers](https://developers.facebook.com/)** App Dashboard.
2. Under **Products**, select **Instagram Platform** ➔ **Webhooks** (or navigate to Webhooks ➔ Instagram).
3. Enter the Webhook details:
   - **Callback URL**: `https://<your-tunnel-url>/webhook/instagram-webhook`
   - **Verify Token**: `agency_nova_secure_token_2026`
4. Click **Verify and save**. Meta will challenge the endpoint, and n8n will immediately return HTTP 200 with the challenge string.
5. In the **Subscription Fields** list:
   - Find **`comments`** and click **Subscribe** (Active).
   - *(Optional)* Find **`mentions`** and click **Subscribe**.

---

## 📱 4. Executive Operation Runbook (Telegram Commands)

As the Executive Director, command the entire agency system via `@RJ_jitendrabot`:

| Command | Action | Description |
| :--- | :--- | :--- |
| `/status` | **System Health** | Checks MySQL connectivity, media engine status, and recent post counts. |
| `/post <topic>` | **Content Generation** | Triggers AI scriptwriting, Edge-TTS audio, FLUX imagery, and FFmpeg video compositing. |
| `/remember <rule>` | **Store Memory** | Permanently commits a business directive or preference into MySQL memory (importance score 9). |
| `/recall <query>` | **Search Memory** | Performs a text search over stored executive memories. |
| `/buildsite <name>` | **Autonomous Website** | Scaffolds and compiles a bespoke React + Tailwind landing page via the Dev Bridge. |

### Interactive Approval Buttons
When a draft asset is ready, n8n sends a vertical video preview to Telegram with one-tap inline controls:
- `[ ✅ Approve & Post ]`: Triggers `social_publisher.json` to publish to YouTube Shorts & Instagram Reels.
- `[ ✏️ Edit Caption ]`: Prompts for a revised caption.
- `[ 🔄 Regenerate ]`: Generates an alternative hook and re-renders the media.
- `[ 💡 Suggest Next Step ]`: Prompts Nova to provide cross-platform repurposing advice.

---

## 🧠 5. Upgrading to Gemini Pro (`ur.jitendra.io@gmail.com`)

Using Gemini Pro through your Google account (`ur.jitendra.io@gmail.com`) provides higher rate limits, superior reasoning, and persistent memory across chats:

### Generating Your Gemini API Key:
1. Navigate to **[Google AI Studio](https://aistudio.google.com/)**.
2. Sign in with **`ur.jitendra.io@gmail.com`**.
3. Click **Get API key** &rarr; **Create API key in new project**.
4. Copy the resulting key (`AIzaSy...`).
5. Open your `.env` file and replace `GEMINI_API_KEY`:
   ```env
   GEMINI_API_KEY=AIzaSyYourGeneratedProKeyHere
   ```
6. Restart n8n:
   ```bash
   docker restart agency-n8n
   ```

### Why Nova Remembers Chats:
- **Persistent Long-Term Memory**: The Telegram Dispatcher and Comment Bot log conversations and directives into `executive_memory` in MySQL.
- **Dynamic Context Injection**: Every conversational query fetches top-ranked memories and past conversation turns from MySQL, injecting them directly into the Gemini prompt context.
- **Gemini Pro 1M+ Context**: Gemini Pro supports up to 1 Million - 2 Million tokens in context, allowing Nova to ingest weeks of ongoing business dialogue, client intake requirements, and creative ideas without forgetting anything.
