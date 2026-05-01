from github import Github
from datetime import datetime
import os

def fetch_commits(repo_url: str, since: datetime, until: datetime) -> list[dict]:
    g = Github(os.environ.get("GITHUB_TOKEN"))
    
    parts = repo_url.rstrip("/").split("/")
    owner, repo_name = parts[-2], parts[-1]
    
    repo = g.get_repo(f"{owner}/{repo_name}")
    commits = repo.get_commits(since=since, until=until)
    
    result = []
    for commit in commits:
        msg = commit.commit.message.strip()
        if msg.startswith("Merge") or len(msg) < 5:
            continue
        result.append({
            "sha": commit.sha[:7],
            "message": msg.split("\n")[0],
            "author": commit.commit.author.name,
            "date": commit.commit.author.date.isoformat(),
        })
    
    return result