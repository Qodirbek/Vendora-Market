from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response
)

from extensions import db

from models.seller import Seller
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.withdraw_request import WithdrawRequest
from models.notification import Notification

from seller.decorators import seller_required

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from datetime import datetime

import os
import uuid
import secrets


seller = Blueprint(
    "seller",
    __name__,
    url_prefix="/seller"
)


UPLOAD_FOLDER = "static/uploads/products"

ALLOWED_IMAGE = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_image(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_IMAGE
    )


def save_product_image(file):

    if not file:
        return None

    if not allowed_image(file.filename):
        return None


    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    filename = (
        str(uuid.uuid4())
        +
        "_"
        +
        secure_filename(
            file.filename
        )
    )


    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    file.save(path)


    return (
        "/static/uploads/products/"
        +
        filename
    )


# =====================================
# REGISTER
# =====================================

@seller.route(
    "/register",
    methods=["GET","POST"]
)
def register():

    if request.method == "POST":

        phone = request.form.get(
            "phone"
        )


        exists = Seller.query.filter_by(
            phone=phone
        ).first()


        if exists:

            flash(
                "Bu telefon mavjud",
                "danger"
            )

            return redirect(
                url_for(
                    "seller.register"
                )
            )


        seller_user = Seller(

            name=request.form.get(
                "name"
            ),

            phone=phone,

            email=request.form.get(
                "email"
            ),

            shop_name=request.form.get(
                "shop_name"
            ),

            address=request.form.get(
                "address"
            ),

            password=
            generate_password_hash(
                request.form.get(
                    "password"
                )
            ),

            status="pending",

            verified=False
        )


        db.session.add(
            seller_user
        )

        db.session.commit()


        flash(
            "Ariza yuborildi",
            "success"
        )


        return redirect(
            url_for(
                "seller.login"
            )
        )


    return render_template(
        "seller/register.html"
    )



# =====================================
# LOGIN
# =====================================


