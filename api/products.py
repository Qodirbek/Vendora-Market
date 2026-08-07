from . import api

from flask import (
    jsonify,
    request
)

from models import Product



# ==========================
# ALL PRODUCTS
# ==========================

@api.route(
    "/products",
    methods=["GET"]
)
def get_products():

    page = request.args.get(
        "page",
        1,
        type=int
    )


    search = request.args.get(
        "search",
        ""
    )


    query = Product.query



    # SEARCH

    if search:

        query = query.filter(
            Product.name.contains(search)
        )



    products = query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )



    result=[]



    for p in products.items:


        result.append({

            "id":p.id,

            "name":p.name,

            "price":p.price,

            "image":p.image,

            "description":
            p.description

        })



    return jsonify({

        "success":True,

        "page":page,

        "total":
        products.total,


        "products":
        result

    })






# ==========================
# PRODUCT DETAIL
# ==========================


@api.route(
    "/products/<int:id>",
    methods=["GET"]
)
def product_detail(id):


    product = Product.query.get_or_404(id)



    return jsonify({

        "success":True,


        "product":{

            "id":
            product.id,


            "name":
            product.name,


            "price":
            product.price,


            "image":
            product.image,


            "description":
            product.description

        }

    })