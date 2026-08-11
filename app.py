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
    print("Starting CanVisa AI FastAPI Server on http://localhost:8000 ...")
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
