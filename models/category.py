from extensions import db


class Category(db.Model):

    __tablename__ = "category"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(100),
        nullable=False
    )


    icon = db.Column(
        db.String(100),
        default="bi-grid"
    )


    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )


    # =========================
    # PRODUCTS
    # =========================

    products = db.relationship(
        "Product",
        back_populates="category",
        lazy=True
    )


    def __repr__(self):
        return f"<Category {self.name}>"