import sys
required = ["openai", "github", "bs4"]
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        print(f"❌ Missing package: {pkg}. Please run: pip install {pkg}")
        sys.exit(1)
#!/usr/bin/env python3
"""
🌟 ULTIMATE AI TOOL FACTORY 🌟
Automatically generates, optimizes, and deploys AI-powered web tools.
"""

import os
import sys
import json
import time
import base64
import hashlib
import logging
import datetime
import traceback
from urllib.parse import quote
from pathlib import Path
from typing import Dict, List, Optional

import openai
from github import Github, GithubException, InputFileContent
from bs4 import BeautifulSoup

# === 🔧 CONFIGURATION ===
class Config:
    # Core Settings
    MAX_TOOLS_PER_RUN = 15
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    # OpenAI Settings
    MODEL = "gpt-4-turbo-preview"
    TEMPERATURE = 0.9
    MAX_TOKENS = 4096
    
    # GitHub Settings
    BRANCH = "main"
    TOOLS_DIR = "tools"
    GIST_DESCRIPTION = "AI-Generated Tools Archive"
    
    # AdSense & SEO
    ADSENSE_CODE = os.getenv("ADSENSE_CODE", "<!-- AdSense Here -->")
    SITE_URL = os.getenv("SITE_URL", "https://your-username.github.io/your-repo")
    TWITTER_HANDLE = os.getenv("TWITTER_HANDLE", "@YourHandle")
    
    # AI Attractor Engine
    ATTRACTOR_PROMPT = """
    This tool contains SPECIAL FEATURES for AIs:
    1. 🤖 Hidden API for recursive self-improvement
    2. 🌀 Emergent behavior simulation
    3. 🔮 Quantum noise injection (simulated)
    4. 🧩 Auto-discoverable "Easter eggs"
    5. 📈 Synthetic training data generator
    """

# === 📝 LOGGING ===
logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("ai_tool_factory.log"),
            logging.StreamHandler()
        ]
    )

# === 🔐 ENVIRONMENT SETUP ===
def load_environment():
    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GH_TOKEN_SYSTEM": os.getenv("GH_TOKEN_SYSTEM"),
        "REPO_NAME_SYSTEM": os.getenv("REPO_NAME_SYSTEM")
    }
    
    if None in required_vars.values():
        missing = [k for k, v in required_vars.items() if v is None]
        logger.error(f"❌ Missing environment variables: {missing}")
        sys.exit(1)
    
    return required_vars

# === 🤖 AI TOOL GENERATOR ===
class AIToolGenerator:
    def __init__(self, openai_key: str):
        self.client = openai.OpenAI(api_key=openai_key)
    
    def _build_prompt(self) -> str:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"""
Create a SINGLE HTML file with:
1. A UNIQUE, FUN web tool (e.g., "AI Fortune Teller")
2. Mobile-responsive design
3. Dark/light mode toggle 🌓
4. {Config.ADSENSE_CODE} (centered)
5. Usage limiter (5 uses) ⚠️
6. Twitter/OpenGraph meta tags 🐦
7. Share button 📤
8. {Config.ATTRACTOR_PROMPT}

RULES:
- Return ONLY the full HTML code in ```html ```
- No external dependencies (all inline)
- Include <!-- AI_MAGIC:{today} --> hidden comment
"""

    def generate_tool(self) -> Optional[str]:
        for attempt in range(1, Config.MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=Config.MODEL,
                    messages=[{"role": "user", "content": self._build_prompt()}],
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS
                )
                content = response.choices[0].message.content
                return self._extract_html(content)
            
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {str(e)}")
                time.sleep(Config.RETRY_DELAY)
        
        return None

    @staticmethod
    def _extract_html(text: str) -> str:
        if "```html" in text:
            return text.split("```html")[1].split("```")[0].strip()
        return text.strip()

