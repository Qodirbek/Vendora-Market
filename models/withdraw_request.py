from extensions import db
from datetime import datetime


class WithdrawRequest(db.Model):

    __tablename__="withdraw_request"


    id=db.Column(
        db.Integer,
        primary_key=True
    )


    seller_id=db.Column(
        db.Integer,
        db.ForeignKey("seller.id"),
        nullable=False
    )


    amount=db.Column(
        db.Integer,
        nullable=False
    )


    status=db.Column(
        db.String(50),
        default="pending"
    )

    # pending
    # approved
    # rejected


    phone=db.Column(
        db.String(30)
    )


    created_at=db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    seller=db.relationship(
        "Seller",
        back_populates="withdraw_requests"
    )


    def __repr__(self):

        return f"<Withdraw {self.amount}>"