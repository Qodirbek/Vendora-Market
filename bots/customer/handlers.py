from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    WebAppInfo
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app import app
from extensions import db
from models.user import User

from keyboards.customer import phone_keyboard
from config import Config

from .states import RegisterState


router = Router()



# ==========================================
# PHONE CLEAN
# ==========================================

def clean_phone(phone):

    if not phone:
        return None

    phone = (
        phone
        .replace(" ","")
        .replace("-","")
        .replace("(","")
        .replace(")","")
    )

    if not phone.startswith("+"):
        phone = "+" + phone

    return phone



# ==========================================
# WEB APP
# ==========================================

def website_button(tg_id):

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="🌐 Vendora Market",
        web_app=WebAppInfo(
            url=(
                f"{Config.SITE_URL}"
                f"/auth/telegram/auth?id={tg_id}"
            )
        )
    )

    keyboard.adjust(1)

    return keyboard.as_markup()



# ==========================================
# START
# ==========================================

@router.message(CommandStart())
async def start(message:Message):

    tg_id=str(
        message.from_user.id
    )


    print(
        "START TG:",
        tg_id
    )


    with app.app_context():

        user=User.query.filter_by(
            tg_id=tg_id
        ).first()


        if user and user.phone:

            await message.answer(
                "👋 Xush kelibsiz!\n\n"
                "Vendora Market:",
                reply_markup=website_button(
                    tg_id
                )
            )

            return



    await message.answer(
        "Assalomu alaykum 👋\n\n"
        "Vendora Market uchun telefon raqamingizni yuboring 📱",
        reply_markup=phone_keyboard()
    )



# ==========================================
# CONTACT
# ==========================================

@router.message(F.contact)
async def save_phone(
    message:Message,
    state:FSMContext
):

    contact=message.contact


    if contact.user_id != message.from_user.id:

        await message.answer(
            "❌ Faqat o'z raqamingizni yuboring"
        )

        return



    phone=clean_phone(
        contact.phone_number
    )


    tg_id=str(
        message.from_user.id
    )


    print(
        "PHONE:",
        phone
    )


    with app.app_context():


        user=User.query.filter_by(
            phone=phone
        ).first()



        # mavjud user

        if user:


            print(
                "USER TOPILDI:",
                user.id
            )


            if user.tg_id and user.tg_id != tg_id:

                await message.answer(
                    "❌ Bu raqam boshqa Telegramga ulangan"
                )

                return



            user.tg_id=tg_id
            user.tg_username=message.from_user.username
            user.tg_first_name=message.from_user.first_name
            user.telegram_verified=True


            db.session.commit()



        # yangi user

        else:


            print(
                "YANGI USER"
            )


            await state.update_data(
                phone=phone,
                tg_id=tg_id
            )


            await message.answer(
                "🔐 Yangi akkaunt yaratamiz\n\n"
                "Saytga kirish uchun parol yarating:"
            )


            await state.set_state(
                RegisterState.waiting_password
            )

            return



    await message.answer(
        "✅ Telegram ulandi\n\n"
        "Kirish:",
        reply_markup=website_button(
            tg_id
        )
    )



# ==========================================
# PASSWORD CREATE
# ==========================================


@router.message(
    RegisterState.waiting_password
)
async def create_password(
    message:Message,
    state:FSMContext
):

    password=message.text


    if len(password)<6:

        await message.answer(
            "❌ Parol kamida 6 ta belgi bo'lsin"
        )

        return



    data=await state.get_data()


    phone=data["phone"]
    tg_id=data["tg_id"]



    with app.app_context():

        user=User(

            name=message.from_user.full_name,

            phone=phone,

            tg_id=tg_id,

            tg_username=message.from_user.username,

            tg_first_name=message.from_user.first_name,

            role="user",

            is_active=True,

            telegram_verified=True

        )


        user.set_password(
            password
        )


        db.session.add(user)

        db.session.commit()



        print(
            "NEW USER:",
            user.id,
            user.phone
        )


    await state.clear()



    await message.answer(
        "✅ Akkaunt yaratildi\n\n"
        "Vendora Market:",
        reply_markup=website_button(
            tg_id
        )
    )



# ==========================================
# PROFILE
# ==========================================

@router.callback_query(
    F.data=="profile"
)
async def profile(call:CallbackQuery):

    tg_id=str(
        call.from_user.id
    )


    with app.app_context():

        user=User.query.filter_by(
            tg_id=tg_id
        ).first()


        if not user:

            await call.message.answer(
                "Profil topilmadi"
            )

            return



        text=(
            "👤 Profil\n\n"
            f"📝 {user.name}\n"
            f"📱 {user.phone}\n"
            f"Telegram ID: {user.tg_id}"
        )


    await call.message.answer(text)



# ==========================================
# OTHER BUTTONS
# ==========================================


@router.callback_query(F.data=="cart")
async def cart(call):

    await call.message.answer(
        "🛒 Savat"
    )



@router.callback_query(F.data=="orders")
async def orders(call):

    await call.message.answer(
        "📦 Buyurtmalar"
    )



@router.callback_query(F.data=="favorites")
async def favorites(call):

    await call.message.answer(
        "❤️ Sevimlilar"
    )



@router.callback_query(F.data=="support")
async def support(call):

    await call.message.answer(
        "💬 @VendoraSupport"
    )