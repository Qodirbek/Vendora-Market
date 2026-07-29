from extensions import db
from datetime import datetime



class OrderItem(db.Model):

    __tablename__ = "order_item"


    # =========================
    # STATUS
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
    # BASIC
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # =========================
    # ORDER
    # =========================

    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "order.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )



    # =========================
    # PRODUCT
    # =========================

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "product.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )



    # =========================
    # PRODUCT SNAPSHOT
    # =========================

    product_name = db.Column(
        db.String(200),
        nullable=False
    )


    product_image = db.Column(
        db.String(500)
    )


    product_brand = db.Column(
        db.String(100)
    )


    product_sku = db.Column(
        db.String(100)
    )



    # =========================
    # SELLER
    # =========================


    seller_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "seller.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )


    seller_name = db.Column(
        db.String(200)
    )



    # =========================
    # PRICE
    # =========================


    price = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )


    subtotal = db.Column(
        db.Integer,
        default=0
    )



    # =========================
    # COMMISSION
    # =========================


    commission_percent = db.Column(
        db.Integer,
        default=10
    )


    commission = db.Column(
        db.Integer,
        default=0
    )


    seller_income = db.Column(
        db.Integer,
        default=0
    )



    # =========================
    # STATUS
    # =========================


    status = db.Column(
        db.String(50),
        default=STATUS_NEW,
        index=True
    )



    # =========================
    # TIME
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
    # RELATIONSHIPS
    # =========================


    order = db.relationship(
        "Order",
        back_populates="items"
    )


    product = db.relationship(
        "Product",
        back_populates="order_items"
    )


    seller = db.relationship(
        "Seller",
        back_populates="order_items"
    )



    # =========================
    # FUNCTIONS
    # =========================


    def calculate_subtotal(self):

        self.subtotal = (
            self.price *
            self.quantity
        )

        return self.subtotal




    def calculate_commission(self, percent=None):

        if percent is not None:
            self.commission_percent = percent

        if self.commission_percent is None:
            self.commission_percent = 10

        if self.subtotal is None:
            self.subtotal = 0

        self.commission = int(
            self.subtotal *
            self.commission_percent /
            100
        )

        self.seller_income = (
            self.subtotal -
            self.commission
        )

        return self.seller_income





    # BUYURTMA PAYTIDA
    # PRODUCT MA'LUMOTINI SAQLASH


    def create_snapshot(self):
        if not self.product:
            raise Exception(
                "Product topilmadi"
            )

        self.product_name = self.product.name
        self.product_image = self.product.image
        self.product_brand = self.product.brand
        self.product_sku = self.product.sku

        self.price = self.product.price

        self.seller_id = self.product.seller_id

        if self.product.seller:
            self.seller_name = (
                self.product.seller.shop_name
            )
        else:
            self.seller_name = "Admin"

        self.calculate_subtotal()

        self.calculate_commission()

        return True





    def increase_quantity(
        self,
        amount=1
    ):

        self.quantity += amount

        self.calculate_subtotal()

        self.calculate_commission()



    def decrease_quantity(
        self,
        amount=1
    ):

        if self.quantity > amount:

            self.quantity -= amount

            self.calculate_subtotal()

            self.calculate_commission()

            return True


        return False





    # =========================
    # STATUS
    # =========================


    def set_status(
        self,
        status
    ):

        if status in self.STATUSES:

            self.status = status

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



    def cancel(self):

        self.status = self.STATUS_CANCELLED




    def is_done(self):

        return (
            self.status ==
            self.STATUS_DONE
        )



    # =========================
    # DISPLAY
    # =========================


    def formatted_price(self):

        return f"{self.subtotal:,} so'm"




    def to_dict(self):

        return {

            "id":
                self.id,


            "product":
                self.product_name,


            "image":
                self.product_image,


            "quantity":
                self.quantity,


            "price":
                self.price,


            "subtotal":
                self.subtotal,


            "seller":
                self.seller_name,


            "status":
                self.status

        }




    def __repr__(self):

        return (
            f"<OrderItem {self.product_name}>"
        )