from extensions import db
from datetime import datetime
import random


class Order(db.Model):

    __tablename__ = "order"


    # =========================
    # ORDER STATUS
    # =========================

    STATUS_NEW = "Kutilmoqda"
    STATUS_ACCEPTED = "Qabul qilindi"
    STATUS_PREPARING = "Tayyorlanmoqda"
    STATUS_SHIPPING = "Yetkazilmoqda"
    STATUS_DONE = "Yetkazildi"
    STATUS_CANCELLED = "Bekor qilindi"


    STATUSES = [
        STATUS_NEW,
        STATUS_ACCEPTED,
        STATUS_PREPARING,
        STATUS_SHIPPING,
        STATUS_DONE,
        STATUS_CANCELLED
    ]



    # =========================
    # PAYMENT STATUS
    # =========================

    PAYMENT_PENDING = "To'lanmagan"
    PAYMENT_PAID = "To'langan"
    PAYMENT_REFUND = "Qaytarilgan"


    PAYMENT_STATUSES = [
        PAYMENT_PENDING,
        PAYMENT_PAID,
        PAYMENT_REFUND
    ]



    # =========================
    # BASIC
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    order_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )


    tracking_code = db.Column(
        db.String(100),
        unique=True
    )



    # =========================
    # USER
    # =========================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )



    # =========================
    # PRICE
    # =========================

    subtotal = db.Column(
        db.Integer,
        default=0
    )


    delivery_price = db.Column(
        db.Integer,
        default=0
    )

    # =========================
    # DELIVERY
    # =========================
    
    delivery_type = db.Column(
        db.String(50),
        default="standard"
    )


    discount = db.Column(
        db.Integer,
        default=0
    )


    total_price = db.Column(
        db.Integer,
        default=0
    )



    # =========================
    # PAYMENT
    # =========================

    payment_method = db.Column(
        db.String(50),
        default="Naqd"
    )


    payment_status = db.Column(
        db.String(50),
        default=PAYMENT_PENDING
    )


    payment_check = db.Column(
        db.String(255),
        nullable=True
    )


    payment_verified = db.Column(
        db.Boolean,
        default=False
    )



    # =========================
    # STATUS
    # =========================

    status = db.Column(
        db.String(50),
        default=STATUS_NEW,
        index=True
    )


    status_note = db.Column(
        db.Text
    )



    # =========================
    # RECEIVER
    # =========================

    receiver_name = db.Column(
        db.String(100),
        nullable=False
    )


    phone = db.Column(
        db.String(30),
        nullable=False
    )


    country = db.Column(
        db.String(100),
        default="Uzbekistan"
    )


    region = db.Column(
        db.String(100)
    )


    city = db.Column(
        db.String(100)
    )


    district = db.Column(
        db.String(100)
    )


    street = db.Column(
        db.String(200)
    )


    house = db.Column(
        db.String(50)
    )


    apartment = db.Column(
        db.String(50)
    )


    address = db.Column(
        db.Text
    )


    comment = db.Column(
        db.Text
    )



    # =========================
    # CANCEL
    # =========================

    cancel_reason = db.Column(
        db.Text
    )



    # =========================
    # TIME
    # =========================

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


    completed_at = db.Column(
        db.DateTime
    )



    # =========================
    # RELATION
    # =========================

    user = db.relationship(
        "User",
        back_populates="orders"
    )


    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    user = db.relationship(
    "User",
    back_populates="orders"
    )


    notifications = db.relationship(
        "Notification",
        back_populates="order",
        cascade="all, delete-orphan"
    )



    # =========================
    # NUMBER
    # =========================

    def generate_number(self):

        while True:

            number = (
                "ORD-"
                +
                datetime.utcnow().strftime(
                    "%Y%m%d"
                )
                +
                "-"
                +
                str(
                    random.randint(
                        10000,
                        99999
                    )
                )
            )


            if not Order.query.filter_by(
                order_number=number
            ).first():

                self.order_number = number
                break



    def generate_tracking(self):

        while True:

            code = (
                "TRK-"
                +
                str(
                    random.randint(
                        100000,
                        999999
                    )
                )
            )


            if not Order.query.filter_by(
                tracking_code=code
            ).first():

                self.tracking_code = code
                break



    # =========================
    # TOTAL
    # =========================

    def calculate_total(self):

        items_total = 0


        for item in self.items:

            item.calculate_subtotal()

            items_total += (
                item.subtotal or 0
            )


        self.subtotal = items_total


        self.total_price = (
            self.subtotal
            +
            (self.delivery_price or 0)
            -
            (self.discount or 0)
        )


        return self.total_price



    # =========================
    # STATUS ACTIONS
    # =========================

    def set_status(self,status):

        if status in self.STATUSES:

            self.status = status
            self.updated_at = datetime.utcnow()

            return True

        return False



    def accept(self):

        self.status = self.STATUS_ACCEPTED



    def preparing(self):

        self.status = self.STATUS_PREPARING



    def shipping(self):

        self.status = self.STATUS_SHIPPING



    def complete(self):

        self.status = self.STATUS_DONE

        self.completed_at = datetime.utcnow()



    def cancel_order(
        self,
        reason=None
    ):

        self.status = self.STATUS_CANCELLED

        self.cancel_reason = reason



    # =========================
    # PAYMENT ACTIONS
    # =========================

    def paid(self):

        self.payment_status = self.PAYMENT_PAID

        self.payment_verified = True



    def refund(self):

        self.payment_status = self.PAYMENT_REFUND



    def is_paid(self):

        return (
            self.payment_status
            ==
            self.PAYMENT_PAID
        )



    # =========================
    # CHECK
    # =========================

    def is_completed(self):

        return (
            self.status
            ==
            self.STATUS_DONE
        )



    def is_cancelled(self):

        return (
            self.status
            ==
            self.STATUS_CANCELLED
        )



    # =========================
    # DISPLAY
    # =========================

    def formatted_price(self):

        return (
            f"{self.total_price or 0:,} so'm"
        )



    def item_count(self):

        return sum(
            item.quantity
            for item in self.items
        )



    # =========================
    # API
    # =========================

    def to_dict(self):

        return {

            "id": self.id,

            "order_number":
                self.order_number,

            "tracking":
                self.tracking_code,

            "status":
                self.status,


            "payment":
                {
                    "method":
                        self.payment_method,

                    "status":
                        self.payment_status
                },


            "receiver":
                {
                    "name":
                        self.receiver_name,

                    "phone":
                        self.phone,

                    "address":
                        self.address
                },


            "price":
                {
                    "subtotal":
                        self.subtotal,

                    "delivery":
                        self.delivery_price,

                    "total":
                        self.total_price
                },


            "items":[
                item.to_dict()
                for item in self.items
            ],


            "created":
                self.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
        }



    def __repr__(self):

        return (
            f"<Order {self.order_number}>"
        )