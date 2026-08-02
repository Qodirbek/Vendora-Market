from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

from config import Config



# =====================================
# PHONE REQUEST
# =====================================

def phone_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Telefon raqamni yuborish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )



# =====================================
# MAIN MENU
# =====================================

def main_menu(
        is_admin=False
):

    buttons=[

        [
            InlineKeyboardButton(
                text="🛒 Vendora Market",
                web_app=WebAppInfo(
                    url=Config.SITE_URL
                )
            )
        ],


        [
            InlineKeyboardButton(
                text="🛍 Mahsulotlar",
                callback_data="products"
            ),

            InlineKeyboardButton(
                text="🛒 Savat",
                callback_data="cart"
            )
        ],


        [
            InlineKeyboardButton(
                text="📦 Buyurtmalarim",
                callback_data="orders"
            )
        ],


        [
            InlineKeyboardButton(
                text="❤️ Sevimlilar",
                callback_data="favorites"
            )
        ],


        [
            InlineKeyboardButton(
                text="👤 Profil",
                callback_data="profile"
            )
        ],


        [
            InlineKeyboardButton(
                text="💬 Yordam",
                callback_data="support"
            )
        ]

    ]


    if is_admin:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="⚙️ Admin panel",
                    callback_data="admin"
                )
            ]
        )


    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )



# =====================================
# TELEGRAM LOGIN
# =====================================

def telegram_auth_keyboard():


    return InlineKeyboardMarkup(
        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="🔐 Telegram orqali kirish",

                    web_app=WebAppInfo(

                        url=
                        f"{Config.SITE_URL}/auth/telegram"

                    )

                )

            ]

        ]
    )



# =====================================
# PRODUCT
# =====================================

def product_keyboard(
        product_id
):


    return InlineKeyboardMarkup(

        inline_keyboard=[


            [

                InlineKeyboardButton(
                    text="🛒 Savatga qo‘shish",
                    callback_data=
                    f"cart_add_{product_id}"
                )

            ],


            [

                InlineKeyboardButton(
                    text="❤️ Sevimliga",
                    callback_data=
                    f"favorite_{product_id}"
                )

            ],


            [

                InlineKeyboardButton(
                    text="👁 Ko‘rish",
                    callback_data=
                    f"product_{product_id}"
                )

            ],


            [

                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="products"
                )

            ]

        ]

    )



# =====================================
# CART
# =====================================

def cart_keyboard():


    return InlineKeyboardMarkup(

        inline_keyboard=[


            [

                InlineKeyboardButton(
                    text="✅ Buyurtma berish",
                    callback_data="checkout"
                )

            ],


            [

                InlineKeyboardButton(
                    text="🗑 Savatni tozalash",
                    callback_data="clear_cart"
                )

            ],


            [

                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="back"
                )

            ]

        ]

    )



# =====================================
# ORDER CONFIRM
# =====================================

def confirm_keyboard():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="confirm_order"
                ),


                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_order"
                )

            ]

        ]

    )



# =====================================
# PAYMENT
# =====================================

def payment_keyboard():

    return InlineKeyboardMarkup(

        inline_keyboard=[


            [

                InlineKeyboardButton(
                    text="💳 To‘lov qilish",
                    callback_data="payment"
                )

            ],


            [

                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="back"
                )

            ]

        ]

    )



# =====================================
# SUPPORT
# =====================================

def support_keyboard():

    return InlineKeyboardMarkup(

        inline_keyboard=[


            [

                InlineKeyboardButton(
                    text="💬 Operator",
                    url="https://t.me/Vendora_Market_Supportbot"
                )

            ],


            [

                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="back"
                )

            ]

        ]

    )



# =====================================
# PAGINATION
# =====================================

def pagination(
        page,
        total_pages
):

    buttons=[]


    if page > 1:

        buttons.append(

            InlineKeyboardButton(
                text="⬅️",
                callback_data=
                f"page_{page-1}"
            )

        )


    buttons.append(

        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data="none"
        )

    )


    if page < total_pages:

        buttons.append(

            InlineKeyboardButton(
                text="➡️",
                callback_data=
                f"page_{page+1}"
            )

        )


    return InlineKeyboardMarkup(

        inline_keyboard=[
            buttons
        ]

    )