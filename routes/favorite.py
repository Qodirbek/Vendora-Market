from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    request
)

from extensions import db

from models.favorite import Favorite
from models.product import Product

from datetime import datetime


favorite = Blueprint(
    "favorite",
    __name__,
    url_prefix="/favorite"
)



# =====================================
# FAVORITES PAGE
# =====================================

@favorite.route("/")
def index():

    if "user_id" not in session:
        flash(
            "Sevimlilar uchun tizimga kiring",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    favorites = Favorite.query.filter_by(
        user_id=user_id
    ).order_by(
        Favorite.created_at.desc()
    ).all()



    products = [
        item.product
        for item in favorites
    ]


    return render_template(
        "favorite/index.html",
        favorites=favorites,
        products=products
    )



# =====================================
# ADD FAVORITE AJAX
# =====================================

@favorite.route(
    "/add/<int:product_id>",
    methods=["POST"]
)
def add(product_id):

    if "user_id" not in session:

        return jsonify({
            "success":False,
            "message":"Login kerak"
        }),401



    user_id = session["user_id"]



    product = Product.query.get_or_404(
        product_id
    )



    exists = Favorite.query.filter_by(
        user_id=user_id,
        product_id=product.id
    ).first()



    if exists:

        return jsonify({

            "success":False,

            "message":
            "Bu mahsulot allaqachon sevimlida"

        })



    favorite_item = Favorite(

        user_id=user_id,

        product_id=product.id,

        created_at=datetime.utcnow()

    )


    db.session.add(
        favorite_item
    )

    db.session.commit()



    return jsonify({

        "success":True,

        "message":
        "Sevimlilarga qo'shildi ❤️"

    })



# =====================================
# REMOVE FAVORITE AJAX
# =====================================


@favorite.route(
"/remove/<int:id>",
methods=["POST"]
)
def remove(id):


    if "user_id" not in session:

        return jsonify({
            "success":False
        }),401



    item = Favorite.query.get_or_404(
        id
    )


    if item.user_id != session["user_id"]:

        return jsonify({

            "success":False,

            "message":
            "Ruxsat yo'q"

        }),403



    db.session.delete(
        item
    )

    db.session.commit()



    return jsonify({

        "success":True,

        "message":
        "O'chirildi"

    })




# =====================================
# CHECK FAVORITE ICON
# =====================================


@favorite.route(
    "/check/<int:product_id>"
)
def check(product_id):


    if "user_id" not in session:

        return jsonify({

            "favorite":False

        })


    exists = Favorite.query.filter_by(

        user_id=session["user_id"],

        product_id=product_id

    ).first()



    return jsonify({

        "favorite":
        bool(exists)

    })



# =====================================
# TOGGLE FAVORITE
# =====================================


@favorite.route(
    "/toggle/<int:product_id>",
    methods=["POST"]
)
def toggle(product_id):


    if "user_id" not in session:

        return jsonify({

            "success":False,

            "login":True

        })



    user_id=session["user_id"]



    item = Favorite.query.filter_by(

        user_id=user_id,

        product_id=product_id

    ).first()



    if item:


        db.session.delete(item)

        db.session.commit()


        return jsonify({

            "favorite":False,

            "message":
            "Sevimlilardan olindi"

        })



    new_item = Favorite(

        user_id=user_id,

        product_id=product_id

    )


    db.session.add(
        new_item
    )

    db.session.commit()



    return jsonify({

        "favorite":True,

        "message":
        "Sevimlilarga qo'shildi ❤️"

    })