# Products callback

from os import stat
import re
from connect import dp
from aiogram import types
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext

from database.connect import User
from ..conversation import Language, MainMenu, Product, ProductForm
from database import db
from ..keyboards import ru, uz


@dp.callback_query_handler(lambda c: c.data == "OnlineOrder", state=Product.info)
async def OnlineOrd(callback: types.callback_query, state: FSMContext):
    # GetData
    User = callback.from_user
    Lang = db.Lang(User.id)

    msg = callback.message

    if Lang in "ru":
        # Condition Code

        await msg.answer("<b>Заказать онлайн</b>", parse_mode="HTML", reply_markup=ru.ClearKb)
        await msg.answer("Заполните вопросы, и мы подберем подходящий курс!")
        await msg.answer("1. Возраст: (День) (Месяц) (Год)", parse_mode="HTML")

        await ProductForm.age.set()

    elif Lang in "uz":

        await msg.answer("<b>Online buyurtma</b>", parse_mode="HTML", reply_markup=ru.ClearKb)
        await msg.answer("Iltimos quyidagi savollarni to’ldiring va sizga mos keladigan kursni taklif qilamiz!")
        await msg.answer("1. Yosh: (kun) (oy) (yil)")

        await ProductForm.age.set()


@dp.callback_query_handler(lambda c: c.data == "OperatorOrder", state=Product.info)
async def OnlineOrd(callback: types.callback_query, state: FSMContext):
    # get Lang
    User = callback.from_user
    Lang = db.Lang(User.id)

    # Condition

    if Lang in "ru":

        await callback.message.edit_text("Свяжитесь с оператором: +998 (71) 230 33 30", reply_markup=ru.OperatorBackType)

    elif Lang in "uz":

        await callback.message.edit_text("Operator bilan bog'laning: +998 (71) 230 33 30", reply_markup=uz.OperatorBackType)


@dp.callback_query_handler(lambda c: c.data == "OnlineOperatorBack", state=Product.info)
async def OperatorBack(callback: types.callback_query, state: FSMContext):
    # get Lang
    User = callback.from_user
    Lang = db.Lang(User.id)
    if Lang in "ru":

        await callback.message.edit_text("Выберите как вы хотите совершить заказ: ", reply_markup=ru.OrderType)

    elif Lang in "uz":

        await callback.message.edit_text("Qaysi mahsulot haqida ma’lumot olmoqchisiz?", reply_markup=uz.OrderType)


# Add Contract
@dp.callback_query_handler(lambda c: re.findall(r"^CourseAdd+\d+$", c.data), state=Product.course)
async def Course(callback: types.callback_query, state: FSMContext):
    # get lang
    User = callback.from_user
    Lang = db.Lang(User.id)

    GetId = callback.data.replace("CourseAdd", "")
    Id = int(GetId)

    async with state.proxy() as data:
        data['Course'] = Id
        orderId = data['OrderId']

    if Lang in "ru":

        await callback.message.edit_text(f"Подпишите договор: \n Ордер Айди: {orderId}")

    elif Lang in "uz":

        await callback.message.edit_text("Shartnoma tuzish: ")
