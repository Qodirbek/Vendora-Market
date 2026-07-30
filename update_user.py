from app import app
from extensions import db


with app.app_context():

    db.session.execute(
        db.text(
            "ALTER TABLE user ADD COLUMN allow_card BOOLEAN DEFAULT 1"
        )
    )

    db.session.execute(
        db.text(
            "ALTER TABLE user ADD COLUMN is_blocked BOOLEAN DEFAULT 0"
        )
    )

    db.session.commit()


print("User columns qo'shildi!")