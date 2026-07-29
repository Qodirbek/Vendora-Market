from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request
)

from extensions import db

from models.user import User
from models.order import Order
from models.favorite import Favorite
from models.cart import Cart


profile = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


# =====================================
# PROFIL BOSH SAHIFA
# =====================================
@profile.route("/")
def index():

    if "user_id" not in session:
        flash(
            "Profilni ko'rish uchun tizimga kiring",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    user = User.query.get_or_404(
        user_id
    )


    # BUYURTMALAR

    orders = Order.query.filter_by(
        user_id=user_id
    ).order_by(
        Order.created_at.desc()
    ).limit(5).all()



    total_orders = Order.query.filter_by(
        user_id=user_id
    ).count()



    waiting_orders = Order.query.filter_by(
        user_id=user_id,
        status=Order.STATUS_NEW
    ).count()



    finished_orders = Order.query.filter_by(
        user_id=user_id,
        status=Order.STATUS_DONE
    ).count()



    spent_money = db.session.query(
        db.func.sum(Order.total_price)
    ).filter_by(
        user_id=user_id
    ).scalar() or 0



    favorite_count = Favorite.query.filter_by(
        user_id=user_id
    ).count()



    cart_count = Cart.query.filter_by(
        user_id=user_id
    ).count()



    return render_template(
        "profile/index.html",

        user=user,

        orders=orders,

        total_orders=total_orders,

        waiting_orders=waiting_orders,

        finished_orders=finished_orders,

        spent_money=spent_money,

        favorite_count=favorite_count,

        cart_count=cart_count
    )



# =====================================
# BUYURTMALARIM
# =====================================
@profile.route("/orders")
def orders():


    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.created_at.desc()
    ).all()



    return render_template(
        "profile/orders.html",
        orders=orders
    )



# =====================================
# BUYURTMA DETAIL
# =====================================
@profile.route(
    "/orders/<int:id>"
)
def order_detail(id):


    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )



    order = Order.query.filter_by(

        id=id,

        user_id=session["user_id"]

    ).first_or_404()



    return render_template(

        "profile/order_detail.html",

        order=order

    )



# =====================================
# PROFILNI TAHRIRLASH
# =====================================
@profile.route(
    "/edit",
    methods=["GET","POST"]
)
def edit():


    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    user = User.query.get_or_404(
        session["user_id"]
    )


    if request.method == "POST":


        user.name = request.form.get(
            "name"
        )


        user.phone = request.form.get(
            "phone"
        )


        user.email = request.form.get(
            "email"
        )


        db.session.commit()



        flash(
            "Profil yangilandi ✅",
            "success"
        )


        return redirect(
            url_for("profile.index")
        )


    return render_template(
        "profile/edit.html",
        user=user
    )



# =====================================
# MANZIL
# =====================================
@profile.route("/address")
def address():


    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    user = User.query.get_or_404(
        session["user_id"]
    )


    return render_template(
        "profile/address.html",
        user=user
    )



# =====================================
# CHIQISH
# =====================================
@profile.route("/logout")
def logout():

    session.clear()


    flash(
        "Tizimdan chiqdingiz",
        "info"
    )


    return redirect(
        url_for("home.index")
    )

# =====================================
# SUPPORT
# =====================================
@profile.route("/support")
def support():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "profile/support.html"
    )



# =====================================
# SETTINGS
# =====================================
@profile.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "profile/settings.html"
    )