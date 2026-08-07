import os
from datetime import timedelta
from dotenv import load_dotenv

# =====================================
# ENV LOAD
# =====================================
load_dotenv()

# =====================================
# PATH
# =====================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# =====================================
# CONFIG CLASS
# =====================================
class Config:

    # =========================
    # SECURITY & SESSION
    # =========================
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or os.getenv("SECRET_KEY", "default-fallback-secret-key")
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Heroku/Render kabi platformalardagi postgres:// ni postgresql:// ga o'girish
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Agar lokal muhit bo'lsa SQLite ishlatiladi
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # FIREBASE CONFIGURATION
    # =========================
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
    FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID")
    FIREBASE_MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID")
    FIREBASE_SERVICE_ACCOUNT_JSON = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

    # =========================
    # TELEGRAM BOT & SITE URLs
    # =========================
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    CUSTOMER_BOT_TOKEN = os.getenv("CUSTOMER_BOT_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    SITE_URL = os.getenv("SITE_URL")
    WEB_APP_URL = os.getenv("WEB_APP_URL")

    # =========================
    # SELLER / API
    # =========================
    SOTUVCHI_KEY = os.getenv("SOTUVCHI_KEY")

    # =========================
    # DEBUG MODE
    # =========================
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
