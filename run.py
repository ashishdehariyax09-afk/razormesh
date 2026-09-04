"""
RazorMesh Master Launcher
Initializes SQLite WAL database, validates SHA-256 audit continuity,
and boots the FastAPI gateway with live telemetry at http://127.0.0.1:8000
"""

import sys
import webbrowser
import threading
import time
import uvicorn

from database import init_db
from audit_engine import verify_audit_integrity

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n[RAZORMESH] Launching Interactive Cockpit at: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    print("=" * 70)
    print("   RAZORMESH: Autonomous Agentic Commerce Gateway v2.0")
    print("   Track 01: Autonomous Agentic Commerce - Razorpay AI Buildathon 2026")
    print("=" * 70)
    
    # 1. Initialize SQLite Database in WAL mode
    print("[1/3] Initializing SQLite WAL Database...")
    init_db()
    
    # 2. Verify Cryptographic SHA-256 Hash Chain
    print("[2/3] Verifying Cryptographic Audit Trail Continuity...")
    integrity = verify_audit_integrity()
    print(f"      Status: {integrity['message']} (Total Blocks: {integrity['total_blocks']})")
    
    # 3. Launch Web Browser
    print("[3/3] Booting FastAPI Server & Telemetry Engine at http://127.0.0.1:8000...")
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
