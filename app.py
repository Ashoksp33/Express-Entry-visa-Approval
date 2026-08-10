import os
import sys
import uvicorn

# Ensure current script directory is in Python's module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app

if __name__ == "__main__":
    print("Starting CanVisa AI FastAPI Server on http://localhost:8000 ...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
