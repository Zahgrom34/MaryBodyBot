# Backward buttons callback

import re
from connect import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ..conversation import Language, MainMenu, Product
from database import db
from ..keyboards import ru, uz


@dp.message_handler(lambda msg: msg.text in ["Назад", "Ortga"], state=MainMenu.register)
async def BackWardMain(msg: types.message, state: FSMContext):
    # Get Lang

    User = msg.from_user
    Lang = db.Lang(User.id)

    current_state = await state.get_state()

    await msg.answer("Возвращаем вас в главное меню...")
    # Back
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if Lang in "ru":

        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Продукты"

        else:

            main = "Регистрация"

        markup2.add(main, "Сменить язык")
        markup2.add("О боте", "Статус заказа")
        await msg.answer('Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                         reply_markup=markup2)

    elif Lang in "uz":

        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Mahsulotlar"

        else:

            main = "Ro'yhatdan o'tish"

        markup2.add(main, "Tilni o'zgartirish")
        markup2.add("Bot haqida", "Buyurtma statusi")
        await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                         reply_markup=markup2)

    await state.finish()
    await MainMenu.main.set()


@dp.message_handler(lambda msg: msg.text in ["Назад", "Ortga"], state=Product.info)
async def BackToHome(msg: types.message, state: FSMContext):
    User = msg.from_user
    Lang = db.Lang(User.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if Lang in "ru":
        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Продукты"

        else:

            main = "Регистрация"

        markup.add(main, "Сменить язык")
        markup.add("О боте", "Статус заказа")
        await msg.answer("Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:", reply_markup=markup)

    elif Lang in "uz":
        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Mahsulotlar"

        else:

            main = "Ro'yhatdan o'tish"

        markup.add(main, "Tilni o’zgartirish")
        markup.add("Bot haqida", "Buyurtma statusi")
        await msg.answer("Assosy menyudan keyingi amalni tanlang!", reply_markup=markup)

    await state.finish()
    await MainMenu.main.set()


# TODO: Make multi-language backward production state
# TODO: Fix register Backward callback
