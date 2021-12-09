from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup


class Language(StatesGroup):
    lang = State()  # Will be represented in storage as 'Form:language'
    change = State()


class MainMenu(StatesGroup):
    main = State()
    register = State()
    phone = State()
    AcceptPhone = State()
    name = State()
    adress = State()
    email = State()


class Product(StatesGroup):
    info = State()
    order = State()
    form = State()
    acceptment = State()
    height = State()
    weight = State()
    course = State()


class ProductForm(StatesGroup):
    age = State()
    gender = State()
    group = State()
    LastStep = State()
