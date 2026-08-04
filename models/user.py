from extensions import db
from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


class User(db.Model):

    __tablename__ = "user"


    # =========================
    # ID
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =========================
    # BASIC INFO
    # =========================

    name = db.Column(
        db.String(100),
        nullable=False,
        default="User"
    )


    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=True,
        index=True
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )


    username = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )


    password = db.Column(
        db.String(255),
        nullable=True
    )



    # =========================
    # TELEGRAM AUTH
    # =========================

    tg_id = db.Column(
        db.String(50),
        unique=True,
        nullable=True,
        index=True
    )


    tg_username = db.Column(
        db.String(100),
        nullable=True
    )


    tg_first_name = db.Column(
        db.String(100),
        nullable=True
    )


    tg_last_name = db.Column(
        db.String(100),
        nullable=True
    )


    tg_photo = db.Column(
        db.String(500),
        nullable=True
    )


    telegram_verified = db.Column(
        db.Boolean,
        default=False
    )



    # =========================
    # PROFILE
    # =========================

    avatar = db.Column(
        db.String(500),
        default="/static/images/default-avatar.png"
    )


    country = db.Column(
        db.String(50),
        default="Uzbekistan"
    )


    region = db.Column(
        db.String(100),
        nullable=True
    )


    city = db.Column(
        db.String(100),
        nullable=True
    )


    address = db.Column(
        db.Text,
        nullable=True
    )


    allow_cash = db.Column(
        db.Boolean,
        default=True
    )
    
    allow_card = db.Column(
        db.Boolean,
        default=True
    )
    
    is_blocked = db.Column(
        db.Boolean,
        default=False
    )


    # =========================
    # ROLE
    # =========================

    role = db.Column(
        db.String(30),
        default="user"
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )


    is_verified = db.Column(
        db.Boolean,
        default=False
    )


    language = db.Column(
        db.String(10),
        default="uz"
    )



    # =========================
    # SECURITY
    # =========================

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )


    last_ip = db.Column(
        db.String(50),
        nullable=True
    )



    # =========================
    # DATE
    # =========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    # =========================
    # RELATIONS
    # =========================

    profile = db.relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    carts = db.relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )



    # =========================
    # PASSWORD SYSTEM
    # =========================

    def set_password(self, password):

        self.password = generate_password_hash(
            password
        )



    def check_password(self, password):

        if not self.password:
            return False


        return check_password_hash(
            self.password,
            password
        )



    # =========================
    # NAME
    # =========================

    def full_name(self):

        return (
            self.name
            or self.tg_first_name
            or self.tg_username
            or "User"
        )



    def telegram_name(self):

        return (
            self.tg_first_name
            or self.tg_username
            or "Telegram User"
        )



    # =========================
    # LOGIN TYPE
    # =========================

    def has_password(self):

        return bool(
            self.password
        )


    def has_phone(self):

        return bool(
            self.phone
        )


    def telegram_login_ready(self):

        return (
            self.tg_id
            and self.phone
            and self.password
        )



    # =========================
    # ROLE CHECK
    # =========================

    def is_admin(self):

        return self.role == "admin"


    def is_seller(self):

        return self.role == "seller"


    def is_customer(self):

        return self.role == "user"



    # =========================
    # STATUS
    # =========================

    def block(self):

        self.is_blocked = True



    def unblock(self):

        self.is_blocked = False



    def activate(self):

        self.is_active = True



    def deactivate(self):

        self.is_active = False



    # =========================
    # API
    # =========================

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.full_name(),

            "phone": self.phone,

            "email": self.email,

            "telegram": self.telegram_verified,

            "tg_id": self.tg_id,

            "avatar": self.avatar,

            "role": self.role

        }



    def __repr__(self):

        return f"<User {self.id} {self.name}>"