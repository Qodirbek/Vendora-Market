from extensions import db

from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



class User(db.Model):

    __tablename__ = "user"


    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20),
        unique=True
    )

    email = db.Column(
        db.String(120)
    )

    address = db.Column(
        db.Text
    )


    # TO'LOV RUXSATLARI

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


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True
    )
    # =====================================
    # BASIC
    # =====================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(100),
        nullable=False
    )


    username = db.Column(
        db.String(50),
        unique=True,
        index=True
    )


    email = db.Column(
        db.String(120),
        unique=True,
        index=True
    )


    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )


    avatar = db.Column(
        db.String(500),
        default="/static/images/default-avatar.png"
    )



    # =====================================
    # LOCATION
    # =====================================

    country = db.Column(
        db.String(50),
        default="Uzbekistan"
    )


    region = db.Column(
        db.String(100)
    )


    city = db.Column(
        db.String(100)
    )


    address = db.Column(
        db.Text
    )



    # =====================================
    # ACCOUNT
    # =====================================

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
        db.String(20),
        default="uz"
    )



    # =====================================
    # LOGIN INFO
    # =====================================

    last_login = db.Column(
        db.DateTime
    )


    last_ip = db.Column(
        db.String(50)
    )



    # =====================================
    # TIME
    # =====================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    # =====================================
    # PASSWORD
    # =====================================

    def set_password(
        self,
        password
    ):

        self.password = generate_password_hash(
            password
        )



    def check_password(
        self,
        password
    ):

        return check_password_hash(
            self.password,
            password
        )



    # =====================================
    # USER INFO
    # =====================================

    def get_full_name(self):

        return self.name



    def is_admin(self):

        return self.role == "admin"



    def is_seller(self):

        return self.role == "seller"



    # =====================================
    # RELATIONSHIPS
    # =====================================


    carts = db.relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )



    profile = db.relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )



    # =====================================
    # JSON
    # =====================================

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "username": self.username,

            "phone": self.phone,

            "avatar": self.avatar,

            "country": self.country,

            "region": self.region,

            "role": self.role,

            "created_at":
                self.created_at.strftime(
                    "%Y-%m-%d"
                )
        }



    # =====================================
    # DELETE ACCOUNT
    # =====================================

    def deactivate(self):

        self.is_active = False



    # =====================================
    # STRING
    # =====================================

    def __repr__(self):

        return (
            f"<User {self.phone}>"
        )