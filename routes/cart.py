from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from extensions import db

from models.cart import Cart
from models.product import Product



cart = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart"
)



# ==========================
# CART PAGE
# ==========================

@cart.route("/")
def index():

    if "user_id" not in session:
        flash(
            "Savat uchun tizimga kiring",
            "warning"
        )
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    items = Cart.query.filter_by(
        user_id=user_id
    ).order_by(
        Cart.created_at.desc()
    ).all()


    total = sum(
        item.total_price()
        for item in items
    )


    return render_template(
        "cart/index.html",
        cart_items=items,
        total=total
    )

@cart.route("/remove/<int:id>")
def remove(id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    item = Cart.query.get_or_404(id)


    if item.user_id != session["user_id"]:
        flash(
            "Ruxsat yo'q",
            "danger"
        )
        return redirect(
            url_for("cart.index")
        )


    db.session.delete(item)
    db.session.commit()


    flash(
        "Mahsulot savatdan o'chirildi",
        "success"
    )


    return redirect(
        url_for("cart.index")
    )





# ==========================
# ADD CART
# ==========================


@cart.route("/add/<int:product_id>")
def add(product_id):


    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )



    product = Product.query.get_or_404(
        product_id
    )



    item = Cart.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()



    if item:

        item.quantity += 1


    else:

        item = Cart(

            user_id=session["user_id"],

            product_id=product.id,

            quantity=1

        )

        db.session.add(item)



    db.session.commit()



    flash(
        "Mahsulot savatga qo'shildi 🛒",
        "success"
    )


    return redirect(
        url_for("cart.index")
    )





# ==========================
# INCREASE
# ==========================


@cart.route(
    "/increase/<int:id>",
    methods=["POST"]
)

def increase(id):


    item = Cart.query.get_or_404(id)



    item.quantity += 1



    db.session.commit()



    return jsonify({

        "success":True,

        "quantity":item.quantity,

        "total":item.total_price()

    })





# ==========================
# DECREASE
# ==========================


@cart.route(
    "/decrease/<int:id>",
    methods=["POST"]
)

def decrease(id):


    item = Cart.query.get_or_404(id)



    if item.quantity > 1:

        item.quantity -= 1


    else:

        db.session.delete(item)



    db.session.commit()



    return jsonify({

        "success":True

    })





# ==========================
# REMOVE
# ==========================





# ==========================
# CLEAR
# ==========================


@cart.route("/clear")

def clear():


    Cart.query.filter_by(
        user_id=session["user_id"]
    ).delete()



    db.session.commit()



    return redirect(
        url_for("cart.index")
    )