@seller.route(
    "/login",
    methods=["GET","POST"]
)
def login():

    if request.method == "POST":


        user = Seller.query.filter_by(
            phone=request.form.get(
                "phone"
            )
        ).first()


        if not user:

            flash(
                "Telefon yoki parol xato",
                "danger"
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        if not check_password_hash(
            user.password,
            request.form.get(
                "password"
            )
        ):

            flash(
                "Telefon yoki parol xato",
                "danger"
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        if user.status != "active":

            flash(
                "Admin tasdiqlashini kuting",
                "warning"
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        session["seller_id"] = user.id


        user.last_login = datetime.utcnow()


        token = secrets.token_hex(32)

        user.remember_token = token


        db.session.commit()


        response = make_response(
            redirect(
                url_for(
                    "seller.dashboard"
                )
            )
        )


        response.set_cookie(
            "seller_token",
            token,
            max_age=60*60*24*30
        )


        return response


    return render_template(
        "seller/login.html"
    )



# =====================================
# LOGOUT
# =====================================


@seller.route(
    "/logout"
)
def logout():

    session.pop(
        "seller_id",
        None
    )


    response = make_response(
        redirect(
            url_for(
                "seller.login"
            )
        )
    )


    response.delete_cookie(
        "seller_token"
    )


    return response



# =====================================
# DASHBOARD
# =====================================


@seller.route("/")
@seller_required
def dashboard():


    seller_user = Seller.query.get_or_404(
        session["seller_id"]
    )


    product_count = Product.query.filter_by(
        seller_id=seller_user.id
    ).count()


    order_count = OrderItem.query.filter_by(
        seller_id=seller_user.id
    ).count()


    sales = db.session.query(
        db.func.sum(
            OrderItem.subtotal
        )
    ).filter_by(
        seller_id=seller_user.id
    ).scalar() or 0



    return render_template(
        "seller/dashboard.html",
        seller=seller_user,
        product_count=product_count,
        order_count=order_count,
        total_sales=sales
    )



# =====================================
# PROFILE
# =====================================


@seller.route(
    "/profile"
)
@seller_required
def profile():

    seller_user = Seller.query.get_or_404(
        session["seller_id"]
    )


    return render_template(
        "seller/profile.html",
        seller=seller_user
    )

# =====================================
# ADD PRODUCT
# =====================================

@seller.route(
    "/products/add",
    methods=["GET","POST"]
)
@seller_required
def add_product():

    seller_id = session.get(
        "seller_id"
    )


    if request.method == "POST":


        image_file = request.files.get(
            "image"
        )


        image_path = save_product_image(
            image_file
        )


        price = int(
            request.form.get(
                "price"
            )
            or 0
        )


        old_price = int(
            request.form.get(
                "old_price"
            )
            or 0
        )


        stock = int(
            request.form.get(
                "stock"
            )
            or 0
        )


        product = Product(

            offer_id=
            "SELLER-"
            +
            str(
                uuid.uuid4()
            )[:8],


            sku=
            "SKU-"
            +
            secrets.token_hex(4),


            name=request.form.get(
                "name"
            ),


            brand=request.form.get(
                "brand"
            ),


            description=request.form.get(
                "description"
            ),


            price=price,


            old_price=old_price,


            stock=stock,


            image=image_path,


            seller_id=seller_id,


            active=False,


            approved=False
        )


        # agar Product modelda bo'lsa
        product.create_slug()


        # chegirma hisoblash
        if hasattr(
            product,
            "calculate_discount"
        ):
            product.calculate_discount()



        db.session.add(
            product
        )


        db.session.commit()



        flash(
            "Mahsulot yuborildi. Admin tasdiqlashi kerak",
            "success"
        )


        return redirect(
            url_for(
                "seller.products"
            )
        )



    return render_template(
        "seller/add_product.html"
    )



# =====================================
# PRODUCTS LIST
# =====================================


@seller.route(
    "/products"
)
@seller_required
def products():


    seller_id = session.get(
        "seller_id"
    )


    products = Product.query.filter_by(
        seller_id=seller_id,
        deleted=False
    ).order_by(
        Product.created_at.desc()
    ).all()



    return render_template(
        "seller/products.html",
        products=products
    )

# =====================================
# EDIT PRODUCT
# =====================================

@seller.route(
    "/products/edit/<int:id>",
    methods=["GET","POST"]
)
@seller_required
def edit_product(id):

    seller_id = session.get("seller_id")

    product = Product.query.filter_by(
        id=id,
        seller_id=seller_id
    ).first_or_404()


    if request.method == "POST":

        product.name = request.form.get("name")
        product.brand = request.form.get("brand")
        product.description = request.form.get("description")

        product.price = int(
            request.form.get("price") or 0
        )

        product.old_price = int(
            request.form.get("old_price") or 0
        )

        product.stock = int(
            request.form.get("stock") or 0
        )


        # yangi rasm yuklansa
        image = request.files.get("image")

        if image and image.filename:

            new_image = save_product_image(image)

            if new_image:
                product.image = new_image


        if hasattr(product,"calculate_discount"):
            product.calculate_discount()


        db.session.commit()


        flash(
            "Mahsulot muvaffaqiyatli yangilandi",
            "success"
        )


        return redirect(
            url_for(
                "seller.products"
            )
        )


    return render_template(
        "seller/product_edit.html",
        product=product
    )

# =====================================
# DELETE PRODUCT
# =====================================


@seller.route(
    "/products/delete/<int:id>"
)
@seller_required
def delete_product(id):


    seller_id = session.get(
        "seller_id"
    )


    product = Product.query.filter_by(
        id=id,
        seller_id=seller_id
    ).first()



    if not product:

        flash(
            "Mahsulot topilmadi",
            "danger"
        )


        return redirect(
            url_for(
                "seller.products"
            )
        )



    # rasmni ham o'chirish

    if product.image:

        image_file = product.image.replace(
            "/",
            os.sep
        ).lstrip(
            os.sep
        )


        if os.path.exists(
            image_file
        ):

            os.remove(
                image_file
            )



    db.session.delete(
        product
    )


    db.session.commit()



    flash(
        "Mahsulot o'chirildi",
        "success"
    )


    return redirect(
        url_for(
            "seller.products"
        )
    )



# =====================================
# SELLER ORDERS
# =====================================


@seller.route(
    "/orders"
)
@seller_required
def orders():


    seller_id = session.get(
        "seller_id"
    )


    orders = (
        Order.query
        .join(
            OrderItem
        )
        .filter(
            OrderItem.seller_id == seller_id
        )
        .order_by(
            Order.created_at.desc()
        )
        .all()
    )


    return render_template(
        "seller/orders.html",
        orders=orders
    )



# =====================================
# ORDER DETAIL
# =====================================


@seller.route(
    "/orders/<int:id>"
)
@seller_required
def order_detail(id):


    seller_id = session.get(
        "seller_id"
    )


    order = (
        Order.query
        .join(
            OrderItem
        )
        .filter(
            Order.id == id,
            OrderItem.seller_id == seller_id
        )
        .first()
    )


    if not order:

        flash(
            "Buyurtma topilmadi",
            "danger"
        )


        return redirect(
            url_for(
                "seller.orders"
            )
        )


    return render_template(
        "seller/order_detail.html",
        order=order
    )

# =====================================
# CHANGE ORDER STATUS
# FAQAT BOSQICHMA-BOSQICH
# =====================================

@seller.route(
    "/orders/<int:id>/status",
    methods=["POST"]
)
@seller_required
def change_order_status(id):

    seller_id = session.get("seller_id")

    order = (
        Order.query
        .join(OrderItem)
        .filter(
            Order.id == id,
            OrderItem.seller_id == seller_id
        )
        .first()
    )


    if not order:
        flash(
            "Buyurtma topilmadi",
            "danger"
        )
        return redirect(
            url_for("seller.orders")
        )


    action = request.form.get("action")


    # =================================
    # YANGI BUYURTMA
    # =================================

    if order.status == "Kutilmoqda":


        if action == "accept":

            order.status = "Tayyorlanmoqda"


        elif action == "cancel":

            order.status = "Bekor qilindi"


        else:
            flash(
                "Noto'g'ri amal",
                "danger"
            )


    # =================================
    # TAYYORLANMOQDA
    # =================================

    elif order.status == "Tayyorlanmoqda":


        if action == "ready":

            order.status = "Yetkazilmoqda"


        else:
            flash(
                "Avval tayyorlashni tugating",
                "warning"
            )


    # =================================
    # YETKAZILMOQDA
    # SELLER TEGOLMAYDI
    # =================================

    elif order.status == "Yetkazilmoqda":

        flash(
            "Buyurtma yetkazilmoqda. Statusni faqat admin o'zgartiradi",
            "warning"
        )


    # =================================
    # YAKUNLANGAN
    # =================================

    elif order.status in [
        "Yetkazildi",
        "Bekor qilindi"
    ]:

        flash(
            "Bu buyurtma yopilgan",
            "warning"
        )


    # OrderItem ham yangilansin

    for item in order.items:

        if item.seller_id == seller_id:
            item.status = order.status


    db.session.commit()


    flash(
        "Buyurtma holati yangilandi",
        "success"
    )


    return redirect(
        url_for(
            "seller.order_detail",
            id=id
        )
    )





# =====================================
# WITHDRAW
# =====================================


@seller.route(
    "/withdraw",
    methods=["GET","POST"]
)
@seller_required
def withdraw():


    seller_user = Seller.query.get_or_404(
        session["seller_id"]
    )



    if request.method == "POST":


        try:

            amount = int(
                request.form.get(
                    "amount"
                )
            )

        except:


            flash(
                "Summani to'g'ri kiriting",
                "danger"
            )


            return redirect(
                url_for(
                    "seller.withdraw"
                )
            )



        if amount <= 0:


            flash(
                "Noto'g'ri summa",
                "danger"
            )


            return redirect(
                url_for(
                    "seller.withdraw"
                )
            )



        if amount > seller_user.balance:


            flash(
                "Balans yetarli emas",
                "danger"
            )


            return redirect(
                url_for(
                    "seller.withdraw"
                )
            )



        withdraw = WithdrawRequest(

            seller_id=seller_user.id,

            amount=amount,

            phone=seller_user.phone,

            status="pending"

        )



        db.session.add(
            withdraw
        )


        db.session.commit()



        flash(
            "Pul yechish so'rovi yuborildi",
            "success"
        )



        return redirect(
            url_for(
                "seller.dashboard"
            )
        )



    return render_template(
        "seller/withdraw.html",
        seller=seller_user
    )





# =====================================
# REMEMBER LOGIN
# =====================================


@seller.route(
    "/remember"
)
def remember_login():


    token = request.cookies.get(
        "seller_token"
    )


    if not token:


        return redirect(
            url_for(
                "seller.login"
            )
        )



    seller_user = Seller.query.filter_by(
        remember_token=token
    ).first()



    if seller_user:


        session["seller_id"] = seller_user.id


        return redirect(
            url_for(
                "seller.dashboard"
            )
        )



    return redirect(
        url_for(
            "seller.login"
        )
    )





# =====================================
# NOTIFICATIONS
# =====================================


@seller.route(
    "/notifications"
)
@seller_required
def notifications():


    seller_id = session.get(
        "seller_id"
    )


    notes = Notification.query.filter_by(
        seller_id=seller_id
    ).order_by(
        Notification.created_at.desc()
    ).all()



    return render_template(
        "seller/notifications.html",
        notifications=notes
    )





# =====================================
# SELLER ERROR HANDLER
# =====================================


@seller.errorhandler(
    404
)
def seller_not_found(error):


    return render_template(
        "seller/errors/404.html"
    ),404





@seller.errorhandler(
    500
)
def seller_server_error(error):


    db.session.rollback()


    return render_template(
        "seller/errors/500.html"
    ),500

# =====================================
# CATEGORIES
# =====================================





# =====================================
# DELETE CATEGORY
# =====================================




# =====================================
# SELLERS
# =====================================

# =====================================
# SELLER BALANCE
# =====================================

@seller.route("/balance")
def balance():

    seller_id = 1  # vaqtincha test uchun

    seller_user = Seller.query.get_or_404(
        seller_id
    )

    return render_template(
        "seller/balance.html",
        seller=seller_user
    )