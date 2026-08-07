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
from flask import current_app
import time

from extensions import db
from models.user import User
from flask import request, redirect, url_for, flash, session, render_template
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)



# =================================
# PHONE CLEAN
# =================================

def clean_phone(phone):
    if not phone:
        return None

    phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace("+", "")
    )

    return phone



# =================================
# REGISTER
# =================================

# =================================
# REGISTER
# =================================

@auth.route(
    "/register",
    methods=["GET","POST"]
)
def register():

    if request.method == "POST":

        print("\n======================")
        print("REGISTER ISHLADI")
        print("======================")


        name = request.form.get(
            "name"
        )

        raw_phone = request.form.get(
            "phone"
        )

        country_code = request.form.get(
            "country_code"
        )


        print(
            "NAME:",
            name
        )

        print(
            "RAW PHONE:",
            raw_phone
        )

        print(
            "COUNTRY:",
            country_code
        )


        # PHONE TOZALASH
        phone = clean_phone(
            raw_phone
        )


        # COUNTRY CODE TOZALASH
        if country_code:

            country_code = (
                country_code
                .replace("+", "")
                .replace("🇺🇿", "")
                .replace("🇰🇬", "")
                .replace("🇷🇺", "")
                .replace("🇺🇸", "")
                .replace("🇹🇷", "")
                .replace("🇩🇪", "")
                .replace("🇬🇧", "")
                .replace("🇨🇳", "")
                .replace("🇰🇿", "")
                .strip()
            )


            phone = (
                "+"
                +
                country_code
                +
                phone
            )


        print(
            "FINAL PHONE:",
            phone
        )
    

        password = request.form.get(
            "password"
        )

        confirm = request.form.get(
            "confirm_password"
        )


        print(
            "PASSWORD:",
            "BOR" if password else "YO'Q"
        )


        # TEKSHIRISH

        if not all([
            name,
            phone,
            password
        ]):

            print(
                "XATO: MAYDONLAR BO'SH"
            )

            flash(
                "Barcha maydonlarni to'ldiring",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )



        if password != confirm:

            print(
                "XATO: PASSWORD MOS EMAS"
            )

            flash(
                "Parollar mos emas",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )



        # TELEFON BORLIGINI TEKSHIRISH

        exists = User.query.filter_by(
            phone=phone
        ).first()


        print(
            "EXIST USER:",
            exists
        )


        if exists:

            flash(
                "Bu telefon raqam mavjud",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )



        # YANGI USER

        user = User(
            name=name,
            phone=phone,
            role="user",
            is_active=True,
            telegram_verified=False
        )


        user.set_password(
            password
        )


        db.session.add(
            user
        )

        db.session.commit()



        print("======================")
        print("REGISTER SUCCESS ✅")
        print(
            "USER ID:",
            user.id
        )
        print(
            "PHONE:",
            user.phone
        )
        print("======================")



        flash(
            "Hisob yaratildi",
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

        raw_phone = request.form.get("phone")

        country_code = request.form.get(
            "country_code"
        )


        print("======================")
        print("RAW PHONE:", raw_phone)
        print("COUNTRY:", country_code)


        phone = clean_phone(
            raw_phone
        )
        
        
        if country_code:
        
            country_code = (
                country_code
                .replace("+","")
                .replace("🇺🇿","")
                .replace("🇰🇬","")
                .replace("🇷🇺","")
                .replace("🇺🇸","")
                .replace("🇹🇷","")
                .replace("🇩🇪","")
                .replace("🇬🇧","")
                .replace("🇨🇳","")
                .replace("🇰🇿","")
                .strip()
            )
        
        
            phone = (
                "+"
                +
                country_code
                +
                phone
            )


        print(
            "FINAL PHONE:",
            phone
        )


        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            phone=phone
        ).first()


        print(
            "USER TOPILDI:",
            user
        )


        if user:

            print(
                "PASSWORD CHECK:",
                user.check_password(password)
            )


        if (
            not user
            or not user.check_password(password)
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


        if user.is_blocked:

            flash(
                "Hisob bloklangan",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.login"
                )
            )


        session["user_id"] = user.id
        session["role"] = user.role


        user.last_login = datetime.utcnow()
        user.last_ip = request.remote_addr


        db.session.commit()


        print("======================")
        print("LOGIN SUCCESS")
        print(
            "USER:",
            user.id
        )
        print(
            "PHONE:",
            user.phone
        )
        print("======================")


        flash(
            "Xush kelibsiz!",
            "success"
        )


        return redirect("/")


    return render_template(
        "auth/login.html"
    )



# ==================================
# TELEGRAM LOGIN START
# ==================================

@auth.route("/telegram")
def telegram_login():

    return redirect(
        "https://t.me/Vendora_Marketbot?start=auth"
    )



