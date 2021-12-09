from os import terminal_size
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton, callback_query, inline_keyboard
from aiogram.dispatcher import FSMContext

from database import db

# Globals
state = []

# Get product list

# GLOBAL clear keyboard markup

ClearKb = ReplyKeyboardRemove()
ClearIn = InlineKeyboardMarkup()
ClearIn.clean()

# Main markup
ProductMainMarkup = ReplyKeyboardMarkup()

ProductMainMarkup.clean()
ProductMainMarkup.add("Назад")

# Main markup

ProductList = db.getProducts()

ProductListButton = InlineKeyboardMarkup()

for list in ProductList:

    ProductListButton.add(InlineKeyboardButton(
        text=list.name, callback_data=f"id{str(list.id)}"))

# Order
OrderType = InlineKeyboardMarkup()

OrderType.add(InlineKeyboardButton(
    text="Онлайн заказ", callback_data="OnlineOrder"))
OrderType.add(InlineKeyboardButton(
    text="Заказ оператора", callback_data="OperatorOrder"))

# Operator order back button
OperatorBackType = InlineKeyboardMarkup()
OperatorBackType.add(InlineKeyboardButton(
    text="Назад", callback_data="OnlineOperatorBack"))

# Gender
GenderKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

GenderKeyboard.add(InlineKeyboardButton(text="🤵 мужской"))
GenderKeyboard.add(InlineKeyboardButton(text="👩‍🦰 женский"))

# Illness category

IllMarkup = ReplyKeyboardMarkup()

IllMarkup.add("Для женщин")
IllMarkup.add("Прием лекарств от депрессии")


# Illness select


async def Ill(msg, state, data, variant):
    # Cond code

    if variant == "Для женщин":

        Var = db.GetButtons(1)

    elif variant == "Прием лекарств от депрессии":

        Var = db.GetButtons(2)

    # Get
    Markup = InlineKeyboardMarkup()

    async with data.proxy() as d:
        d['Variant'] = variant

    for V in Var:
        if(V.id in state):
            Markup.add(InlineKeyboardButton(
                text=f"{V.name} ✅", callback_data=f"Btn{V.id}"))
        else:
            Markup.add(InlineKeyboardButton(
                text=f"{V.name} ❌", callback_data=f"Btn{V.id}"))

    Markup.add(InlineKeyboardButton(
        text="✅ Продолжить", callback_data="Proceed"))

    Markup.add(InlineKeyboardButton(
        text="Я не болел за указанное время", callback_data="SkipBtn"))

    return Markup


async def IllChange(msg, data, variant):
    # Cond code
    id = db.GetButtonsById(variant).id

    # Get
    if id in state:
        state.remove(variant)
    else:
        state.append(variant)

    async with data.proxy() as d:
        get = await Ill(msg, state, data, d['Variant'])

    return get


# Accept Button
AcceptMarkup = InlineKeyboardMarkup()

AcceptMarkup.add(InlineKeyboardButton(text="Да", callback_data="AgreeForm"),
                 InlineKeyboardButton(text="Нет", callback_data="NotForm"))


# Course select

CourseReplyBtn = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

# CourseReplyBtn.add("5-9 кг", "10-14 кг")
# CourseReplyBtn.add("15-24 кг", "25-35 кг")

# 5-9 10-14 15-24
data = db.getCourses()

# for i in range(0, len(data)):
#     if len(data) % 2 == 0 and i == len(data) + 1:
#         data = data[i + 1]
#     else:

#     CourseReplyBtn.add(data[i]["name"])
counter = 2
for i in range(0, len(data), 2):
    if counter < len(data):
        CourseReplyBtn.add(data[counter - 2].text,
                           data[counter - 1].text)
    else:
        CourseReplyBtn.add(data[counter - 2].text)
    counter += 2

# Contract


async def AddContract(id):
    CourseContract = InlineKeyboardMarkup()

    CourseContract.add(InlineKeyboardButton(
        text="Контракт", callback_data=f"CourseAdd{id}"))

    return CourseContract
