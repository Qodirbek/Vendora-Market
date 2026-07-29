from app import app
from extensions import db
from models.admin import Admin


with app.app_context():

    admin=Admin(
        username="Qodirbek_2007"
    )

    admin.set_password(
        "Qodirbek_2007"
    )


    db.session.add(admin)

    db.session.commit()


print("Admin yaratildi")