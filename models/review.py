from extensions import db
from datetime import datetime


class Review(db.Model):

    __tablename__ = "review"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )


    rating = db.Column(
        db.Integer,
        default=5
    )


    text = db.Column(
        db.Text,
        nullable=False
    )


    approved = db.Column(
        db.Boolean,
        default=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    user = db.relationship(
        "User",
        back_populates="reviews"
    )



    product = db.relationship(
        "Product",
        back_populates="reviews"
    )



    def __repr__(self):

        return f"<Review {self.id}>"