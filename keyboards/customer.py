from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

from config import Config



# Telefon yuborish

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



# Sayt tugmasi

def site_keyboard():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="🛒 Vendora Market",

                    web_app=WebAppInfo(

                        url=Config.SITE_URL

                    )

                )

            ]

        ]

    )