# ==================================
# TELEGRAM AUTH PAGE
# ==================================

@auth.route("/telegram/auth")
def telegram_auth():

    print("===================")
    print("TELEGRAM AUTH")
    print("===================")


    tg_id = request.args.get("id")


    if not tg_id:

        return redirect(
            url_for(
                "auth.telegram_login"
            )
        )



    session["tg_id"] = str(tg_id)


    user = User.query.filter_by(
        tg_id=str(tg_id)
    ).first()



    print(
        "USER:",
        user
    )



    if not user:

        return redirect(
            url_for(
                "auth.telegram_wait_phone"
            )
        )



    return render_template(
        "auth/telegram_auth.html",
        user=user
    )




# ==================================
# TELEGRAM CONTACT KELGANDAN KEYIN
# ==================================

@auth.route(
    "/telegram/phone",
    methods=["POST"]
)
def telegram_phone():

    print("\n==========================")
    print("TELEGRAM PHONE START")
    print("==========================")


    phone = clean_phone(
        request.form.get("phone")
    )

    print(
        "PHONE:",
        phone
    )


    tg_id = session.get(
        "tg_id"
    )


    print(
        "TG_ID:",
        tg_id
    )


    if not tg_id:
        flash(
            "Telegram sessiya tugagan",
            "danger"
        )
        return redirect("/")



    user = User.query.filter_by(
        phone=phone
    ).first()


    print(
        "USER:",
        user
    )



    if not user:

        print(
            "USER TOPILMADI"
        )

        flash(
            "Bu telefon bilan Vendora akkaunti yo'q",
            "danger"
        )

        return redirect("/")



    # boshqa telegramga ulanganmi

    if user.tg_id and user.tg_id != str(tg_id):

        print(
            "BOSHQA TG ULANGAN"
        )

        flash(
            "Bu akkaunt boshqa Telegramga ulangan",
            "danger"
        )

        return redirect("/")



    # TELEGRAM ULASH


    user.tg_id = str(tg_id)

    user.tg_username = session.get(
        "tg_username"
    )

    user.tg_first_name = session.get(
        "tg_name"
    )

    user.tg_photo = session.get(
        "tg_photo"
    )

    user.telegram_verified = True


    db.session.commit()



    print("==========================")
    print("TELEGRAM ULANDI")
    print(
        "USER:",
        user.id
    )
    print(
        "PHONE:",
        user.phone
    )
    print(
        "TG:",
        user.tg_id
    )
    print("==========================")


    return redirect(
        url_for(
            "auth.telegram_auth",
            id=tg_id
        )
    )




# ==================================
# TELEGRAM PASSWORD LOGIN
# ==================================

@auth.route(
    "/telegram/connect",
    methods=["POST"]
)
def telegram_connect():

    print("\n==============================")
    print("🔐 TELEGRAM CONNECT ISHLADI")
    print("==============================")

    print("==============================")
    print("KELGAN PASSWORD:", repr(password))
    print("UZUNLIK:", len(password) if password else 0)
    print("==============================")

    # SESSIONDAN TG ID
    tg_id = session.get("tg_id")

    print(
        "SESSION TG_ID:",
        tg_id
    )


    # FORM PASSWORD
    password = request.form.get(
        "password"
    )


    print(
        "PASSWORD KELDI:",
        "HA" if password else "YO'Q"
    )


    # TG ID YO'Q
    if not tg_id:

        print(
            "❌ TG_ID SESSIONDA YO'Q"
        )

        flash(
            "Telegram sessiya tugagan. Qaytadan kiring.",
            "danger"
        )

        return redirect(
            url_for(
                "auth.telegram_login"
            )
        )



    # PASSWORD YO'Q
    if not password:

        print(
            "❌ PASSWORD BO'SH"
        )

        flash(
            "Parol kiriting",
            "danger"
        )

        return redirect(
            request.referrer
        )



    # USER TOPISH

    print(
        "USER QIDIRILYAPTI:",
        tg_id
    )


    user = User.query.filter_by(
        tg_id=str(tg_id)
    ).first()



    print(
        "USER:",
        user
    )


    if not user:

        print(
            "❌ TG USER TOPILMADI"
        )

        flash(
            "Telegram hisob topilmadi",
            "danger"
        )

        return redirect("/")



    print("==============================")
    print("USER MALUMOT")
    print(
        "ID:",
        user.id
    )
    print(
        "PHONE:",
        user.phone
    )
    print(
        "TG:",
        user.tg_id
    )
    print(
        "PASSWORD HASH:",
        bool(user.password)
    )
    print("==============================")



    # USERDA PASSWORD BORMI

    if not user.password:

        print(
            "❌ USERDA PASSWORD YO'Q"
        )

        flash(
            "Bu akkauntda parol mavjud emas. Avval saytdan ro'yxatdan o'ting.",
            "danger"
        )

        return redirect(
            request.referrer
        )



    # PASSWORD TEKSHIRISH

    try:

        check = user.check_password(
            password
        )

        print(
            "PASSWORD CHECK:",
            check
        )


    except Exception as e:

        print(
            "PASSWORD ERROR:",
            e
        )

        flash(
            "Parol tekshirish xatosi",
            "danger"
        )

        return redirect(
            request.referrer
        )



    if not check:

        print(
            "❌ PAROL XATO"
        )

        flash(
            "Parol noto'g'ri",
            "danger"
        )

        return redirect(
            request.referrer
        )



    # LOGIN

    session["user_id"] = user.id
    session["role"] = user.role


    user.last_login = datetime.utcnow()
    user.last_ip = request.remote_addr


    db.session.commit()



    print("==============================")
    print("✅ LOGIN MUVAFFAQIYATLI")
    print(
        "USER ID:",
        user.id
    )
    print(
        "PHONE:",
        user.phone
    )
    print(
        "TG ID:",
        user.tg_id
    )
    print("==============================\n")



    flash(
        "Xush kelibsiz!",
        "success"
    )


    return redirect("/")





