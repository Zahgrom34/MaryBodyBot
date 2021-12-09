from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton
from database import db

# Globals

state = []

# get Product list
ProductList = db.getProducts()

# Main markup
ProductMainMarkup = ReplyKeyboardMarkup()

ProductMainMarkup.clean()
ProductMainMarkup.add("Назад")

# Main markup

ProductListButton = InlineKeyboardMarkup()

for list in ProductList:

    ProductListButton.add(InlineKeyboardButton(
        text=list.uzname, callback_data=f"id{str(list.id)}"))

# Order
OrderType = InlineKeyboardMarkup()

OrderType.add(InlineKeyboardButton(
    text="Onlayn buyurtma", callback_data="OnlineOrder"))
OrderType.add(InlineKeyboardButton(
    text="Operatorga buyurtma", callback_data="OperatorOrder"))

# Operator order back button
OperatorBackType = InlineKeyboardMarkup()
OperatorBackType.add(InlineKeyboardButton(
    text="Ortga", callback_data="OnlineOperatorBack"))

# Gender
GenderKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

GenderKeyboard.add(InlineKeyboardButton(text="🤵 erkak"))
GenderKeyboard.add(InlineKeyboardButton(text="👩‍🦰 ayol"))

# Illness category

IllMarkup = ReplyKeyboardMarkup()

IllMarkup.add("Ayollar uchun")
IllMarkup.add("Depressiya uchun dori ichmoqda")


# Illness select


async def Ill(msg, state, data, variant):
    # Cond code

    if variant == "Ayollar uchun":

        Var = db.GetButtons(1)

    elif variant == "Depressiya uchun dori ichmoqda":

        Var = db.GetButtons(2)

    # Get
    Markup = InlineKeyboardMarkup()

    async with data.proxy() as d:
        d['Variant'] = variant

    for V in Var:
        if(V.id in state):
            Markup.add(InlineKeyboardButton(
                text=f"{V.uzname} ✅", callback_data=f"Btn{V.id}"))
        else:
            Markup.add(InlineKeyboardButton(
                text=f"{V.uzname} ❌", callback_data=f"Btn{V.id}"))

    Markup.add(InlineKeyboardButton(
        text="✅ Davom etish", callback_data="Proceed"))

    Markup.add(InlineKeyboardButton(
        text="Belgilangan vaqt davomida men kasal bo'lmaganman", callback_data="SkipBtn"))

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


# Course select

CourseReplyBtn = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

CourseReplyBtn.add("5-9 kg", "10-14 kg")
CourseReplyBtn.add("15-24 kg", "25-35 kg")


# Course Contract Btn

async def AddContract(id):
    CourseContract = InlineKeyboardMarkup()

    CourseContract.add(InlineKeyboardButton(
        text="Shartnoma tuzish", callback_data=f"CourseAdd{id}"))

    return CourseContract
