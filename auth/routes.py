from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash
)

from datetime import datetime

from extensions import db
from models.user import User


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)



# =================================
# REGISTER
# =================================

@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():


    if request.method == "POST":


        name = request.form.get(
            "name"
        )

        phone = request.form.get(
            "phone"
        )

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )



        # EMPTY CHECK

        if not name or not phone or not password:

            flash(
                "Barcha maydonlarni to'ldiring",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )



        # PASSWORD CHECK

        if password != confirm_password:

            flash(
                "Parollar bir xil emas",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )



        # PHONE CHECK

        old_user = User.query.filter_by(
            phone=phone
        ).first()


        if old_user:


            flash(
                "Bu telefon allaqachon ro'yxatdan o'tgan",
                "danger"
            )


            return redirect(
                url_for(
                    "auth.register"
                )
            )



        # CREATE USER

        user = User(

            name=name,

            phone=phone

        )


        user.set_password(
            password
        )



        db.session.add(
            user
        )


        db.session.commit()



        flash(
            "Hisob muvaffaqiyatli yaratildi",
            "success"
        )



        return redirect(
            url_for(
                "auth.login"
            )
        )



    return render_template(
        "auth/register.html"
    )





# =================================
# LOGIN
# =================================

@auth.route(
    "/login",
    methods=["GET","POST"]
)
def login():


    if request.method == "POST":


        phone = request.form.get(
            "phone"
        )


        password = request.form.get(
            "password"
        )



        user = User.query.filter_by(
            phone=phone
        ).first()



        if not user:


            flash(
                "Telefon yoki parol xato",
                "danger"
            )


            return redirect(
                url_for(
                    "auth.login"
                )
            )



        if not user.check_password(
            password
        ):


            flash(
                "Telefon yoki parol xato",
                "danger"
            )


            return redirect(
                url_for(
                    "auth.login"
                )
            )



        if not user.is_active:


            flash(
                "Hisob bloklangan",
                "danger"
            )


            return redirect(
                url_for(
                    "auth.login"
                )
            )



        # SESSION

        session["user_id"] = user.id



        # REMEMBER ME

        if request.form.get(
            "remember"
        ):

            session.permanent = True



        user.last_login = datetime.utcnow()



        db.session.commit()



        flash(
            "Xush kelibsiz!",
            "success"
        )



        return redirect("/")



    return render_template(
        "auth/login.html"
    )





# =================================
# LOGOUT
# =================================

@auth.route(
    "/logout"
)
def logout():


    session.pop(
        "user_id",
        None
    )


    flash(
        "Hisobdan chiqildi",
        "success"
    )


    return redirect(
        url_for(
            "auth.login"
        )
    )