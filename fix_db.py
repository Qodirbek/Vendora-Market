from app import app
from extensions import db
from sqlalchemy import text


with app.app_context():

    queries = [

    # USER
    """
    ALTER TABLE "user"
    ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN DEFAULT FALSE;
    """,


    # ORDER
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


    # ORDER ITEM
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
    """

    ]


    for q in queries:
        db.session.execute(text(q))


    db.session.commit()


print("✅ DATABASE MIGRATION DONE")
