from app import app
from extensions import db
from sqlalchemy import text

with app.app_context():
    result = db.session.execute(
        text("PRAGMA table_info(user)")
    )

    for row in result:
        print(row)