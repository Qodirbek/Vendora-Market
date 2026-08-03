from extensions import db
from datetime import datetime


class Notification(db.Model):

    __tablename__ = "notification"


    # =================================
    # BASIC
    # =================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )

    user = db.relationship(
    "User",
    back_populates="notifications"
    )


    message = db.Column(
        db.Text,
        nullable=False
    )


    # notification turi
    # product
    # order
    # payment
    # system
    # seller
    type = db.Column(
        db.String(50),
        default="system"
    )


    # kim yubordi
    sender = db.Column(
        db.String(100),
        default="System"
    )


    # o'qilgan yoki yo'q
    is_read = db.Column(
        db.Boolean,
        default=False
    )



    # =================================
    # USER
    # =================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id"
        ),
        nullable=True,
        index=True
    )



    # =================================
    # SELLER
    # =================================

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "seller.id"
        ),
        nullable=True,
        index=True
    )



    # =================================
    # ORDER
    # =================================

    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "order.id"
        ),
        nullable=True,
        index=True
    )



    # =================================
    # PRODUCT
    # =================================

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "product.id"
        ),
        nullable=True,
        index=True
    )



    # =================================
    # EXTRA DATA
    # =================================

    # URL yoki sahifa
    # masalan:
    # /seller/orders/5

    link = db.Column(
        db.String(500),
        nullable=True
    )


    # icon nomi
    # fa-shopping-cart
    # fa-box

    icon = db.Column(
        db.String(100),
        default="bell"
    )



    # =================================
    # TIME
    # =================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        index=True
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    # =================================
    # RELATIONSHIPS
    # =================================


    user = db.relationship(
        "User",
        back_populates="notifications"
    )


    seller = db.relationship(
        "Seller",
        back_populates="notifications"
    )


    order = db.relationship(
        "Order",
        back_populates="notifications"
    )


    product = db.relationship(
        "Product",
        back_populates="notifications"
    )



    # =================================
    # FUNCTIONS
    # =================================


    def mark_read(self):

        self.is_read = True



    def mark_unread(self):

        self.is_read = False



    def toggle_read(self):

        self.is_read = not self.is_read



    def short_message(self):

        if len(self.message) > 80:
            return self.message[:80] + "..."

        return self.message



    def age(self):

        """
        Qancha vaqt oldin yaratilgan
        """

        diff = datetime.utcnow() - self.created_at


        seconds = diff.total_seconds()


        if seconds < 60:
            return "Hozir"


        if seconds < 3600:
            return f"{int(seconds/60)} daqiqa oldin"


        if seconds < 86400:
            return f"{int(seconds/3600)} soat oldin"


        return f"{int(seconds/86400)} kun oldin"




    def to_dict(self):

        return {

            "id":
                self.id,

            "title":
                self.title,

            "message":
                self.message,

            "type":
                self.type,

            "is_read":
                self.is_read,

            "icon":
                self.icon,

            "link":
                self.link,

            "created_at":
                self.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )

        }



    def __repr__(self):

        return (
            f"<Notification {self.title}>"
        )