# =====================================
# CONFIGURATION
# Vendora Market
# =====================================

import os
from dotenv import load_dotenv


# Load .env
load_dotenv()



class Config:


    # =================================
    # TELEGRAM BOT
    # =================================

    CUSTOMER_BOT_TOKEN = os.getenv(
        "CUSTOMER_BOT_TOKEN"
    )


    TG_BOT_TOKEN = os.getenv(
        "TG_BOT_TOKEN"
    )


    BOT_TOKEN = (
        CUSTOMER_BOT_TOKEN
        or TG_BOT_TOKEN
    )



    # =================================
    # WEBSITE
    # =================================

    SITE_URL = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:5000"
    )


    WEB_APP_URL = os.getenv(
        "WEB_APP_URL",
        SITE_URL
    )



    # =================================
    # FLASK
    # =================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "vendora-secret-key"
    )


    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"



    # =================================
    # DATABASE
    # =================================

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///database.db"
    )



    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # =================================
    # TELEGRAM AUTH
    # =================================

    TELEGRAM_BOT_USERNAME = os.getenv(
        "TELEGRAM_BOT_USERNAME",
        "Vendora_Marketbot"
    )



    # =================================
    # PAYMENT
    # =================================

    STRIPE_KEY = os.getenv(
        "STRIPE_KEY"
    )


    NOWPAYMENTS_KEY = os.getenv(
        "NOWPAYMENTS_KEY"
    )



    # =================================
    # UPLOAD
    # =================================

    MAX_CONTENT_LENGTH = (
        50 * 1024 * 1024
    )


    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "static/uploads"
    )



    # =================================
    # LANGUAGE
    # =================================

    DEFAULT_LANGUAGE = "uz"



    # =================================
    # SECURITY
    # =================================

    SESSION_COOKIE_SECURE = os.getenv(
        "SESSION_COOKIE_SECURE",
        "False"
    ).lower() == "true"


    REMEMBER_COOKIE_DURATION = 30 * 24 * 60 * 60



# =====================================
# EXPORT VARIABLES
# =====================================

BOT_TOKEN = Config.BOT_TOKEN

SITE_URL = Config.SITE_URL

WEB_APP_URL = Config.WEB_APP_URL