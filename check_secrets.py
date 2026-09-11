import os

def check_secrets():
    bad_strings = ["umesh051412"]
    found = False
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".venv" in root or "node_modules" in root or "artifacts" in root or ".gemini" in root:
            continue
            
        for file in files:
            # Check python and js files
            if file.endswith(('.py', '.js', '.jsx', '.json', '.html', '.css', '.env.example')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for bad in bad_strings:
                            if bad in content:
                                print(f"WARNING: Exposed secret '{bad}' found in {filepath}!")
                                found = True
                except Exception as e:
                    pass
                    
    if not found:
        print("SUCCESS: No exposed secrets found in source code.")

if __name__ == "__main__":
    check_secrets()
