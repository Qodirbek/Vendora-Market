import os
from dotenv import load_dotenv
from datetime import timedelta


# =====================================
# ENV LOAD
# =====================================

load_dotenv()


# =====================================
# PATH
# =====================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# =====================================
# SESSION
# =====================================

PERMANENT_SESSION_LIFETIME = timedelta(
    days=30
)


# =====================================
# CONFIG
# =====================================

class Config:

    # =========================
    # SECURITY
    # =========================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "secret-key"
    )


    # =========================
    # DATABASE
    # =========================

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )


    if DATABASE_URL:

        if DATABASE_URL.startswith(
            "postgres://"
        ):

            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )


        SQLALCHEMY_DATABASE_URI = DATABASE_URL


    else:

        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(
                BASE_DIR,
                "database.db"
            )
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False



    # =========================
    # TELEGRAM BOT
    # =========================

    TG_BOT_TOKEN = os.getenv(
        "TG_BOT_TOKEN"
    )


    # =========================
    # SELLER / API
    # =========================

    SOTUVCHI_KEY = os.getenv(
        "SOTUVCHI_KEY"
    )

    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    CUSTOMER_BOT_TOKEN = os.getenv("CUSTOMER_BOT_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    SITE_URL = os.getenv("SITE_URL")
    WEB_APP_URL = os.getenv("WEB_APP_URL")



    # =========================
    # DEBUG
    # =========================

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ) == "True"