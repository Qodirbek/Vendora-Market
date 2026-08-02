from app import app
from extensions import db
from sqlalchemy import text


with app.app_context():

    print("Database fixing...")


    # sqlite NOT NULL olib tashlash uchun
    db.session.execute(text("""
    
    CREATE TABLE user_new AS
    SELECT *
    FROM user;

    """))


    db.session.execute(text("""
    
    DROP TABLE user;

    """))


    db.session.execute(text("""
    
    CREATE TABLE user (

        id INTEGER PRIMARY KEY,

        name VARCHAR(100),

        username VARCHAR(50),

        email VARCHAR(120),

        phone VARCHAR(20),

        password VARCHAR(255),

        avatar VARCHAR(500),

        country VARCHAR(50),

        region VARCHAR(100),

        city VARCHAR(100),

        address TEXT,

        role VARCHAR(30),

        is_active BOOLEAN DEFAULT 1,

        is_verified BOOLEAN DEFAULT 0,

        language VARCHAR(20),

        last_login DATETIME,

        last_ip VARCHAR(50),

        created_at DATETIME,

        updated_at DATETIME,


        allow_cash BOOLEAN DEFAULT 1,

        allow_card BOOLEAN DEFAULT 1,

        is_blocked BOOLEAN DEFAULT 0,


        tg_id VARCHAR(50) UNIQUE,

        tg_username VARCHAR(100),

        tg_first_name VARCHAR(100),

        tg_photo VARCHAR(500),

        telegram_verified BOOLEAN DEFAULT 0

    );

    """))


    db.session.execute(text("""

    INSERT INTO user

    SELECT *

    FROM user_new;

    """))


    db.session.execute(text("""

    DROP TABLE user_new;

    """))


    db.session.commit()


print("✅ USER TABLE FIXED")