from extensions import db
from datetime import datetime
from slugify import slugify
import json


class Product(db.Model):

    __tablename__ = "product"


    # =========================
    # BASIC
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    offer_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )


    sku = db.Column(
        db.String(100),
        unique=True,
        index=True
    )


    name = db.Column(
        db.String(200),
        nullable=False,
        index=True
    )


    slug = db.Column(
        db.String(250),
        unique=True,
        index=True
    )


    description = db.Column(
        db.Text
    )


    brand = db.Column(
        db.String(100)
    )


    # =========================
    # PRICE
    # =========================

    price = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


    old_price = db.Column(
        db.Integer,
        default=0
    )


    discount = db.Column(
        db.Integer,
        default=0
    )


    # =========================
    # IMAGE
    # =========================

    image = db.Column(
        db.String(500)
    )


    images = db.Column(
        db.Text,
        default="[]"
    )


    def get_images(self):

        try:
            return json.loads(
                self.images
            )

        except:
            return []


    def set_images(self, images):

        self.images = json.dumps(
            images,
            ensure_ascii=False
        )


    # =========================
    # STOCK
    # =========================

    stock = db.Column(
        db.Integer,
        default=0
    )


    sold_count = db.Column(
        db.Integer,
        default=0
    )


    # =========================
    # STATISTICS
    # =========================

    views = db.Column(
        db.Integer,
        default=0
    )


    rating = db.Column(
        db.Float,
        default=0
    )


    reviews_count = db.Column(
        db.Integer,
        default=0
    )


    # =========================
    # STATUS
    # =========================

    active = db.Column(
        db.Boolean,
        default=False
    )


    approved = db.Column(
        db.Boolean,
        default=False
    )


    deleted = db.Column(
        db.Boolean,
        default=False
    )


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
    # CATEGORY
    # =========================

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "category.id"
        )
    )


    category = db.relationship(
        "Category",
        back_populates="products"
    )


    # =========================
    # SELLER
    # =========================

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "seller.id"
        ),
        index=True
    )


    seller = db.relationship(
        "Seller",
        back_populates="products"
    )


    # =========================
    # CART
    # =========================

    cart_items = db.relationship(
        "Cart",
        back_populates="product",
        cascade="all, delete-orphan"
    )


    # =========================
    # FAVORITE
    # =========================

    favorites = db.relationship(
        "Favorite",
        back_populates="product",
        cascade="all, delete-orphan"
    )


    # =========================
    # REVIEW
    # =========================

    reviews = db.relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )


    # =========================
    # ORDER
    # =========================

    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )

    # =========================
    # NOTIFICATIONS
    # =========================

    notifications = db.relationship(
        "Notification",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # =========================
    # METHODS
    # =========================

    def create_slug(self):
        import uuid
        from slugify import slugify

        base = slugify(self.name)

        self.slug = (
            base
            + "-"
            + str(uuid.uuid4())[:8]
        )

    def calculate_discount(self):
        if self.old_price and self.old_price > self.price:
            self.discount = int(
                (
                    (
                        self.old_price -
                        self.price
                    )
                    /
                    self.old_price
                )
                * 100
            )
        else:
            self.discount = 0



    def increase_view(self):

        self.views += 1



    def increase_sale(self, quantity=1):

        self.sold_count += quantity

        if self.stock >= quantity:

            self.stock -= quantity



    def update_rating(self):

        total = 0
        count = 0


        for review in self.reviews:

            if review.approved:

                total += review.rating
                count += 1


        if count:

            self.rating = round(
                total/count,
                1
            )

            self.reviews_count = count


        else:

            self.rating = 0
            self.reviews_count = 0



    def is_available(self):

        return (
            self.active
            and
            self.approved
            and
            not self.deleted
            and
            self.stock > 0
        )



    def soft_delete(self):

        self.deleted = True
        self.active = False



    def approve(self):

        self.approved = True
        self.active = True



    def formatted_price(self):

        return f"{self.price:,}"



    def __repr__(self):

        return f"<Product {self.name}>"