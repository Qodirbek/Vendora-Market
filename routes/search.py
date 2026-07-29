from flask import (
    Blueprint,
    render_template,
    request
)

from models.product import Product


search = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


# =====================================
# SEARCH PAGE
# =====================================

@search.route("/")
def index():

    q = request.args.get(
        "q",
        ""
    ).strip()


    products = []

    if q:

        products = Product.query.filter(
            Product.name.ilike(
                f"%{q}%"
            )
        ).filter_by(
            active=True
        ).all()



    # Agar qidiruv topilmasa
    # tavsiya mahsulotlar
    suggestions = Product.query.filter_by(
        active=True
    ).order_by(
        Product.views.desc()
    ).limit(8).all()



    return render_template(
        "search/index.html",
        products=products,
        suggestions=suggestions,
        q=q
    )