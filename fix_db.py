from app import app
from extensions import db
from sqlalchemy import text


queries = [

    # =========================
    # USER TABLE
    # =========================

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN DEFAULT FALSE;
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS tg_id BIGINT;
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS tg_username VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS tg_first_name VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS tg_last_name VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS tg_photo TEXT;
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS telegram_verified BOOLEAN DEFAULT FALSE;
    """,


    # =========================
    # ORDER TABLE
    # =========================

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS delivery_type VARCHAR(50);
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS delivery_price FLOAT DEFAULT 0;
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS discount FLOAT DEFAULT 0;
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS payment_check VARCHAR(255);
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS payment_verified BOOLEAN DEFAULT FALSE;
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS status_note TEXT;
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS cancel_reason TEXT;
    """,

    """
    ALTER TABLE "order"
    ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP;
    """,


    # =========================
    # ORDER ITEM TABLE
    # =========================

    """
    ALTER TABLE order_item
    ADD COLUMN IF NOT EXISTS commission_percent FLOAT DEFAULT 0;
    """,

    """
    ALTER TABLE order_item
    ADD COLUMN IF NOT EXISTS commission FLOAT DEFAULT 0;
    """,

    """
    ALTER TABLE order_item
    ADD COLUMN IF NOT EXISTS seller_income FLOAT DEFAULT 0;
    """,


    # =========================
    # USER EXTRA
    # =========================

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS avatar VARCHAR(255);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS country VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS region VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS city VARCHAR(100);
    """,

    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS address TEXT;
    """
]


with app.app_context():

    for q in queries:
        try:
            db.session.execute(text(q))
            print("OK:", q.strip().split("\n")[1])
        except Exception as e:
            print("ERROR:", e)

    db.session.commit()


print("======================")
print(" DATABASE MIGRATION COMPLETE ")
print("======================")