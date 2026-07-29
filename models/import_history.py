from extensions import db
from datetime import datetime


class ImportHistory(db.Model):

    __tablename__ = "import_history"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    seller_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "seller.id"
        )
    )


    filename = db.Column(
        db.String(255)
    )


    total = db.Column(
        db.Integer,
        default=0
    )


    success = db.Column(
        db.Integer,
        default=0
    )


    errors = db.Column(
        db.Integer,
        default=0
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )