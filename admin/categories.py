from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db
from models.category import Category


category_admin = Blueprint(
    "category_admin",
    __name__,
    url_prefix="/admin/categories"
)


# =========================
# CATEGORY LIST
# =========================
@category_admin.route("/")
def categories():

    categories = Category.query.all()

    return render_template(
        "admin/categories.html",
        categories=categories
    )


# =========================
# ADD CATEGORY
# =========================
@category_admin.route(
    "/add",
    methods=["POST"]
)
def add_category():

    name = request.form.get("name")
    icon = request.form.get("icon")


    if not name:
        flash(
            "Kategoriya nomi bo'sh bo'lmasin",
            "danger"
        )

        return redirect(
            url_for(
                "category_admin.categories"
            )
        )


    category = Category(
        name=name,
        icon=icon
    )


    db.session.add(category)
    db.session.commit()


    flash(
        "Kategoriya yaratildi",
        "success"
    )


    return redirect(
        url_for(
            "category_admin.categories"
        )
    )

# =========================
# DELETE CATEGORY
# =========================
@category_admin.route(
    "/delete/<int:id>"
)
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()


    flash(
        "Kategoriya o'chirildi",
        "success"
    )


    return redirect(
        url_for(
            "category_admin.categories"
        )
    )