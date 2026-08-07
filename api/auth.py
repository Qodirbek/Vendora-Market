from . import api

from flask import (
    request,
    jsonify
)

from models import User

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



# =========================
# REGISTER
# =========================

@api.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()


    if not data:

        return jsonify({

            "success":False,

            "message":"Ma'lumot kelmadi"

        }),400



    name = data.get("name")
    phone = data.get("phone")
    password = data.get("password")



    if not name or not phone or not password:

        return jsonify({

            "success":False,

            "message":
            "Barcha maydonlarni to'ldiring"

        }),400



    old_user = User.query.filter_by(
        phone=phone
    ).first()



    if old_user:

        return jsonify({

            "success":False,

            "message":
            "Bu telefon raqam mavjud"

        }),400




    user = User(

        name=name,

        phone=phone,

        password=
        generate_password_hash(password)

    )



    from app import db

    db.session.add(user)

    db.session.commit()



    return jsonify({

        "success":True,

        "message":
        "Ro'yxatdan o'tildi",

        "user":{

            "id":user.id,

            "name":user.name,

            "phone":user.phone

        }

    })






# =========================
# LOGIN
# =========================


@api.route(
    "/login",
    methods=["POST"]
)
def login():


    data=request.get_json()



    phone=data.get("phone")

    password=data.get("password")



    user=User.query.filter_by(
        phone=phone
    ).first()



    if not user:


        return jsonify({

            "success":False,

            "message":
            "Foydalanuvchi topilmadi"

        }),404




    if not check_password_hash(
        user.password,
        password
    ):


        return jsonify({

            "success":False,

            "message":
            "Parol noto'g'ri"

        }),401




    return jsonify({

        "success":True,

        "message":
        "Kirish muvaffaqiyatli",


        "user":{

            "id":user.id,

            "name":user.name,

            "phone":user.phone

        }

    })





# =========================
# USER PROFILE
# =========================


@api.route(
    "/user/<int:id>",
    methods=["GET"]
)
def profile(id):


    user=User.query.get_or_404(id)



    return jsonify({

        "success":True,

        "user":{

            "id":user.id,

            "name":user.name,

            "phone":user.phone

        }

    })