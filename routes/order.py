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


import os
from werkzeug.utils import secure_filename


order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/order"
)

# =================================
# BUYURTMALARIM
# =================================

@order_bp.route("/")
def orders():

    if "user_id" not in session:
        flash(
            "Avval tizimga kiring",
            "warning"
        )

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



# =================================
# CHECKOUT
# =================================

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


    subtotal = sum(
        item.total_price()
        for item in cart_items
    )


    return render_template(
        "order/checkout.html",
        cart_items=cart_items,
        total=subtotal
    )



# =================================
# CREATE ORDER
# =================================

@order_bp.route(
    "/create",
    methods=["POST"]
)
def create_order():
    print("creat order ishladi ✅")

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

    phone = request.form.get(
        "phone"
    )



    if not fullname or not phone:

        flash(
            "Ma'lumotlarni to'liq kiriting",
            "danger"
        )

        return redirect(
            url_for("order.checkout")
        )



    # ==========================
    # MAHSULOT SUMMASI
    # ==========================

    subtotal = sum(
        item.total_price()
        for item in cart_items
    )



    # ==========================
    # YETKAZISH
    # ==========================

    delivery_type = request.form.get(
        "delivery_type"
    )


    delivery_price = 0



    if delivery_type == "courier":

        # 1.2 mln dan oshsa bepul
        if subtotal >= 1200000:

            delivery_price = 0

        else:

            delivery_price = 30000



    else:

        # standart

        if subtotal >= 120000:

            delivery_price = 0


        elif subtotal >= 45000:

            delivery_price = 10000


        elif subtotal >= 10000:

            delivery_price = 20000


        else:

            delivery_price = 30000



    # ==========================
    # TO'LOV
    # ==========================

    payment_method = request.form.get(
        "payment_method"
    )


    payment_check_path = None


    if payment_method == "Karta":
        file = request.files.get(
            "payment_check"
        )

        print("CHEK KELDI:", file)

        if not file or file.filename == "":
            flash(
                "💳 Karta orqali to'lov uchun chek yuklang!",
                "danger"
            )
            return redirect(
                url_for("order.checkout")
            )

        filename = secure_filename(
            file.filename
        )

        folder = "static/uploads/payments"

        os.makedirs(
            folder,
            exist_ok=True
        )

        filepath = os.path.join(
            folder,
            filename
        )

        file.save(filepath)

        payment_check_path = "/" + filepath



    # ==========================
    # ADDRESS
    # ==========================

    address = f"""
{request.form.get('region')},
{request.form.get('city')},
{request.form.get('mahalla')},
{request.form.get('street')},
Uy: {request.form.get('house')},
Xonadon: {request.form.get('apartment')},
Mo'ljal: {request.form.get('landmark')}
"""



    # ==========================
    # ORDER CREATE
    # ==========================

    try:


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


            payment_method=payment_method,


            payment_check=payment_check_path,


            subtotal=subtotal,


            delivery_type=delivery_type,


            delivery_price=delivery_price

        )


        # agar modelda status bo'lsa
        # new_order.status="Yangi"



        new_order.generate_number()



        db.session.add(
            new_order
        )


        db.session.flush()



        # ======================
        # CART -> ORDER ITEM
        # ======================


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



        # jami:
        # mahsulot + yetkazish

        new_order.delivery_price = delivery_price


        new_order.calculate_total()



        # savat tozalash

        for cart in cart_items:

            db.session.delete(cart)



        db.session.commit()



    except Exception as e:


        db.session.rollback()


        print(e)


        flash(
            "Buyurtma yaratishda xatolik!",
            "danger"
        )


        return redirect(
            url_for("order.checkout")
        )



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





# =================================
# DETAIL
# =================================

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