from extensions import db
from datetime import datetime


class Cart(db.Model):

    __tablename__ = "cart"


    # ======================
    # BASIC
    # ======================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ======================
    # USER
    # ======================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id"
        ),
        nullable=False,
        index=True
    )



    # ======================
    # PRODUCT
    # ======================

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "product.id"
        ),
        nullable=False,
        index=True
    )



    # ======================
    # QUANTITY
    # ======================

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )



    # ======================
    # CHECKOUT
    # ======================

    selected = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )



    # ======================
    # TIME
    # ======================

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



    # ======================
    # RELATIONSHIP
    # ======================

    user = db.relationship(
        "User",
        back_populates="carts"
    )

    user = db.relationship(
    "User",
    back_populates="carts"
    )


    product = db.relationship(
        "Product",
        back_populates="cart_items"
    )



    # ======================
    # QUANTITY METHODS
    # ======================


    def increase(self, amount=1):

        if amount > 0:

            self.quantity += amount

        return self.quantity



    def decrease(self, amount=1):

        if (
            amount > 0
            and
            self.quantity > amount
        ):

            self.quantity -= amount

            return True


        return False



    def set_quantity(self, quantity):

        if quantity < 1:

            quantity = 1


        self.quantity = quantity

        return self.quantity



    # ======================
    # PRICE
    # ======================


    def unit_price(self):

        if self.product:

            return (
                self.product.price or 0
            )

        return 0



    def total_price(self):

        return (
            self.unit_price()
            *
            self.quantity
        )



    @property
    def subtotal(self):

        return self.total_price()



    # ======================
    # STOCK CHECK
    # ======================


    def available(self):

        if not self.product:

            return False


        return (
            self.product.stock
            >=
            self.quantity
        )



    def stock_left(self):

        if self.product:

            return self.product.stock


        return 0



    # ======================
    # SELECT
    # ======================


    def select(self):

        self.selected = True



    def unselect(self):

        self.selected = False



    # ======================
    # API
    # ======================


    def to_dict(self):

        return {

            "id":
                self.id,


            "product_id":
                self.product_id,


            "name":
                (
                    self.product.name
                    if self.product
                    else None
                ),


            "image":
                (
                    self.product.image
                    if self.product
                    else None
                ),


            "price":
                self.unit_price(),


            "quantity":
                self.quantity,


            "subtotal":
                self.subtotal,


            "stock":
                self.stock_left(),


            "available":
                self.available(),


            "selected":
                self.selected

        }



    # ======================
    # DISPLAY
    # ======================


    def formatted_price(self):

        return (
            f"{self.total_price():,} so'm"
        )



    def __repr__(self):

        return (
            f"<Cart {self.id}>"
        )