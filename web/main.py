from web.database import save_changelog, get_changelog, get_stats
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
import uuid


from core.github_fetcher import fetch_commits
from core.changelog_generator import generate_changelog
from web.database import save_changelog, get_changelog

app = FastAPI()

templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="landing.html", context={})

@app.get("/app", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": None})

@app.post("/generate")
async def generate(
    request: Request,
    repo_url: str = Form(...),
    since_date: str = Form(...),
    until_date: str = Form(...)
):
    try:
        since = datetime.fromisoformat(since_date).replace(tzinfo=timezone.utc)
        until = datetime.fromisoformat(until_date).replace(tzinfo=timezone.utc)

        commits = fetch_commits(repo_url, since, until)

        if not commits:
            return templates.TemplateResponse(request=request, name="index.html", context={
                "error": "No commits found in that date range."
            })

        repo_name = repo_url.rstrip("/").split("/")[-1]
        result = generate_changelog(commits, repo_name)

        slug = str(uuid.uuid4())[:8]
        save_changelog(slug, repo_url, repo_name, result)

        return RedirectResponse(f"/c/{slug}", status_code=303)

    except Exception as e:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "error": f"Something went wrong: {str(e)}"
        })

@app.get("/c/{slug}", response_class=HTMLResponse)
async def view_changelog(request: Request, slug: str):
    data = get_changelog(slug)
    if not data:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "error": "Changelog not found."
        })
    return templates.TemplateResponse(request=request, name="changelog.html", context=data)

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, key: str = ""):
    if key != os.environ.get("ADMIN_KEY", "changeme"):
        return HTMLResponse("<h1 style='font-family:monospace;padding:40px'>Access denied.</h1>", status_code=403)
    stats = get_stats()
    return templates.TemplateResponse(request=request, name="admin.html", context={"stats": stats})
