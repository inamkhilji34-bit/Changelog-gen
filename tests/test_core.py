from dotenv import load_dotenv
from github import Github
from datetime import datetime, timezone
import os

load_dotenv()

# --- TEST: Connect to GitHub and fetch commits ---
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo("tiangolo/fastapi")
print(f"✅ GitHub connected! Repo: {repo.full_name}")

commits = repo.get_commits(
    since=datetime(2024, 10, 1, tzinfo=timezone.utc),
    until=datetime(2024, 10, 15, tzinfo=timezone.utc)
)

commit_list = list(commits[:5])
print(f"✅ Fetched {len(commit_list)} commits")
for c in commit_list:
    print(f"  → {c.sha[:7]} {c.commit.message[:60]}")