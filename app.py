from flask import (
    Flask,
    session,
    render_template
)

from config import Config
from extensions import db, login_manager

import subprocess

import threading


# =====================================
# APPLICATION FACTORY
# =====================================

def create_app():

    app = Flask(__name__)


    # =====================================
    # CONFIG
    # =====================================

    app.config.from_object(Config)


    # =====================================
    # EXTENSIONS
    # =====================================

    login_manager.init_app(app)
    db.init_app(app)


    # =====================================
    # MODELS
    # =====================================

    from models.user import User
    from models.profile import Profile
    from models.category import Category
    from models.product import Product
    from models.cart import Cart
    from models.favorite import Favorite
    from models.order import Order
    from models.order_item import OrderItem
    from models.seller import Seller
    from models.review import Review
    from models.notification import Notification
    from models.withdraw_request import WithdrawRequest


    # =====================================
    # BLUEPRINTS
    # =====================================

    from routes.home import home
    from routes.cart import cart
    from routes.profile import profile
    from routes.favorite import favorite
    from routes.search import search
    from routes.order import order_bp

    from auth.routes import auth

    from seller.routes import seller
    from seller.import_routes import seller_import
    from seller.template_routes import template

    from routes.excel import excel

    from admin.routes import admin
    from admin.categories import category_admin
    from admin.excel import excel_admin
    from admin.products_excel import product_excel_admin


    # =====================================
    # REGISTER
    # =====================================

    app.register_blueprint(home)
    app.register_blueprint(cart)
    app.register_blueprint(profile)
    app.register_blueprint(favorite)
    app.register_blueprint(search)

    app.register_blueprint(auth)

    app.register_blueprint(seller)
    app.register_blueprint(seller_import)
    app.register_blueprint(template)

    app.register_blueprint(excel)

    app.register_blueprint(admin)
    app.register_blueprint(category_admin)
    app.register_blueprint(excel_admin)
    app.register_blueprint(product_excel_admin)

    app.register_blueprint(order_bp)



    # =====================================
    # GLOBAL VARIABLES
    # =====================================

    @app.context_processor
    def global_variables():

        cart_count = 0

        if "user_id" in session:

            cart_count = Cart.query.filter_by(
                user_id=session["user_id"]
            ).count()


        return {
            "site_name":
                "Sotuv Platform",

            "cart_count":
                cart_count
        }



    # =====================================
    # ERRORS
    # =====================================

    @app.errorhandler(404)
    def not_found(error):

        return render_template(
            "errors/404.html"
        ),404



    @app.errorhandler(500)
    def internal_error(error):

        db.session.rollback()

        return render_template(
            "errors/500.html"
        ),500



    # =====================================
    # SESSION CLEAR
    # =====================================

    @app.route("/clear-session")
    def clear_session():

        session.clear()

        return """
        <h2>Session tozalandi ✅</h2>
        <a href="/auth/login">
        Login qilish
        </a>
        """



    # =====================================
    # DATABASE
    # =====================================

    with app.app_context():

        db.create_all()

        print(
            "✅ DATABASE tayyor"
        )



    # =====================================
    # STATUS
    # =====================================

    @app.route("/status")
    def status():

        return {

            "app":
            "Sotuv Platform",

            "version":
            "1.0.0",

            "status":
            "running"
        }



    print("REGISTERED ROUTES:")

    for rule in app.url_map.iter_rules():

        print(rule)



    return app



# =====================================
# START APP
# =====================================


app = create_app()



# =====================================
# START TELEGRAM BOT
# =====================================
def start_bot_thread():
    try:
        from bots.customer.bot import run_bot

        thread = threading.Thread(
            target=run_bot,
            daemon=True
        )

        thread.start()

        print(
            "🤖 Telegram bot thread ishga tushdi"
        )

    except Exception as e:
        print(
            "BOT START XATO:",
            e
        )

start_bot_thread()


# =====================================
# RUN LOCAL
# =====================================
def run_bot():
    subprocess.call(
        ["python", "bots/customer/bot.py"]
    )

threading.Thread(
    target=run_bot,
    daemon=True
).start()



# =====================================
# RUN LOCAL
# =====================================

if __name__ == "__main__":

    print(
"""
================================
🚀 SOTUV PLATFORM ISHGA TUSHDI

🌐 Website:
http://127.0.0.1:5000

🤖 Telegram:
Vendora Customer Bot

================================
"""
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )