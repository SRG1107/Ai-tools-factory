import os
import openai
import datetime
from github import Github

# ✅ 1. CONFIGURATION (Auto handled from GitHub Secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GH_TOKEN_SYSTEM")
repo_name = os.getenv("REPO_NAME_SYSTEM")  # e.g., "username/Ai-tools-factory"

# ✅ 2. CONNECT TO GITHUB
github = Github(github_token)
repo = github.get_repo(repo_name)

# ✅ 3. TOOL GENERATOR FUNCTION
def generate_tool_code():
    prompt = """
You are a viral AI tool generator.
Create a never-before-seen, 1-page HTML + JS AI-powered web tool that:
- Solves a unique, dopamine-hitting micro problem
- Clean UI (centered layout, responsive, mobile-first)
- Insert fake AdSense blocks (<!-- ADSENSE HERE -->)
- Include token lock after 5 uses (function lockToolAfterLimit())
- No repeated tools — every tool must feel original
Output full code in one HTML file.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ✅ 4. SAVE TOOL TO GITHUB
def save_tool_to_github(filename, content):
    now = datetime.datetime.now().isoformat()
    file_path = f"tools/{filename}.html"
    commit_message = f"Add new tool {filename} on {now}"
    repo.create_file(file_path, commit_message, content)

# ✅ 5. MAIN: Generate 15 Tools per Run
for i in range(1, 16):
    print(f"🚀 Creating Tool #{i}")
    tool_code = generate_tool_code()
    filename = f"ai_tool_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{i}"
    save_tool_to_github(filename, tool_code)
