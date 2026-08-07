from . import api

from flask import jsonify

from models import Category


# ==========================
# ALL CATEGORIES
# ==========================

@api.route(
    "/categories",
    methods=["GET"]
)
def get_categories():

    categories = Category.query.all()

    data=[]


    for c in categories:

        data.append({

            "id": c.id,

            "name": c.name,

            "image": getattr(
                c,
                "image",
                None
            )

        })


    return jsonify({

        "success":True,

        "categories":data

    })