import sys
sys.path.append(r"D:\changelog\changelog-gen")
from dotenv import load_dotenv
from datetime import datetime, timezone
from core.github_fetcher import fetch_commits
from core.changelog_generator import generate_changelog
import os

load_dotenv(dotenv_path=r"D:\changelog\changelog-gen\.env")

print("Fetching commits...")
commits = fetch_commits(
    "https://github.com/tiangolo/fastapi",
    since=datetime(2024, 10, 1, tzinfo=timezone.utc),
    until=datetime(2024, 10, 15, tzinfo=timezone.utc)
)
print(f"✅ Fetched {len(commits)} commits")

print("\nGenerating changelog...")
result = generate_changelog(commits, "FastAPI")

print(f"✅ Done!\n")
print(f"Summary: {result['summary']}\n")
for category, items in result['categories'].items():
    if items:
        print(f"{category}:")
        for item in items:
            print(f"  → {item}")