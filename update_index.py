from main import AIToolFactory

def generate_index():
    """Updates the GitHub Pages index with all tools"""
    factory = AIToolFactory()
    
    # Get all existing tools
    tools = []
    try:
        contents = factory.gh.repo.get_contents(factory.gh.TOOLS_DIR)
        tools = [
            {"name": f.name.replace(".html", ""), "path": f.path}
            for f in contents if f.name.endswith(".html")
        ]
    except Exception as e:
        print(f"Error listing tools: {e}")
    
    # Update index.html
    if tools:
        factory.gh.update_index(tools)