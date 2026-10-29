"""
RetailBot AI — Application Entry Point
Run with: python main.py
"""

import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.config import get_settings


def main():
    settings = get_settings()
    
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=(settings.app_env == "development"),
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
