import re

from aiogram.types import reply_keyboard
from connect import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from database.models import Courses
from .conversation import *
from database import db

# Keyboards
from .keyboards import uz, ru


# Product Main
@dp.callback_query_handler(lambda c: re.findall(r"id[\w]*", c.data), state=Product.info)
async def Main(callback: types.callback_query, state: FSMContext):
    # Code
    User = callback.from_user
    Lang = db.Lang(User.id)

    # Get Product Id
    GetId = callback.data.replace("id", "")
    Id = int(GetId)

    # Get Product

    GetProduct = db.getProduct(product_id=Id)

    async with state.proxy() as data:
        data['OrderId'] = Id

    # Fully form condition

    # Language condition
    if Lang in "ru":

        markup = types.ReplyKeyboardMarkup()

        markup.clean()
        markup.add("Заказать")
        markup.add("Назад")

        await callback.message.answer(f"<b>{GetProduct.name}</b>\n{GetProduct.description}", parse_mode="HTML")
        await callback.message.answer(GetProduct.link, parse_mode="HTML", reply_markup=markup)

    elif Lang in "uz":

        markup = types.ReplyKeyboardMarkup()

        markup.clean()
        markup.add("Buyurtma berish")
        markup.add("Ortga")

        await callback.message.answer(f"<b>{GetProduct.uzname}</b>\n{GetProduct.uzdescription}", parse_mode="HTML")
        await callback.message.answer(GetProduct.link, reply_markup=markup, parse_mode="HTML")


@dp.message_handler(lambda msg: msg.text in ['Заказать', 'Buyurtma berish'], state=Product.info)
async def order(msg: types.message, state: FSMContext):
    # get user and language
    User = msg.from_user
    Lang = db.Lang(User.id)

    # code
    if Lang in "ru":

        await msg.answer("Выберите как вы хотите совершить заказ: ", reply_markup=ru.OrderType)

    elif Lang in "uz":

        await msg.answer("Выберите как вы хотите совершить заказ: ", reply_markup=uz.OrderType)


@dp.message_handler(state=Product.height)
async def height(msg: types.message, state: FSMContext):
    # Get user and language library
    User = msg.from_user
    Lang = db.Lang(User.id)

    async with state.proxy() as data:
        data['OrderHeight'] = msg.text

    # code
    if Lang in "ru":

        await msg.answer("Вес: ")

    elif Lang in "uz":

        await msg.answer("Vazn: ")

    await Product.next()


@dp.message_handler(state=Product.weight)
async def weight(msg: types.message, state: FSMContext):
    # Get user and language library
    User = msg.from_user
    Lang = db.Lang(User.id)

    async with state.proxy() as data:
        data['OrderWeight'] = msg.text

    # code
    if Lang in "ru":

        await msg.answer("Сколько кг вы хотите похудеть: ", reply_markup=ru.CourseReplyBtn)

    elif Lang in "uz":

        await msg.answer("Nechchi kg ozmoqchisiz?: ", uz.CourseReplyBtn)

    await Product.next()


@dp.message_handler(state=Product.course)
async def RecommendCourse(msg: types.message, state: FSMContext):
    # Get user and language library
    User = msg.from_user
    Lang = db.Lang(User.id)
    Check = db.CourseExists(msg.text)

    if Lang in "ru":

        Answer = "В {name} входит: "
        Error = "Введена не верная операция! Выберите с клавиатуры!"

    elif Lang in "uz":

        Answer = "{name} o’z ichiga quyidagilarnio oladi: "
        Error = "Klaviaturadan tugmani bosing!"

    if(Check):
        Course = db.getCourse(msg.text)

        if Lang in "ru":

            Cours = await ru.AddContract(Course.id)
            await msg.answer(Answer.format(name=Course.title) + f"\n {Course.description}", reply_markup=Cours)

        elif Lang in "uz":

            Cours = await uz.AddContract(Course.id)
            await msg.answer(Answer.format(name=Course.uztitle) + f"\n {Course.uzdescription}", reply_markup=Cours)

    else:
        await msg.answer(Error)
