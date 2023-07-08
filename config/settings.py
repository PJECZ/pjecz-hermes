"""
Config Settings
"""
import os

from dotenv import load_dotenv

load_dotenv()


# Google Cloud Storage
GCS_BUCKETS = os.getenv("GCS_BUCKETS", "").split(",")

# Plataforma Web API key
PLATAFORMA_WEB_API_URL = os.getenv("PLATAFORMA_WEB_API_URL", "")
PLATAFORMA_WEB_API_KEY = os.getenv("PLATAFORMA_WEB_API_KEY", "")
LIMIT = int(os.getenv("LIMIT", "100"))
TIMEOUT = int(os.getenv("TIMEOUT", "12"))
SLEEP = int(os.getenv("SLEEP", "1"))

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")
