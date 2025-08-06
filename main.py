#!/usr/bin/env python3
import os
import sys
from github import Github
from dotenv import load_dotenv

# Optional: Load local .env for dev environment
load_dotenv()

def load_environment():
    """Load and validate all required environment variables."""
    config = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GH_TOKEN": os.getenv("GH_TOKEN"),  # Expect GH_TOKEN from GitHub Secrets
        "REPO_NAME": os.getenv("GITHUB_REPOSITORY")  # Automatically set by GitHub Actions
    }

    # Check for missing vars
    missing = [key for key, value in config.items() if not value]
    if missing:
        print(f"⛔ Missing environment variables: {missing}")
        print("🛠️ Make sure they're set in GitHub Secrets or in your .env file")
        sys.exit(1)

    return config

class GitHubManager:
    def __init__(self, token: str, repo_name: str):
        print(f"🔐 Connecting to GitHub repo: {repo_name}")
        try:
            self.gh = Github(token)
            self.repo = self.gh.get_repo(repo_name)
            print("✅ GitHub repository access confirmed.")
        except Exception as e:
            print(f"❌ GitHub access failed: {e}")
            print("🔎 Solutions:")
            print("1. Verify the repo exists: https://github.com/" + repo_name)
            print("2. Ensure your GH_TOKEN has correct 'repo' permissions")
            sys.exit(1)

# Your main tool-building logic goes here
def build_ai_tools():
    print("🛠️ Starting AI tool generation...")
    # Replace the print statements with real functionality later
    print("🤖 Tool 1 built")
    print("🤖 Tool 2 built")
    print("✅ All tools generated and deployed successfully.")

if __name__ == "__main__":
    try:
        env = load_environment()
        gh_manager = GitHubManager(env["GH_TOKEN"], env["REPO_NAME"])

        # Optional: Debug mode toggle
        debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
        if debug_mode:
            print("🐞 Debug mode enabled.")

        build_ai_tools()

    except Exception as e:
        print(f"⛔ Critical failure: {e}")
        sys.exit(1)