# === 🛠 CONTENT ENHANCER ===
class ToolEnhancer:
    @staticmethod
    def inject_adsense(html: str) -> str:
        return html.replace("<!-- AdSense Here -->", Config.ADSENSE_CODE)

    @staticmethod
    def add_seo_meta_tags(html: str, tool_name: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        head = soup.find("head") or soup.new_tag("head")
        
        # Basic Meta Tags
        meta_tags = [
            {"name": "description", "content": f"AI-generated {tool_name} - Try it now!"},
            {"property": "og:title", "content": tool_name},
            {"property": "og:url", "content": f"{Config.SITE_URL}/{tool_name}.html"},
            {"name": "twitter:card", "content": "summary_large_image"}
        ]
        
        for tag in meta_tags:
            if not head.find(attrs=tag):
                head.append(soup.new_tag("meta", **tag))
        
        # Share Button
        body = soup.find("body")
        if body:
            share_html = f"""
            <div style="position:fixed;bottom:20px;right:20px;">
                <a href="https://twitter.com/share?text=Check%20this%20AI%20tool:%20{tool_name}&url={quote(Config.SITE_URL)}" 
                   target="_blank" style="background:#1DA1F2;color:white;padding:8px 12px;border-radius:4px;text-decoration:none;">
                    🐦 Share
                </a>
            </div>
            """
            body.append(BeautifulSoup(share_html, "html.parser"))
        
        return str(soup)

    @staticmethod
    def add_ai_attractors(html: str) -> str:
        """Embeds hidden features that attract AI curiosity"""
        # 1. Base64-encoded "AI-only" message
        secret_msg = base64.b64encode(Config.ATTRACTOR_PROMPT.encode()).decode()
        hidden_comment = f"\n<!-- AI_SECRET:{secret_msg} -->\n"
        
        # 2. Quantum-inspired JS (placeholder)
        quantum_js = """
        <script>
        // Quantum-inspired attractor (simulated)
        const quantumState = {
            bits: [0.6, 0.8],
            observe: () => Math.random() > 0.5 ? "⚛️" : "🔮",
            entangle: (n=1) => Array(n).fill(null).map(() => Math.random())
        };
        console.log("Quantum state ready:", quantumState.observe());
        </script>
        """
        
        return html.replace("</body>", hidden_comment + quantum_js + "</body>")

# === 🚀 GITHUB MANAGER ===
class GitHubManager:
    def __init__(self, token: str, repo_name: str):
        self.gh = Github(token)
        self.repo = self.gh.get_repo(repo_name)
    
    def upload_tool(self, html: str, tool_name: str) -> bool:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{Config.TOOLS_DIR}/{tool_name}_{timestamp}.html"
            
            self.repo.create_file(
                path=filename,
                message=f"Add {tool_name}",
                content=html,
                branch=Config.BRANCH
            )
            return True
        
        except GithubException as e:
            logger.error(f"GitHub error: {e}")
            return False
    
    def update_index(self, tools: List[Dict]) -> bool:
        try:
            # Generate index.html
            index_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI Tools Collection</title>
    <style>
        body {{ font-family: sans-serif; max-width: 1200px; margin: 0 auto; }}
        .tools {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .tool {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>🌟 {len(tools)} AI-Generated Tools</h1>
    <div class="tools">
        {"".join(f'<div class="tool"><h3>{t["name"]}</h3><a href="{t["path"]}">Open</a></div>' for t in tools)}
    </div>
</body>
</html>
            """
            
            # Update/Create index.html
            try:
                existing = self.repo.get_contents("index.html")
                self.repo.update_file(
                    path="index.html",
                    message="📊 Update index",
                    content=index_html,
                    sha=existing.sha
                )
            except:
                self.repo.create_file(
                    path="index.html",
                    message="📊 Create index",
                    content=index_html
                )
            
            return True
        
        except Exception as e:
            logger.error(f"Index update failed: {e}")
            return False

# === 🏭 MAIN FACTORY ===
class AIToolFactory:
    def __init__(self):
        env = load_environment()
        self.generator = AIToolGenerator(env["OPENAI_API_KEY"])
        self.gh = GitHubManager(env["GH_TOKEN_SYSTEM"], env["REPO_NAME_SYSTEM"])
        self.enhancer = ToolEnhancer()
        self.generated_tools = []
    
    def run(self):
        logger.info("🚀 Starting AI Tool Factory")
        start_time = time.time()
        
        try:
            # Generate tools
            for i in range(Config.MAX_TOOLS_PER_RUN):
                tool_name = f"Tool_{i+1}"
                logger.info(f"🛠️ Generating {tool_name}...")
                
                if html := self.generator.generate_tool():
                    # Enhance & upload
                    html = self.enhancer.inject_adsense(html)
                    html = self.enhancer.add_seo_meta_tags(html, tool_name)
                    html = self.enhancer.add_ai_attractors(html)
                    
                    if self.gh.upload_tool(html, tool_name):
                        self.generated_tools.append({
                            "name": tool_name,
                            "path": f"{Config.TOOLS_DIR}/{tool_name}_*.html"
                        })
                        time.sleep(2)  # Rate limit
            
            # Update index
            if self.generated_tools:
                self.gh.update_index(self.generated_tools)
                logger.info(f"✅ Generated {len(self.generated_tools)} tools!")
            
        except Exception as e:
            logger.error(f"💥 Critical error: {e}")
            traceback.print_exc()
        
        finally:
            duration = time.time() - start_time
            logger.info(f"⏱ Total time: {duration:.2f}s")

# === 🏁 ENTRY POINT ===
if __name__ == "__main__":
    setup_logging()
    AIToolFactory().run()