from extensions import db


class Profile(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True
    )


    full_name = db.Column(
        db.String(100)
    )


    phone = db.Column(
        db.String(20),
        unique=True
    )


    email = db.Column(
        db.String(120),
        unique=True
    )


    country = db.Column(
        db.String(100),
        default="O'zbekiston"
    )


    language = db.Column(
        db.String(20),
        default="uz"
    )


    avatar = db.Column(
        db.String(500),
        default="/static/images/user.png"
    )


    user = db.relationship(
        "User",
        back_populates="profile"
    )


    def __repr__(self):
        return f"<Profile {self.full_name}>"