# ==================================
# WAIT PHONE PAGE
# ==================================

@auth.route("/telegram/wait-phone")
def telegram_wait_phone():

    return render_template(
        "auth/telegram_phone.html"
    )





# ==================================
# FORGOT PASSWORD
# ==================================

@auth.route("/forgot-password")
def forgot_password():

    return render_template(
        "auth/forgot_password.html"
    )


# =================================
# LOGOUT
# =================================

@auth.route("/logout")
def logout():

    session.clear()


    flash(
        "Hisobdan chiqildi",
        "success"
    )


    return redirect(
        url_for(
            "auth.login"
        )
    )

# GOOGLE LOGIN CALLBACK MARSHRUTI
@auth.route('/google-login-callback', methods=['POST'])
def google_login_callback():
    id_token = request.form.get('firebase_id_token')
    
    if not id_token:
        flash("Google avtorizatsiya kaliti topilmadi!", "danger")
        return redirect(url_for('auth.login'))

    try:
        # Vaqt tafovuti bo'lsa 1 soniya kutib qayta tekshiramiz
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception as token_err:
            if "Token used too early" in str(token_err):
                time.sleep(1.5)  # 1.5 soniya kutamiz
                decoded_token = firebase_auth.verify_id_token(id_token)
            else:
                raise token_err

        email = decoded_token.get('email')
        name = decoded_token.get('name', 'Google Foydalanuvchisi')
        uid = decoded_token.get('uid')

        # ... qolgan bazaga saqlash kodingiz ...
        # 1. Firebase tokenini tekshirish va ma'lumotlarni olish
        decoded_token = firebase_auth.verify_id_token(id_token)
        
        email = decoded_token.get('email')
        name = decoded_token.get('name', 'Google Foydalanuvchisi')
        uid = decoded_token.get('uid')

        if not email:
            flash("Google hisobingizdan email olinmadi!", "danger")
            return redirect(url_for('auth.login'))

        # 2. Bazadan foydalanuvchini email bo'yicha qidiramiz
        user = User.query.filter_by(email=email).first()

        # 3. Agar foydalanuvchi bazada bo'lmasa, yangi obyekt yaratib bazaga qo'shamiz
        if not user:
            user = User(
                name=name,
                email=email
            )
            
            # Agar User modelingizda parol maydoni majburiy bo'lsa:
            if hasattr(user, 'set_password'):
                user.set_password(f"google_oauth_{uid[:8]}")
            elif hasattr(user, 'password'):
                user.password = f"google_oauth_{uid[:8]}"

            db.session.add(user)
            db.session.commit()
            print(f"✅ Yangi foydalanuvchi bazaga qo'shildi: {email}")

        # 4. Foydalanuvchi bazadagi ID'si bilan sessiyaga saqlanadi
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email

        flash(f"Xush kelibsiz, {user.name}!", "success")
        
        # Profil sahifasiga yo'naltirish
        return redirect(url_for('profile.profile') if 'profile.profile' in current_app.view_functions else '/')

    except Exception as e:
        db.session.rollback()
        print("----------------------------------------")
        print("Google Login / DB Error:", str(e))
        print("----------------------------------------")
        flash(f"Google orqali kirishda xatolik yuz berdi: {str(e)}", "danger")
        return redirect(url_for('auth.login'))

    # Firebase Admin-ni retsipatsiyasiz 1 marta retsipatsiya qilish
    if not firebase_admin._apps:
            # serviceAccountKey.json faylingiz ildiz papkada bo'lishi kerak
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
