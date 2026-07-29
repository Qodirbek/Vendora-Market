from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from extensions import db
from models.cart import Cart
from models.order import Order
from models.order_item import OrderItem


order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/order"
)


# ================================
# BUYURTMALARIM
# ================================
@order_bp.route("/")
def orders():

    if "user_id" not in session:
        flash("Avval tizimga kiring", "warning")
        return redirect(
            url_for("auth.login")
        )

    orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.created_at.desc()
    ).all()


    return render_template(
        "order/orders.html",
        orders=orders
    )



# ================================
# CHECKOUT
# ================================
@order_bp.route("/checkout")
def checkout():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    cart_items = Cart.query.filter_by(
        user_id=session["user_id"]
    ).all()


    if not cart_items:
        flash(
            "Savat bo'sh",
            "warning"
        )

        return redirect(
            url_for("cart.index")
        )


    total = sum(
        item.total_price()
        for item in cart_items
    )


    return render_template(
        "order/checkout.html",
        cart_items=cart_items,
        total=total
    )



# ================================
# CREATE ORDER
# ================================
@order_bp.route(
    "/create",
    methods=["POST"]
)
def create_order():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    cart_items = Cart.query.filter_by(
        user_id=user_id
    ).all()


    if not cart_items:

        flash(
            "Savat bo'sh",
            "danger"
        )

        return redirect(
            url_for("cart.index")
        )



    fullname = request.form.get(
        "fullname"
    )


    if not fullname:

        flash(
            "Ism familiya kiritilmagan",
            "danger"
        )

        return redirect(
            url_for("order.checkout")
        )



    phone = request.form.get(
        "phone"
    )


    address = f"""
{request.form.get('city')},
{request.form.get('mahalla')},
{request.form.get('street')},
Uy: {request.form.get('house')},
Xonadon: {request.form.get('apartment')},
Mo'ljal: {request.form.get('landmark')}
"""



    new_order = Order(

        user_id=user_id,

        receiver_name=fullname,

        phone=phone,

        country="Uzbekistan",

        region=request.form.get(
            "region"
        ),

        city=request.form.get(
            "city"
        ),

        district=request.form.get(
            "mahalla"
        ),

        street=request.form.get(
            "street"
        ),

        house=request.form.get(
            "house"
        ),

        apartment=request.form.get(
            "apartment"
        ),

        address=address,

        comment=request.form.get(
            "comment"
        ),

        payment_method=request.form.get(
            "payment_method"
        ),

        delivery_price=int(
            request.form.get(
                "delivery_price",
                0
            )
        )
    )



    new_order.generate_number()


    db.session.add(
        new_order
    )

    db.session.flush()


    # =================================
    # CART -> ORDER ITEM
    # =================================

    for cart in cart_items:

        item = OrderItem(
            order_id=new_order.id,
            product_id=cart.product_id,
            quantity=cart.quantity
        )

        item.product = cart.product

        item.create_snapshot()

        db.session.add(item)


    db.session.flush()


    # jami hisoblash

    new_order.calculate_total()


    # savatni tozalash

    for cart in cart_items:
        db.session.delete(cart)


    db.session.commit()


    flash(
        "Buyurtmangiz qabul qilindi ✅",
        "success"
    )


    return redirect(
        url_for(
            "order.detail",
            id=new_order.id
        )
    )



# ================================
# DETAIL
# ================================
@order_bp.route(
    "/detail/<int:id>"
)
def detail(id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    order = Order.query.filter_by(

        id=id,

        user_id=session["user_id"]

    ).first_or_404()



    return render_template(

        "order/detail.html",

        order=order

    )