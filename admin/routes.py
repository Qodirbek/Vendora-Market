from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db

from models.product import Product
from models.category import Category
from models.seller import Seller
from models.notification import Notification
from models.admin import Admin
from models.user import User


from flask import Blueprint

from werkzeug.utils import secure_filename

import os
from datetime import datetime

from flask_login import (
    login_user,
    logout_user,
    login_required
)



admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================
# UPLOAD SETTINGS
# ==========================

UPLOAD_FOLDER = "static/uploads/products"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)



def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".",1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



# ==========================
# DASHBOARD
# ==========================

@admin.route("/")
@login_required
def dashboard():

    products_count = Product.query.count()

    categories_count = Category.query.count()

    sellers_count = Seller.query.count()


    latest_products = Product.query.order_by(
        Product.created_at.desc()
    ).limit(5).all()


    return render_template(
        "admin/dashboard.html",
        products=products_count,
        categories=categories_count,
        sellers=sellers_count,
        orders=0,
        revenue=0,
        latest_products=latest_products
    )



# ==========================
# PRODUCTS LIST
# ==========================

@admin.route("/products")
def products():

    search = request.args.get(
        "search"
    )


    query = Product.query


    if search:

        query = query.filter(
            Product.name.contains(search)
        )


    products = query.order_by(
        Product.id.desc()
    ).all()



    return render_template(
        "admin/products.html",
        products=products
    )

# =====================================
# PRODUCT APPROVE (SELLER MAHSULOTI)
# =====================================



@admin.route(
    "/products/approve/<int:id>"
)
def approve_product(id):

    product = Product.query.get_or_404(id)

    product.approved = True
    product.active = True

    # sellerga notification
    if product.seller_id:

        notification = Notification(
            title="Mahsulot tasdiqlandi",
            message=f"{product.name} mahsulotingiz admin tomonidan tasdiqlandi va sotuvga chiqarildi",
            seller_id=product.seller_id
        )

        db.session.add(notification)


    db.session.commit()


    flash(
        "Mahsulot tasdiqlandi",
        "success"
    )


    return redirect(
        url_for(
            "admin.products"
        )
    )



# =====================================
# PRODUCT REJECT
# =====================================

@admin.route(
    "/products/reject/<int:id>"
)
def reject_product(id):

    product = Product.query.get_or_404(id)


    product.approved = False
    product.active = False


    if product.seller_id:

        notification = Notification(
            title="Mahsulot rad etildi",
            message=f"{product.name} mahsulotingiz admin tomonidan rad qilindi",
            seller_id=product.seller_id
        )

        db.session.add(notification)


    db.session.commit()


    flash(
        "Mahsulot rad qilindi",
        "warning"
    )


    return redirect(
        url_for(
            "admin.products"
        )
    )





# =====================================
# ADD PRODUCT
# =====================================

@admin.route(
    "/products/add",
    methods=["GET","POST"]
)
def add_product():

    if request.method == "POST":

        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        if not name or not price:
            flash(
                "Nom va narx kerak",
                "danger"
            )
            return redirect(
                url_for("admin.add_product")
            )


        product = Product(
            offer_id="ADMIN-"+datetime.now().strftime("%Y%m%d%H%M%S"),
            name=name,
            price=int(price),
            description=description,
            approved=True,
            active=True
        )


        db.session.add(product)
        db.session.commit()


        flash(
            "Mahsulot qo'shildi",
            "success"
        )

        return redirect(
            url_for("admin.products")
        )


    categories = Category.query.all()

    return render_template(
        "admin/product_add.html",
        categories=categories
    )


# =====================================
# EDIT PRODUCT
# =====================================

@admin.route(
    "/products/edit/<int:id>",
    methods=["GET","POST"]
)
def edit_product(id):

    product = Product.query.get_or_404(id)


    if request.method == "POST":

        product.name = request.form.get(
            "name"
        )

        product.price = int(
            request.form.get("price") or 0
        )

        product.description = request.form.get(
            "description"
        )


        if request.form.get("brand"):
            product.brand = request.form.get(
                "brand"
            )


        db.session.commit()


        flash(
            "Mahsulot yangilandi",
            "success"
        )


        return redirect(
            url_for(
                "admin.products"
            )
        )


    return render_template(
        "admin/product_edit.html",
        product=product
    )

# =====================================
# DELETE PRODUCT    
# =====================================
@admin.route("/products/delete/<int:id>")
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("admin.products"))


# =====================================
# PENDING PRODUCTS
# =====================================

@admin.route(
    "/products/pending"
)
def pending_products():

    products = Product.query.filter_by(
        approved=False
    ).order_by(
        Product.created_at.desc()
    ).all()


    return render_template(
        "admin/pending_products.html",
        products=products
    )


#===========================
# USERS LIST admin
#===========================

@admin.route("/users")
def users():
    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )

