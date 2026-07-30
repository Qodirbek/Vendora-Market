from app import app
from extensions import db
from sqlalchemy import text


with app.app_context():

    columns = [
        """
        ALTER TABLE "user"
        ADD COLUMN IF NOT EXISTS allow_cash BOOLEAN DEFAULT TRUE;
        """,

        """
        ALTER TABLE "user"
        ADD COLUMN IF NOT EXISTS allow_card BOOLEAN DEFAULT TRUE;
        """
    ]


    for sql in columns:
        db.session.execute(text(sql))


    db.session.commit()

    print("✅ USER columns fixed")