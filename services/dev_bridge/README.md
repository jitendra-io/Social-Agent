# 🛠️ Autonomous Web Dev Bridge
### Host Integration Service for Antigravity Autonomous Web Engineering

The **Dev Bridge** runs on the host machine to execute autonomous web engineering workflows triggered by n8n or direct Telegram/WhatsApp commands. It coordinates workspace scaffolding, code generation, local compilation testing, Git commits, and cloud deployment.

---

## ⚡ Core Components

1. **`bridge_server.py`**:
   - FastAPI server running on `http://localhost:8050`.
   - Ingests `POST /build-website` requests containing client project briefs.
   - Spawns asynchronous scaffolding and emits completion webhooks back to n8n with the live URL.

2. **`site_scaffolder.py`**:
   - Generates production-grade, mobile-responsive web applications using modern React, Vite, and Tailwind CSS.
   - Embeds SEO meta tags, OpenGraph data, and a direct WhatsApp click-to-chat CTA.
   - Generates and tests project dependencies (`npm install` & `npm run build`).

3. **`deployer.py`**:
   - Manages local Git version control (`git init`, `git add`, `git commit`).
   - Pushes to remote repository and triggers hosting webhooks (Render / Vercel CLI).

---

## 🚀 Running the Dev Bridge

```bash
cd services/dev_bridge
pip install -r requirements.txt
python bridge_server.py
```

- **Listening Port**: `8050`
- **Health Check**: `GET http://localhost:8050/health`
- **Build Trigger**: `POST http://localhost:8050/build-website`
