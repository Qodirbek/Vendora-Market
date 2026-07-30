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
        """,

        """
        ALTER TABLE "user"
        ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN DEFAULT FALSE;
        """

    ]


    for column in columns:
        db.session.execute(text(column))


    db.session.commit()


print("✅ USER columns fixed")