@admin.route("/users/<int:id>")
def user_detail(id):

    user = User.query.get_or_404(id)

    total_buy = sum(
        order.total_price or 0
        for order in user.orders
    )

    return render_template(
        "admin/user_detail.html",
        user=user,
        total_buy=total_buy
    )


# =====================================
# SELLER DETAIL
# =====================================

@admin.route(
    "/sellers/<int:id>"
)
def seller_detail(id):

    seller = Seller.query.get_or_404(
        id
    )


    products = Product.query.filter_by(
        seller_id=id
    ).all()


    return render_template(
        "admin/seller_detail.html",
        seller=seller,
        products=products
    )



# =====================================
# SELLER DELETE
# =====================================

@admin.route(
    "/sellers/delete/<int:id>"
)
def delete_seller(id):

    seller = Seller.query.get_or_404(
        id
    )


    Product.query.filter_by(
        seller_id=id
    ).delete()


    db.session.delete(
        seller
    )


    db.session.commit()


    flash(
        "Seller o'chirildi",
        "success"
    )


    return redirect(
        url_for(
            "admin.sellers"
        )
    )



# =====================================
# SELLER NOTIFICATIONS
# =====================================

@admin.route(
    "/notifications"
)
def notifications():

    notes = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()


    return render_template(
        "admin/notifications.html",
        notifications=notes
    )

# =====================================
# APPROVE SELLER
# =====================================

# =====================================
# APPROVE SELLER
# =====================================

@admin.route(
    "/sellers/approve/<int:id>"
)
def approve_seller(id):

    seller = Seller.query.get_or_404(id)

    seller.activate()

    db.session.commit()

    flash(
        "Seller tasdiqlandi",
        "success"
    )

    return redirect(
        url_for(
            "admin.sellers"
        )
    )

# =====================================
# APPROVE SELLER
# =====================================


# =====================================
# REJECT SELLER
# =====================================

@admin.route(
    "/sellers/reject/<int:id>"
)
def reject_seller(id):

    seller = Seller.query.get_or_404(id)

    seller.status = "blocked"
    seller.verified = False
    seller.blocked_reason = "Admin tomonidan rad qilindi"

    db.session.commit()

    flash(
        "Seller rad qilindi",
        "warning"
    )

    return redirect(
        url_for(
            "admin.sellers"
        )
    )


# =====================================
# MARK NOTIFICATION READ
# =====================================

@admin.route(
    "/notifications/read/<int:id>"
)
def notification_read(id):

    note = Notification.query.get_or_404(
        id
    )


    note.is_read = True


    db.session.commit()


    return redirect(
        url_for(
            "admin.notifications"
        )
    )



# =====================================
# ORDERS LIST
# =====================================

from models.order import Order


@admin.route(
    "/orders"
)
def orders():

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()


    return render_template(
        "admin/orders.html",
        orders=orders
    )



# =====================================
# ORDER DETAIL
# =====================================

@admin.route(
    "/orders/<int:id>"
)
def order_detail(id):

    order = Order.query.get_or_404(
        id
    )


    return render_template(
        "admin/order_detail.html",
        order=order
    )



# =====================================
# CHANGE ORDER STATUS
# =====================================
@admin.route(
    "/orders/status/<int:id>",
    methods=["POST"]
)
def change_order_status(id):

    order = Order.query.get_or_404(id)

    status = request.form.get("status")

    allowed = [
        "Yangi",
        "Qabul qilindi",
        "Tayyorlanmoqda",
        "Yetkazilmoqda",
        "Yetkazildi",
        "Bekor qilindi"
    ]

    if status not in allowed:
        flash(
            "Noto'g'ri status",
            "danger"
        )
        return redirect(
            url_for(
                "admin.order_detail",
                id=id
            )
        )

    action = request.form.get("action")

    if action == "approve":
        order.payment_status = "To'langan"
        order.payment_verified = True
        order.status = "Qabul qilindi"
        db.session.commit()

    # Agar oldin yetkazilgan bo'lsa qayta pul bermaydi
    if order.completed_at and status == "Yetkazildi":
        flash(
            "Bu buyurtma allaqachon yakunlangan",
            "warning"
        )
        return redirect(
            url_for(
                "admin.order_detail",
                id=id
            )
        )


    order.status = status


    # =====================================
    # SELLER BALANCE
    # FAQAT YETKAZILGANDA
    # =====================================

    if status == "Yetkazildi":

        for item in order.items:

            seller = item.seller

            if seller:

                seller.add_income(
                    item.seller_income
                )

                seller.add_sale(
                    item.subtotal,
                    item.quantity
                )


            item.status = "Yetkazildi"


        order.completed_at = datetime.utcnow()



    db.session.commit()


    flash(
        "Buyurtma statusi yangilandi",
        "success"
    )


    return redirect(
        url_for(
            "admin.order_detail",
            id=id
        )
    )


# =====================================
# SELLERS LIST
# =====================================

