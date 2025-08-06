import openai
import os
import datetime
from github import Github

# === ✅ Load Secrets from GitHub ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN_SYSTEM")
REPO_NAME = os.getenv("REPO_NAME_SYSTEM")

# === ✅ Init API Clients ===
openai.api_key = OPENAI_API_KEY
github = Github(GH_TOKEN)
repo = github.get_repo(REPO_NAME)

# === 🔁 Generate Unique Tool with GPT ===
def generate_tool_code():
    today = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    prompt = f"""
You are a powerful AI developer. Generate a highly unique, addictive, and creative AI-based one-page tool in HTML+JavaScript format.
Constraints:
- Must be super simple to use (like a calculator or converter)
- Must not be something already existing or boring
- Should trigger dopamine in users (e.g., generate surprising results)
- Include a minimal UI (centered with a dark mode toggle)
- Embed placeholder for AdSense (<!-- AdSense Here -->)
- Add usage token limit: max 5 uses (add JS alert after 5 uses)
- Must be cleanly formatted in ONE index.html code block

Today's date is: {today}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response['choices'][0]['message']['content']

# === 💾 Save to GitHub ===
def push_tool_to_github(tool_code, tool_name):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"tools/{tool_name}_{now}.html"
    repo.create_file(file_path, f"Add {tool_name}", tool_code, branch="main")

# === 🧠 Main Engine ===
def build_and_push_assets():
    for i in range(15):
        tool_code = generate_tool_code()
        tool_name = f"Tool_{i+1}"
        push_tool_to_github(tool_code, tool_name)
        print(f"✅ {tool_name} deployed successfully.")

# === 🚀 Start ===
if __name__ == "__main__":
    build_and_push_assets()
import update_index
update_index.generate_index()