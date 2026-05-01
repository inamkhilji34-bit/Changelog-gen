# Changelog Generator

Turn messy git commits into clean, human-readable release notes — powered by AI.

🔗 **Live demo:** https://web-production-17ca2.up.railway.app

---

## What it does

Paste any public GitHub repository URL, pick a date range, and get a beautifully
formatted changelog in seconds. No more manually writing release notes.

**Before** (raw git commits):
a3f92bc fix: resolve null pointer exception in auth middleware
d8e21aa feat: add redis caching layer
c19f334 chore: bump dependencies
e82a1bc Merge pull request #234

**After** (your changelog):
> **New features**
> → Dramatically improved page load speeds with intelligent caching
>
> **Bug fixes**  
> → Fixed a crash that occurred when logging in with certain email formats

---

## How it works

1. Paste a GitHub repository URL
2. Select a date range
3. Get a shareable changelog page instantly

---

## Tech stack

- **Backend:** Python, FastAPI
- **AI:** Groq API (Llama 3.1)
- **Database:** SQLite
- **Deployment:** Railway

---

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/changelog-gen.git
cd changelog-gen
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (use `.env.example` as template):
GITHUB_TOKEN=your_github_pat
GROQ_API_KEY=your_groq_key
SECRET_KEY=any_random_string

Start the server:
```bash
uvicorn web.main:app --reload
```

Open http://localhost:8000

---

## Roadmap

- [ ] GitHub OAuth login
- [ ] Multiple repo support
- [ ] Auto-generate on every release via webhooks
- [ ] Export to Markdown / PDF
- [ ] Custom branding for teams

---

Built by [inamkhilji34-bit](https://github.com/inamkhilji34-bit)