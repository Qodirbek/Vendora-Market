import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PERMANENT_SESSION_LIFETIME = timedelta(days=30)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "secret-key"
    )


    # Render PostgreSQL
    DATABASE_URL = os.environ.get(
        "DATABASE_URL"
    )


    if DATABASE_URL:

        if DATABASE_URL.startswith("postgres://"):

            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )


        SQLALCHEMY_DATABASE_URI = DATABASE_URL


    else:

        # Local kompyuter uchun SQLite
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(
                BASE_DIR,
                "database.db"
            )
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SOTUVCHI_KEY = os.getenv(
        "SOTUVCHI_KEY"
    )
