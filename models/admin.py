from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Admin(db.Model, UserMixin):

    __tablename__ = "admin"


    id = db.Column(
    db.Integer,
    primary_key=True,
    autoincrement=True
    )


    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )


    role = db.Column(
        db.String(50),
        default="admin"
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # Parol saqlash
    def set_password(self, password):

        self.password = generate_password_hash(
            password
        )


    # Parol tekshirish
    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )


    # Flask-Login uchun
    def get_id(self):

        return str(self.id)


    def __repr__(self):

        return f"<Admin {self.username}>"
