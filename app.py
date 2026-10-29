import os
import sys
import uvicorn
import webbrowser
import threading
import time

# Ensure current script directory is in Python's module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    is_cloud = bool(os.environ.get("PORT"))
    host = "0.0.0.0" if is_cloud else "127.0.0.1"

    print(f"Starting CanVisa AI FastAPI Server on http://{host}:{port} ...")
    if not is_cloud:
        threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False
    )