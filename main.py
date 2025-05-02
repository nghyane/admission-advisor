import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from admission_advisor.config import Config

# Get configs
configs = Config()

# Get the directory where admission_advisor is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))


# Configure CORS for your domains
ALLOWED_ORIGINS = ["*"]

# Create FastAPI app with the session service
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url=configs.SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=True  # Set to False in production if you have your own frontend
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))