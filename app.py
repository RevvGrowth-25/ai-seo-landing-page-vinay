import os
import sys
from flask import Flask, render_template

app = Flask(__name__)

# ANSI Color codes for clean, elegant console reporting
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"

@app.route('/')
def index():
    """Serve the AI SEO Landing Standalone page."""
    try:
        return render_template("AI SEO Landing - Standalone.html")
    except Exception as e:
        print(f"\033[91m[ERROR] Failed to render Standalone landing page: {str(e)}\033[0m")
        return "Error: AI SEO Landing - Standalone.html not found in templates directory.", 404

if __name__ == '__main__':
    # Default Flask port requested is 5000
    # host='0.0.0.0' binds to all interfaces, which is essential for Hostinger VPS deployment
    port_num = 5000
    if len(sys.argv) > 1:
        try:
            port_num = int(sys.argv[1])
        except ValueError:
            pass
            
    print("\n" + "*"*60)
    print(f"[ACTIVE] {BOLD}{GREEN}AI SEO LANDING VPS SERVER ACTIVE & LISTENING{RESET}")
    print("*"*60)
    print(f"[URL]  {BOLD}Landing Page URL:{RESET}   {BOLD}{CYAN}http://localhost:{port_num}/{RESET}")
    print(f"[INFO] {BOLD}VPS Ready:{RESET}          Hostinger configured to run on 0.0.0.0:{port_num}")
    print("*"*60 + "\n")
    
    app.run(host='0.0.0.0', port=port_num, debug=True)
