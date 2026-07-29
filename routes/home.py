from pdb import main

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request
)

from models.product import Product
from models.category import Category
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from extensions import db
from flask import request, session, flash
from models.review import Review


home = Blueprint(
    "home",
    __name__
)



@home.route("/")
def index():

    # login tekshirish
    if "user_id" not in session:
        return redirect("/auth/login")



    # qidiruv
    search = request.args.get(
        "q",
        ""
    )



    # kategoriya
    category_id = request.args.get(
        "category"
    )



    products = Product.query



    # Qidiruv
    if search:

        products = products.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )



    # kategoriya filter
    if category_id:

        products = products.filter_by(
            category_id=category_id
        )



    # yangi va mashhur mahsulotlar
    products = products.order_by(
        Product.id.desc()
    ).all()



    # kategoriyalar
    categories = Category.query.all()



    return render_template(

        "home/index.html",

        products=products,

        categories=categories,

        search=search

    )

# =========================
# PRODUCT DETAIL
# =========================

@home.route("/product/<int:id>")
def product_detail(id):
    product = Product.query.get_or_404(id)

    return render_template(
        "product/detail.html",
        product=product
    )


@home.route("/product/<int:id>/review", methods=["POST"])
def add_review(id):

    if "user_id" not in session:
        flash(
            "Sharh yozish uchun tizimga kiring",
            "warning"
        )
        return redirect(
            url_for("auth.login")
        )


    rating = request.form.get(
        "rating"
    )

    text = request.form.get(
        "text"
    )


    review = Review(
        user_id=session["user_id"],
        product_id=id,
        rating=int(rating),
        text=text,
        approved=False
    )


    db.session.add(review)
    db.session.commit()


    flash(
        "Sharhingiz yuborildi. Admin tasdiqlagandan keyin chiqadi ⭐",
        "success"
    )


    return redirect(
        url_for(
            "home.product_detail",
            id=id
        )
    )
