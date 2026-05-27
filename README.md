# AI SEO Landing Page - Vinay

This repository contains a clean, minimal single-page Python Flask application serving the **AI SEO Landing Page** on port 5000. It is designed to be deployed on a VPS (like Hostinger) alongside other applications (e.g. Next.js) without any port conflicts.

## 🚀 Files Included

* **`app.py`**: The core Flask server running on port `5000` (bound to `0.0.0.0` for VPS external access) serving ONLY the landing page.
* **`templates/AI SEO Landing - Standalone.html`**: The main standalone SEO agency landing page, complete with a custom brand favicon.
* **`requirements.txt`**: Minimal requirements (Flask) for running the server.

## 📦 How to Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Visit `http://localhost:5000` in your web browser.
