"""
Autonomous Dev Bridge Server.
FastAPI service listening on port 8050 for web build tasks dispatched by n8n.
Coordinates Antigravity code generation, build verification, Git tracking,
and emits completion callbacks.
"""

import os
import requests
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from site_scaffolder import scaffold_client_website, slugify
from deployer import verify_compilation, initialize_git_repository, trigger_cloud_deployment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("dev_bridge.server")

app = FastAPI(
    title="Autonomous Web Dev Bridge",
    description="Webhook bridge for automated web scaffolding, testing, Git commits, and cloud deployment.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DEPLOYMENTS_DIR = os.getenv("DEPLOYMENTS_DIR", "./deployments")
os.makedirs(BASE_DEPLOYMENTS_DIR, exist_ok=True)

class WebsiteBriefRequest(BaseModel):
    client_name: str = Field(..., min_length=2, description="Business or brand name")
    niche: Optional[str] = Field("Professional Services", description="Industry or niche")
    tagline: Optional[str] = Field(None, description="Company motto or marketing hook")
    features: Optional[List[str]] = Field(default_factory=list, description="List of key offerings or services")
    phone: Optional[str] = Field("+1234567890", description="WhatsApp business contact phone number")
    email: Optional[str] = Field(None, description="Contact email address")
    callback_url: Optional[str] = Field(None, description="n8n webhook URL to receive completion callback")

def execute_build_and_callback(brief: Dict[str, Any], callback_url: Optional[str]):
    """Background task to scaffold, verify, deploy, and fire callback to n8n."""
    client_name = brief.get("client_name", "Client")
    slug = slugify(client_name)
    logger.info(f"Initiating autonomous web build for '{client_name}' (slug: {slug})...")

    try:
        # 1. Scaffold full React/Vite/Tailwind workspace
        workspace_dir = scaffold_client_website(brief, base_deployments_dir=BASE_DEPLOYMENTS_DIR)

        # 2. Verify compilation integrity
        compile_info = verify_compilation(workspace_dir)

        # 3. Git commit tracking
        git_info = initialize_git_repository(workspace_dir, client_name)

        # 4. Deploy or resolve live preview URL
        deploy_info = trigger_cloud_deployment(workspace_dir, slug, brief)
        live_url = deploy_info.get("live_url", f"https://{slug}.preview.agency.internal")

        payload = {
            "status": "success",
            "client_name": client_name,
            "slug": slug,
            "live_url": live_url,
            "workspace_dir": workspace_dir,
            "verified": compile_info.get("verified", True),
            "deployment": deploy_info
        }

        logger.info(f"Autonomous build complete for '{client_name}'. Live URL: {live_url}")

        # 5. Emit callback webhook back to n8n if callback_url is provided
        target_callback = callback_url or os.getenv("N8N_BUILD_CALLBACK_URL", "http://localhost:5678/webhook/build-complete")
        if target_callback:
            try:
                logger.info(f"Emitting completion callback to: {target_callback}")
                cb_res = requests.post(target_callback, json=payload, timeout=10)
                logger.info(f"Callback responded with status code: {cb_res.status_code}")
            except Exception as cb_err:
                logger.warning(f"Could not reach n8n callback URL ({target_callback}): {cb_err}")

    except Exception as err:
        logger.error(f"Error during autonomous web build: {err}", exc_info=True)
        if callback_url:
            try:
                requests.post(callback_url, json={"status": "error", "client_name": client_name, "error": str(err)}, timeout=10)
            except Exception:
                pass

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {
        "status": "healthy",
        "service": "dev-bridge",
        "deployments_dir": os.path.abspath(BASE_DEPLOYMENTS_DIR)
    }

@app.post("/build-website", status_code=status.HTTP_202_ACCEPTED)
async def build_website(payload: WebsiteBriefRequest, background_tasks: BackgroundTasks):
    """
    Accepts project brief from n8n, starts autonomous build pipeline,
    and returns 202 Accepted immediately while completing in background.
    """
    brief_data = payload.model_dump()
    background_tasks.add_task(execute_build_and_callback, brief_data, payload.callback_url)
    
    return {
        "status": "building",
        "message": f"Autonomous web build started for {payload.client_name}.",
        "slug": slugify(payload.client_name),
        "target_directory": os.path.join(BASE_DEPLOYMENTS_DIR, slugify(payload.client_name))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bridge_server:app", host="0.0.0.0", port=8050, reload=True)
