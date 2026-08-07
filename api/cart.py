from . import api

from flask import (
    request,
    jsonify
)

from models import (
    Cart,
    Product
)

from extensions import db



# ==========================
# ADD CART
# ==========================

@api.route(
    "/cart/add",
    methods=["POST"]
)
def add_cart():

    data = request.json


    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get(
        "quantity",
        1
    )


    product = Product.query.get(product_id)


    if not product:

        return jsonify({

            "success":False,

            "message":
            "Mahsulot topilmadi"

        })



    old_cart = Cart.query.filter_by(

        user_id=user_id,

        product_id=product_id

    ).first()



    if old_cart:

        old_cart.quantity += quantity


    else:

        cart = Cart(

            user_id=user_id,

            product_id=product_id,

            quantity=quantity

        )

        db.session.add(cart)



    db.session.commit()



    return jsonify({

        "success":True,

        "message":
        "Savat yangilandi"

    })





# ==========================
# GET CART
# ==========================

@api.route(
    "/cart/<int:user_id>",
    methods=["GET"]
)
def get_cart(user_id):


    carts = Cart.query.filter_by(

        user_id=user_id

    ).all()



    items=[]

    total=0



    for c in carts:


        product = Product.query.get(
            c.product_id
        )


        if product:


            price = product.price * c.quantity


            total += price


            items.append({

                "cart_id":c.id,

                "product_id":
                product.id,


                "name":
                product.name,


                "image":
                product.image,


                "price":
                product.price,


                "quantity":
                c.quantity,


                "subtotal":
                price

            })



    return jsonify({

        "success":True,

        "items":items,

        "total":total

    })





# ==========================
# REMOVE CART
# ==========================

@api.route(
    "/cart/remove/<int:id>",
    methods=["DELETE"]
)
def remove_cart(id):


    cart = Cart.query.get(id)


    if not cart:

        return jsonify({

            "success":False,

            "message":
            "Savat topilmadi"

        })



    db.session.delete(cart)

    db.session.commit()



    return jsonify({

        "success":True,

        "message":
        "O'chirildi"

    })