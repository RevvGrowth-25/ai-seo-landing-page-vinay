# DevOps Deployment Documentation: AI SEO Landing Page

This document provides complete technical documentation of the Flask-based **AI SEO Landing Page** deployment on the production Hostinger VPS server. It outlines server environments, ports, directory structures, PM2 process management, and essential troubleshooting guides for your technical team.

---

## 🖥️ Server Environment & Architecture

| Parameter | Value / Configuration |
| :--- | :--- |
| **Server Provider** | Hostinger VPS |
| **Operating System** | Ubuntu Linux (LTS) |
| **Host / IP Address** | `69.62.81.179` |
| **Deployment Port** | `5000` (Binds to `0.0.0.0` inside Flask/Gunicorn) |
| **Gunicorn Workers** | `4` parallel worker processes (recommended for production load) |
| **GitHub Repository** | `https://github.com/RevvGrowth-25/ai-seo-landing-page-vinay.git` |
| **Root Directory** | `/var/www/ai-seo-landing` |
| **Process Manager** | PM2 (Process Name: `ai-seo-landing`) |

---

## 📁 Directory & Workspace Structure

```bash
/var/www/ai-seo-landing/
├── app.py                  # Core Flask entrypoint serving the templates
├── requirements.txt        # Python dependency requirements (Flask, Gunicorn)
├── README.md               # Quick-start setup manual for local testing
├── .gitignore              # Configured to ignore internal tracker & config variables
├── templates/
│   └── AI SEO Landing - Standalone.html # Main landing page template (embedded with Brand favicon)
└── venv/                   # Local Python 3 virtual environment
```

---

## 🚀 Execution & Process Commands (PM2)

The application is registered inside the VPS **PM2 God Daemon** manager to keep it running 24/7. It will automatically restart on crashes and automatically boot up when the VPS is restarted.

### 1. Starting the Server under Gunicorn (High Traffic Setup)
To handle 1000+ simultaneous visitors cleanly without lag, Gunicorn serves the Flask WSGI instance with 4 workers:
```bash
# Delete default fork processes (if any)
pm2 delete ai-seo-landing

# Start Gunicorn in PM2
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 app:app" --name "ai-seo-landing"

# Save list to host system config for boot-recovery
pm2 save
```

### 2. Standard Service Management
```bash
# Check running status, CPU, and Memory footprints
pm2 status
# Or:
pm2 list

# Restart the application
pm2 restart ai-seo-landing

# Stop the application
pm2 stop ai-seo-landing
```

---

## 🛠️ Debugging & Troubleshooting

Use these standard commands when you need to inspect logs or debug connection issues:

### 1. View Live Server Logs
PM2 streams real-time console `stdout` and `stderr` outputs from Flask/Gunicorn:
```bash
pm2 logs ai-seo-landing --lines 100
```

### 2. Verify Port & Process Binding
To ensure the Flask port `5000` is active and running cleanly:
```bash
sudo ss -tulpn | grep 5000
```

### 3. Check Local Firewall Rules
If the server is active internally but inaccessible in the web browser, verify the UFW firewall rules:
```bash
# Allow port 5000 traffic
sudo ufw allow 5000/tcp

# Reload firewall configurations
sudo ufw reload

# Check status of allowed ports
sudo ufw status verbose
```

### 4. Direct Manual Testing
To run the server manually in foreground shell mode (for deep local debugging):
```bash
# Navigate to the workspace
cd /var/www/ai-seo-landing

# Activate virtual environment
source venv/bin/activate

# Execute app in foreground
python app.py
```

---
*Created and maintained by the DevOps Team. For updates, please edit this file and push to main.*