@admin.route("/sellers")
@login_required
def sellers():

    sellers = Seller.query.order_by(
        Seller.id.desc()
    ).all()


    return render_template(
        "admin/sellers.html",
        sellers=sellers
    )



# =====================================
# REVIEWS
# =====================================

@admin.route("/reviews")
@login_required
def reviews():

    return render_template(
        "admin/reviews.html"
    )

# =========================
# BLOCK SELLER
# =========================

@admin.route("/sellers/block/<int:id>")
def block_seller(id):

    seller = Seller.query.get_or_404(id)

    seller.status = "blocked"
    seller.verified = False

    db.session.commit()

    flash(
        "Seller bloklandi",
        "warning"
    )

    return redirect(
        url_for(
            "admin.sellers"
        )
    )

# ==========================
# GIVE BONUS TO SELLER
# ==========================

@admin.route(
    "/sellers/bonus/<int:id>",
    methods=["POST"]
)
def give_bonus(id):

    seller = Seller.query.get_or_404(id)

    try:
        amount = int(
            request.form.get("amount")
        )
    except:
        flash(
            "Summani to'g'ri kiriting",
            "danger"
        )
        return redirect(
            url_for(
                "admin.seller_detail",
                id=id
            )
        )


    if amount <= 0:
        flash(
            "Noto'g'ri summa",
            "danger"
        )
        return redirect(
            url_for(
                "admin.seller_detail",
                id=id
            )
        )


    seller.balance += amount
    seller.total_income += amount


    db.session.commit()


    flash(
        f"{amount} so'm bonus berildi",
        "success"
    )


    return redirect(
        url_for(
            "admin.seller_detail",
            id=id
        )
    )

# ==========================
# SELLER WITHDRAW
# ==========================

@admin.route(
    "/sellers/withdraw/<int:id>",
    methods=["POST"]
)
def withdraw_seller(id):

    seller = Seller.query.get_or_404(id)

    try:
        amount = int(
            request.form.get("amount")
        )

    except:
        flash(
            "Summani to'g'ri kiriting",
            "danger"
        )
        return redirect(
            url_for(
                "admin.seller_detail",
                id=id
            )
        )


    if amount <= 0:
        flash(
            "Noto'g'ri summa",
            "danger"
        )
        return redirect(
            url_for(
                "admin.seller_detail",
                id=id
            )
        )


    if amount > seller.balance:
        flash(
            "Seller balansida yetarli pul yo'q",
            "danger"
        )
        return redirect(
            url_for(
                "admin.seller_detail",
                id=id
            )
        )


    # balansdan ayirish
    seller.balance -= amount


    # yechilgan pul statistikasi
    seller.withdrawn_money += amount


    db.session.commit()


    flash(
        f"{amount} so'm sellerga berildi",
        "success"
    )


    return redirect(
        url_for(
            "admin.seller_detail",
            id=id
        )
    )

@admin.route(
    "/login",
    methods=["GET","POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")


        admin_user = Admin.query.filter_by(
            username=username
        ).first()


        if admin_user and admin_user.check_password(password):

            login_user(admin_user)

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )


        flash(
            "Login yoki parol xato",
            "danger"
        )


    return render_template(
        "admin/login.html"
    )

admin_bp = admin

@admin.route("/categories/delete/<int:id>")
def delete_category(id):

    category = Category.query.get_or_404(id)

    # agar ichida mahsulot bo'lsa o'chirmaymiz
    if category.products:
        flash(
            "Bu kategoriyada mahsulotlar bor. Avval mahsulotlarni o'chiring!",
            "danger"
        )
        return redirect(
            url_for("admin.categories")
        )

    db.session.delete(category)
    db.session.commit()

    flash(
        "Kategoriya o'chirildi",
        "success"
    )

    return redirect(
        url_for("admin.categories")
    )

@admin.route("/orders/payment/<int:id>/<action>")
def payment_action(id, action):

    order = Order.query.get_or_404(id)

    print(
        "ORDER:",
        order.id,
        action
    )

    if action == "approve":
        order.payment_status = "To'langan"
        order.payment_verified = True

    elif action == "cancel":
        order.payment_status = "Bekor qilindi"
        order.payment_verified = False

    db.session.commit()

    print(
        "STATUS:",
        order.payment_status
    )

    flash(
        "To'lov yangilandi",
        "success"
    )

    return redirect(
        url_for("admin.orders")
    )

@admin_bp.route(
"/orders/status/<int:id>/<status>"
)
def order_status(id,status):

    order = Order.query.get_or_404(id)


    if status == "cancel":

        order.status = Order.STATUS_CANCELLED

        order.cancel_reason = (
            "Admin tomonidan bekor qilindi"
        )


    db.session.commit()


    flash(
        "Buyurtma holati o'zgardi",
        "success"
    )


    return redirect(
        url_for(
            "admin.orders"
        )
    )