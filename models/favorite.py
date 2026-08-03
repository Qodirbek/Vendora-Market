from extensions import db
from datetime import datetime



class Favorite(db.Model):

    __tablename__ = "favorite"



    id = db.Column(

        db.Integer,

        primary_key=True

    )


    user_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "user.id"
        ),

        nullable=False,

        index=True

    )

    user = db.relationship(
    "User",
    back_populates="favorites"
    )



    product_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "product.id"
        ),

        nullable=False,

        index=True

    )



    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow,

        nullable=False

    )



    # =================================
    # RELATIONSHIPS
    # =================================


    product = db.relationship(

        "Product",

        back_populates="favorites"

    )


    user = db.relationship(

        "User",

        back_populates="favorites"

    )



    # =================================
    # FUNCTIONS
    # =================================


    def to_dict(self):

        return {

            "id":
            self.id,


            "product_id":
            self.product_id,


            "created_at":
            self.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

        }



    def __repr__(self):

        return (

            f"<Favorite user={self.user_id} "
            f"product={self.product_id}>"

        )