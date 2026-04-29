from groq import Groq
import json
import os

def generate_changelog(commits: list[dict], repo_name: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    commits_text = "\n".join([
        f"- [{c['sha']}] {c['message']} (by {c['author']})"
        for c in commits
    ])
    
    prompt = f"""You are a technical writer generating a user-facing changelog for "{repo_name}".

Here are the raw git commits:
{commits_text}

Your job:
1. IGNORE: dependency bumps, typo fixes, merge commits, CI changes, version bumps
2. GROUP into categories (only include if items exist):
   - New features
   - Improvements
   - Bug fixes
   - Breaking changes
3. REWRITE each commit in plain English a non-developer would understand
4. Skip commits too vague to rewrite meaningfully

Return ONLY valid JSON, no other text:
{{
  "summary": "One sentence describing the most important changes",
  "categories": {{
    "New features": [],
    "Improvements": [],
    "Bug fixes": [],
    "Breaking changes": []
  }},
  "commit_count_processed": 0,
  "commit_count_included": 0
}}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    return json.loads(raw)