from os import stat
import re
from connect import dp
from aiogram import types
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from .conversation import *
from database import db

# Keyboards
from .keyboards import uz, ru


@dp.message_handler(state=ProductForm.age)
async def AgeProccess(msg: types.message, state: FSMContext):
    # Get User library
    User = msg.from_user
    Lang = db.Lang(User.id)

    async with state.proxy() as data:
        data["FormAge"] = msg.text

    # Coditions
    if(Lang in "ru"):

        await msg.answer("2. Пол: ", reply_markup=ru.GenderKeyboard)

    elif (Lang in "uz"):

        await msg.answer("2. Jinsi: ", reply_markup=uz.GenderKeyboard)

    await ProductForm.next()


@dp.message_handler(lambda msg: msg.text not in ["🤵 мужской", "👩‍🦰 женский", "🤵 erkak", "👩‍🦰 ayol"], state=ProductForm.gender)
async def GenderProccess(msg: types.message, state: FSMContext):
    # Get User library
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Coditions
    if Lang in "ru":

        await msg.answer("Укажите пол из клавиатуры!")

    elif Lang in "uz":

        await msg.answer("Klaviaturadan jinsni belgilang!")


@dp.message_handler(state=ProductForm.gender)
async def GenderAcceptProccess(msg: types.message, state: FSMContext):
    # Get User library
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Coditions
    if Lang in "ru":

        answerText = "3: Есть ли у вас какие-либо из следующих состояний или заболеваний?"
        Markup = ru.IllMarkup

    elif Lang in "uz":

        answerText = "3: Quyidagi holatlardamisz yoki kasalliklar bilan og’riganmisz"
        Markup = uz.IllMarkup

    # Verification
    async with state.proxy() as data:
        data["FormGender"] = msg.text

    await msg.answer(answerText, reply_markup=Markup)

    await ProductForm.next()


@dp.message_handler(lambda msg: msg.text not in ["Для женщин", "Прием лекарств от депрессии", "Ayollar uchun", "Depressiya uchun dori ichmoqda"], state=ProductForm.group)
async def GroupProccess(msg: types.message, state: FSMContext):
    # Get User library
    User = msg.from_user
    Lang = db.Lang(User.id)

    if Lang in "ru":

        await msg.answer("Выберите вариант с клавиатуры!")

    elif Lang in "uz":

        await msg.answer("Klaviaturadan variantni tanlang!")


@dp.message_handler(state=ProductForm.group)
async def GroupControllerProccess(msg: types.message, state: FSMContext):
    # Get User library
    User = msg.from_user
    Lang = db.Lang(User.id)

    if Lang in "ru":

        Inline = await ru.Ill(msg=msg, state=[], data=state, variant=msg.text)
        await msg.answer(f"Раздел <b>{msg.text}</b>", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(f"<i>Доступны один или несколько вариантов.</i>", reply_markup=Inline, parse_mode="HTML")

    elif Lang in "uz":

        Inline = await uz.Ill(msg=msg, state=[], data=state, variant=msg.text)
        await msg.answer(f"Раздел <b>{msg.text}</b>", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer(f"<i>Bir yoki bir nechta variantlarni belgilashingiz mumkin.</i>", reply_markup=Inline, parse_mode="HTML")

    await ProductForm.next()


# Callback
@dp.callback_query_handler(lambda c: re.findall(r"^Btn+\d+$", c.data), state=ProductForm.LastStep)
async def GroupCallbackProccess(callback: types.callback_query, state: FSMContext):
    # Get User library
    User = callback.from_user
    Lang = db.Lang(User.id)

    msg = callback.message

    GetId = callback.data.replace("Btn", "")
    Id = int(GetId)

    if Lang in "ru":

        Inline = await ru.IllChange(msg=msg, data=state, variant=Id)
        await msg.edit_text(f"Выбрано ({len(ru.state)})", reply_markup=Inline)

    elif Lang in "uz":

        Inline = await uz.IllChange(msg=msg, data=state, variant=Id)
        await msg.edit_text(f"Tanlangan ({len(uz.state)})", reply_markup=Inline)


@dp.callback_query_handler(lambda c: c.data == "SkipBtn", state=ProductForm.LastStep)
async def SkipProccess(callback: types.callback_query, state: FSMContext):
    # Get User library
    User = callback.from_user
    Lang = db.Lang(User.id)

    msg = callback.message
    ru.state = []
    if Lang in "ru":

        await msg.edit_text(f"Укажите свой рост: ", parse_mode="HTML")

    elif Lang in "uz":

        await msg.edit_text(f"Bo’y: ", parse_mode="HTML")

    await Product.height.set()


@dp.callback_query_handler(lambda c: c.data == "Proceed", state=ProductForm.LastStep)
async def ProceedProccess(callback: types.callback_query, state: FSMContext):
    # Get User library
    User = callback.from_user
    Lang = db.Lang(User.id)

    msg = callback.message
    lists = ""
    if Lang in "ru":
        for list in ru.state:
            txt = db.GetButtonsById(list)
            lists = lists + f"\n <i>- {txt.name}</i>"

        await msg.edit_text(f"\nВы выбрали: {lists}", parse_mode="HTML")

    elif Lang in "uz":
        for list in uz.state:
            txt = db.GetButtonsById(list)
            lists = lists + f"\n <i>- {txt.name}</i>"

        await msg.edit_text(f"\nSiz tanladingiz: {lists}", parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data == "AgreeForm", state=ProductForm.LastStep)
async def AgreeProccess(callback: types.callback_query, state: FSMContext):
    # Get User Library
    User = callback.from_user
    Lang = db.Lang(User.id)

    msg = callback.message

    if Lang in "ru":

        pass
