from app import app
from extensions import db
from models.admin import Admin


with app.app_context():

    username = "Qodirbek_2007"

    # Admin borligini tekshirish
    admin = Admin.query.filter_by(
        username=username
    ).first()


    if admin:

        print("Admin allaqachon mavjud ✅")


    else:

        admin = Admin(
            username=username
        )

        admin.set_password(
            "Qodirbek_2007"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin yaratildi ✅")
