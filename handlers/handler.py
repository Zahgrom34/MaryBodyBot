import re
from connect import dp
from aiogram import types
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from .conversation import Language, MainMenu, Product
from database import db
from .keyboards import ru, uz
from api import phone


@dp.message_handler(commands=['start'])
async def start(msg: types.message):
    if not db.IsUserExists(user_id=msg.from_user.id):
        await msg.answer('Здравствуйте.  Добро пожаловать в службу поддержки клиентов Mary Naturel Health Center!\nAssalomu alaykum. Meri Naturel sog’lomlashtirish markazi mijozlar bilan ishlash botiga xush kelibsiz!')
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        markup.add('🇺🇿 O\'zbek')
        markup.add('🇷🇺 Русский')
        await msg.answer('<b>Пожалуйста, выберите язык:</b>\n<b>Marhamat tilni tanlang</b>', parse_mode="HTML", reply_markup=markup)
        await Language.lang.set()
    else:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        # Check User Set Lang
        if db.Lang(user_id=msg.from_user.id) == "ru":

            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Продукты"

            else:

                main = "Регистрация"

            markup.add(main, "Сменить язык")
            markup.add("О боте", "Статус заказа")
            await msg.answer('Вы находитесь на главном меню.\nПожалуйста выберите следующее действие:',
                             reply_markup=markup)
        if db.Lang(user_id=msg.from_user.id) == "uz":

            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Mahsulotlar"

            else:

                main = "Ro'yhatdan o'tish"

            markup.add(main, "Tilni o’zgartirish")
            markup.add("Bot haqida", "Buyurtma statusi")
            await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                             reply_markup=markup)
        await MainMenu.main.set()


@dp.message_handler(commands=['restart'], state="*")
async def start(msg: types.message):
    if not db.IsUserExists(user_id=msg.from_user.id):
        await msg.answer('Здравствуйте.  Добро пожаловать в службу поддержки клиентов Mary Naturel Health Center!\nAssalomu alaykum. Meri Naturel sog’lomlashtirish markazi mijozlar bilan ishlash botiga xush kelibsiz!')
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        markup.add('🇺🇿 O\'zbek')
        markup.add('🇷🇺 Русский')
        await msg.answer('<b>Пожалуйста, выберите язык:</b>\n<b>Marhamat tilni tanlang</b>', parse_mode="HTML", reply_markup=markup)
        await Language.lang.set()
    else:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        # Check User Set Lang
        if db.Lang(user_id=msg.from_user.id) == "ru":

            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Продукты"

            else:

                main = "Регистрация"

            markup.add(main, "Сменить язык")
            markup.add("О боте", "Статус заказа")
            await msg.answer('Вы находитесь на главном меню.\nПожалуйста выберите следующее действие:',
                             reply_markup=markup)
        if db.Lang(user_id=msg.from_user.id) == "uz":

            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Mahsulotlar"

            else:

                main = "Ro'yhatdan o'tish"

            markup.add(main, "Tilni o’zgartirish")
            markup.add("Bot haqida", "Buyurtma statusi")
            await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                             reply_markup=markup)
        await MainMenu.main.set()


@dp.message_handler()
async def notChoosed(msg: types.message, state: FSMContext):
    current_state = await state.get_state()
    if (current_state is None):
        await msg.answer("Вы не запустили бота. Пожалуйста запустите бота написав /start")


@dp.message_handler(lambda message: message.text in ["Назад", "Ortga"], state=Language.change)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # Markup
    if db.Lang(message.from_user.id) == "ru":
        await message.answer('Действие отменено!')
    else:
        await message.answer('Amal bekor qilindi!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # Check User Set Lang
    if db.Lang(user_id=message.from_user.id) == "ru":
        if db.SuppliedUser(user_id=message.from_user.id):

            main = "Продукты"

        else:

            main = "Регистрация"
        markup.add(main, "Сменить язык")
        markup.add("О боте", "Статус заказа")
        await message.answer('Вы находитесь на главном меню.\nПожалуйста выберите следующее действие:',
                             reply_markup=markup)
        await state.finish()
        await MainMenu.main.set()

    if db.Lang(user_id=message.from_user.id) == "uz":
        if db.SuppliedUser(user_id=message.from_user.id):

            main = "Mahsulotlar"

        else:

            main = "Ro’yhatdan o’tish"

        markup.add(main, "Tilni o’zgartirish")
        markup.add("Bot haqida", "Buyurtma statusi")
        await message.answer('Assosy menyudan keyingi amalni tanlang!',
                             reply_markup=markup)
        await state.finish()
        await MainMenu.main.set()


@dp.message_handler(lambda msg: msg.text not in ['🇺🇿 O\'zbek', '🇷🇺 Русский'], state=Language.change)
async def name(msg: types.Message):
    await msg.answer('Выберите язык. Нажав на одну из кнопок')


@dp.message_handler(state=Language.change)
async def langChange(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if msg.text in "🇺🇿 O'zbek":
        await msg.answer('Siz O\'zbek tilliga almashtirdiz!', reply_markup=markup)

        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Mahsulotlar"

        else:

            main = "Ro’yhatdan o’tish"

        markup2.add(main, "Tilni o’zgartirish")
        markup2.add("Bot haqida", "Buyurtma statusi")
        await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                         reply_markup=markup2)
        chLang = db.ChangeLang(user_id=msg.from_user.id, lang="uz")
    elif msg.text in "🇷🇺 Русский":
        await msg.answer('Вы успешно поменяли язык на "Русский"!', reply_markup=markup)

        if db.SuppliedUser(user_id=msg.from_user.id):

            main = "Продукты"

        else:

            main = "Регистрация"

        markup2.add(main, "Сменить язык")
        markup2.add("О боте", "Статус заказа")
        await msg.answer('Отлично! Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                         reply_markup=markup2)
        chLang = db.ChangeLang(user_id=msg.from_user.id, lang="ru")

    await state.finish()
    await MainMenu.main.set()


@dp.message_handler(lambda msg: msg.text not in ['🇺🇿 O\'zbek', '🇷🇺 Русский'], state=Language.lang)
async def name(msg: types.Message):
    await msg.answer('Выберите язык. Нажав на одну из кнопок')


@dp.message_handler(state=Language.lang)
async def name(msg: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if (msg.text in "🇺🇿 O'zbek"):
        await msg.answer('Siz O\'zbek tilini tangladiz!', reply_markup=markup)
        markup2.add("Ro’yhatdan o’tish", "Tilni o’zgartirish")
        markup2.add("Bot haqida", "Buyurtma statusi")
        await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                         reply_markup=markup2)
        createUser = db.AddUser(user_id=msg.from_user.id, lang="uz")
    elif (msg.text in "🇷🇺 Русский"):
        await msg.answer('Вы выбрали Русский язык!', reply_markup=markup)
        markup2.add("Регистрация", "Сменить язык")
        markup2.add("О боте", "Статус заказа")
        await msg.answer('Отлично! Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                         reply_markup=markup2)
        createUser = db.AddUser(user_id=msg.from_user.id, lang="ru")
    await state.finish()
    await MainMenu.main.set()


# MainMenu State

@dp.message_handler(state=MainMenu.main)
async def Main(msg: types.message, state: FSMContext):
    # Start list
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Check User Language Set

    if Lang in "ru":

        # Conditions

        if msg.text in "Продукты":

            # Anti hack
            if db.SuppliedUser(user_id=msg.from_user.id):

                # Continue

                Markup = ru.ProductMainMarkup

                # answer
                await msg.answer("---", reply_markup=Markup)
                await msg.answer("О каком продукте вы хотите узнать?", reply_markup=ru.ProductListButton)

                await state.finish()
                await Product.info.set()

            else:
                markup2 = types.ReplyKeyboardMarkup(
                    resize_keyboard=True, selective=True)

                markup2.add("Регистрация", "Сменить язык")
                markup2.add("О боте", "Статус заказа")
                await msg.answer('Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                                 reply_markup=markup2)

        elif msg.text in "Регистрация":

            # Keyboard Markup
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.add('Продолжить')
            markup.add('Назад')

            # Answer to message
            await msg.answer('Теперь вам будут заданы вопросы. После того, как вы ответите на вопросы, нажмите кнопку '
                             'подтверждения, и ваш запрос будет принят Ниже находится кнопка «<b>Назад</b>», '
                             'которая возвращает в главное меню.', parse_mode="HTML", reply_markup=markup)

            await MainMenu.next()

        elif msg.text in "Сменить язык":

            # ReplyKeyBoard
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.clean()
            markup.add('🇺🇿 O\'zbek')
            markup.add('🇷🇺 Русский')
            markup.add('Назад')

            await msg.answer("<b>Выберите язык:</b>", parse_mode="HTML", reply_markup=markup)
            await Language.change.set()

        elif msg.text in "О боте":

            await msg.answer("Ассаламу алейкум. Зарегистрируйтесь в Центре здоровья Mary Naturel, "
                             "чтобы улучшить обслуживание клиентов и изменить свою жизнь к лучшему!")

        elif msg.text in "Статус заказа":

            pass  # Condition code

        else:
            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Продукты"

            else:

                main = "Регистрация"

            markup2.add(main, "Сменить язык")
            markup2.add("О боте", "Статус заказа")
            await msg.answer('Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                             reply_markup=markup2)

    if msg.text in "Mahsulotlar":

        # Anti hack
        if db.SuppliedUser(user_id=msg.from_user.id):

            # Continue

            # answer
            await msg.answer("Qaysi mahsulot haqida ma’lumot olmoqchisiz?", reply_markup=ru.ProductListButton)

            await state.finish()
            await Product.info.set()

        else:
            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)

            markup2.add("Регистрация", "Сменить язык")
            markup2.add("О боте", "Статус заказа")
            await msg.answer('Вы находитесь на главном меню. \nПожалуйста выберите следующее действие:',
                             reply_markup=markup2)

    elif Lang in "uz":

        # Conditions

        if msg.text in "Ro’yhatdan o’tish":

            # Keyboard Markup
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.add('Davom etish')
            markup.add('Ortga')

            # Answer to message
            await msg.answer(
                'Hozir sizga savollar beriladi. Javoblarni to’ldirganingizdan so’ng, tasdiqlash tugmasini bosing va so’rovnomangiz qabul qilinadi.  \n<i>Pastda  Asosiy menyuga qaytadigan <b>“Ortga”</b> tugmasi bo’ladi.</i>',
                parse_mode="HTML", reply_markup=markup)

            await MainMenu.next()

        elif msg.text in "Tilni o’zgartirish":

            # ReplyKeyBoard
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.clean()
            markup.add('🇺🇿 O\'zbek')
            markup.add('🇷🇺 Русский')
            markup.add("Ortga")

            await msg.answer("<b>Tilni tanglang:</b>", parse_mode="HTML", reply_markup=markup)
            await Language.change.set()

        elif msg.text in "Bot haqida":

            await msg.answer("Assalomu alaykum. Meri naturel sog’lomlashtirish markazi mijozlar bilan ishlash "
                             "servisini yaxshilash uchun ochilgan botida ro’yhatdan o’ting va hayotingizni yaxshi "
                             "tomonga o’zgartiring!")

        elif msg.text in "Buyurtma statusi":

            pass  # Condition code

        else:
            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            if db.SuppliedUser(user_id=msg.from_user.id):

                main = "Mahsulotlar"

            else:

                main = "Ro'yhatdan o'tish"

            markup2.add(main, "Tilni o’zgartirish")
            markup2.add("Bot haqida", "Buyurtma statusi")
            await msg.answer('Assosy menyudan keyingi amalni tanlang!',
                             reply_markup=markup2)


@dp.message_handler(lambda msg: msg.text in ["Продолжить", "Davom etish"], state=MainMenu.register)
async def RegisterProcess(msg: types.Message, state: FSMContext):
    # Main List
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Language Conditions
    if Lang in "ru":
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        markup.clean()
        markup.add(types.KeyboardButton(
            text="Отправить мой контакт", request_contact=True))
        markup.add("Назад")

        await msg.answer("Номер телефона*, нажмите на «Отправить мой контакт» или отправьте мне свой номер "
                         "формате: +998 99 999 99 99", reply_markup=markup)

    elif Lang in "uz":

        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        markup.clean()
        markup.add(types.KeyboardButton(
            text="Kontaktimni jo'natish", request_contact=True))

        await msg.answer(
            "Telefon nomeri*, «Kontaktimni jo'natish» tugmasini bosing yoki qo'lda nomerizni terib yuvoring"
            "<b>+998 99 999 99 99</b> formatda", parse_mode="HTML", reply_markup=markup)

    await MainMenu.next()


@dp.message_handler(content_types=['contact'], state=MainMenu.phone)
async def GetContact(msg: types.Message, state: FSMContext):
    # Main List Get
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Language Condition
    async with state.proxy() as data:

        data['RegPhone'] = msg.contact.phone_number
        # print(msg.contact.phone_number)
        markup = types.ReplyKeyboardRemove()

        if Lang in "ru":

            await msg.answer(f'На ваш номер +{msg.contact.phone_number} Отправлен СМС с кодом подтверждения! \nПодтвердите свой номер: ', reply_markup=markup)

        elif Lang in "uz":

            await msg.answer(f"Tasdiqlash kodi bilan SMS +{msg.contact.phone_number} raqamingizga yuborildi! \nRaqamingizni tasdiqlang: ", reply_markup=markup)

        phone.SendMessage(User.id, msg.contact.phone_number, Lang)
        await MainMenu.next()


@dp.message_handler(lambda msg: re.findall(r"\+?[\d]{3} [\d]{2} [\d]{3} [\d]{2} [\d]{2}", msg.text) or re.findall(
    r"\+?[\d]{3} [\d]{2} [\d]{3} [\d]{4}", msg.text),
    state=MainMenu.phone)
async def GetNumber(msg: types.Message, state: FSMContext):
    # Main List Get
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Message edit
    Rep1 = msg.text.replace(" ", "")
    Rep2 = Rep1.replace("+", "")

    # Language Condition
    async with state.proxy() as data:

        data['RegPhone'] = Rep2

        markup = types.ReplyKeyboardRemove()

        if Lang in "ru":

            await msg.answer(f'На ваш номер +{Rep2} Отправлен СМС с кодом подтверждения! \nПодтвердите свой номер: ', reply_markup=markup)

        elif Lang in "uz":

            await msg.answer(f"Tasdiqlash kodi bilan SMS +{Rep2} raqamingizga yuborildi! \nRaqamingizni tasdiqlang: ", reply_markup=markup)

        phone.SendMessage(User.id, msg.contact.phone_number, Lang)
        await MainMenu.next()


@dp.message_handler(lambda msg: not re.findall(r"\+?[\d]{3} [\d]{2} [\d]{3} [\d]{2} [\d]{2}", msg.text) or re.findall(
    r"\+?[\d]{3} [\d]{2} [\d]{3} [\d]{4}", msg.text),
    state=MainMenu.phone)
async def GetNumber(msg: types.Message, state: FSMContext):
    # Main List Get
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Lang condition
    if Lang in "ru":

        # Message edit
        await msg.answer("Формат номера телефона должен быть: +998 99 999 99 99 или +998 99 999 9999!")

    elif Lang in "uz":

        # Message edit
        await msg.answer(
            "Telefon nomeringizni formati <b>+998 99 999 99 99</b> yoki <b>+998 99 999 9999</b> bo'lish kerak!",
            parse_mode="HTML")


@dp.message_handler(state=MainMenu.AcceptPhone)
async def AcceptPhoneProcess(msg: types.message, state: FSMContext):
    # Get name and lang
    User = msg.from_user
    Lang = db.Lang(User.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    verify = phone.Verify(User.id, msg.text)

    # Check phone number
    if verify:
        if Lang in "ru":
            markup.clean()
            await msg.answer('Код подтверждён! Теперь отправьте мне ваше имя и фамилия: ', reply_markup=markup)
            await MainMenu.next()

        elif Lang in "uz":
            markup.clean()
            await msg.answer("Kod qabul qilindi! Ism va familiya * : ", reply_markup=markup)
            await MainMenu.next()

    else:
        if Lang in "ru":
            await msg.answer('Код подтверждения не верный!', reply_markup=markup)

        elif Lang in "uz":
            await msg.answer('Tekshirov kod no tog\'ri!')


@dp.message_handler(state=MainMenu.name)
async def NameProcess(msg: types.message, state: FSMContext):
    # Get name and surname
    User = msg.from_user
    Lang = db.Lang(User.id)

    async with state.proxy() as data:
        text = msg.text
        name, surname = text.split()

        data['RegName'] = name
        data['RegSurname'] = surname

        # Send message and Next state
        if Lang in "ru":

            await msg.answer("Прекрасно! Теперь отпраьте мне ваш Адрес")
            await MainMenu.next()

        elif Lang in "uz":

            await msg.answer("endi manzilingizni yuboring")
            await MainMenu.next()


@dp.message_handler(state=MainMenu.adress)
async def AdressProcess(msg: types.message, state: FSMContext):
    # Get name and lang
    User = msg.from_user
    Lang = db.Lang(User.id)

    async with state.proxy() as data:
        data['RegAdress'] = msg.text

        # Language
        if Lang in "ru":

            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.clean()
            markup.add("Пропустить")

            await msg.answer("Блестяще! Введите Адрес электронной почты (Необязательно): ", reply_markup=markup)

        elif Lang in "uz":

            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup.clean()
            markup.add("O'tkazib yuborish")

            await msg.answer("Email manzil (ixtiyoriy): ", reply_markup=markup)

        await MainMenu.next()


@dp.message_handler(lambda msg: msg.text in ["Пропустить", "O'tkazib yuborish"], state=MainMenu.email)
async def SkipEmail(msg: types.message, state: FSMContext):
    # Get name and lang
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Store
    async with state.proxy() as data:
        data['RegEmail'] = "None"

        # Conditions
        if Lang in "ru":

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                'Подтвердить', callback_data='accept'))

            markup2 = types.ReplyKeyboardRemove()

            await msg.answer("Готово!", reply_markup=markup2)
            await msg.answer(
                f"<b>Вы ответили на все вопросы</b>\nФамилия и имя: {data['RegName']}\nНомер телефона: {data['RegPhone']}\nАдрес: {data['RegAdress']}\nEmail: <i>Не указано</i>.\nНажмите на «<b>Подтвердить</b>» чтобы продолжить",
                reply_markup=markup, parse_mode="HTML")

        elif Lang in "uz":

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                'Taqdiqlash', callback_data='accept'))

            markup2 = types.ReplyKeyboardRemove()

            await msg.answer("Hammasi tayyor!", reply_markup=markup2)
            await msg.answer(
                f"<b>Siz hamma savollarga javob berdiz!</b>\nIsm familiya: {data['RegName']}\nTelefon nomer: {data['RegPhone']}\nManzilingiz: {data['RegAdress']}\nEmail: <i>Не указано</i>.\nTasdiqlash tugmasini bosing davom etish uchun",
                reply_markup=markup,
                parse_mode="HTML")


@dp.message_handler(lambda msg: msg.text not in ["Пропустить", "O'tkazib yuborish"], state=MainMenu.email)
async def EmailProcess(msg: types.message, state: FSMContext):
    # Get name and lang
    User = msg.from_user
    Lang = db.Lang(User.id)

    # Store
    async with state.proxy() as data:
        data['RegEmail'] = msg.text

        # Conditions
        if Lang in "ru":

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                'Подтвердить', callback_data='accept'))

            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup2.clean()

            await msg.answer("Готово!", reply_markup=markup2)
            await msg.answer(f"<b>Вы ответили на все вопросы</b>\n"
                             f"Фамилия и имя: {data['RegName']}\n"
                             f"Номер телефона: {data['RegPhone']}\n"
                             f"Адрес: {data['RegAdress']}\n"
                             f"Email: {data['RegEmail']}.\n"
                             f"Нажмите на «<b>Подтвердить</b>» чтобы продолжить", reply_markup=markup,
                             parse_mode="HTML")

        elif Lang in "uz":

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                'Taqdiqlash', callback_data='accept'))

            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True, selective=True)
            markup2.clean()

            await msg.answer("Hammasi tayyor!", reply_markup=markup2)
            await msg.answer(f"<b>Siz hamma savollarga javob berdiz!</b>\n"
                             f"Ism familiya: {data['RegName']}\n"
                             f"Telefon nomer: {data['RegPhone']}\n"
                             f"Manzilingiz: {data['RegAdress']}\n"
                             f"Email: <i>Не указано</i>.\n"
                             f"Tasdiqlash tugmasini bosing davom etish uchun", reply_markup=markup,
                             parse_mode="HTML")


# Accept Callback Data
@dp.callback_query_handler(lambda c: c.data == "accept", state=MainMenu.email)
async def AcceptProcess(callback: types.CallbackQuery, state: FSMContext):
    # Accept Process List...
    User = callback.from_user
    Lang = db.Lang(User.id)

    # Storage

    async with state.proxy() as data:

        db.SupplementUser(user_id=User.id, first_name=data['RegName'], last_name=data['RegSurname'],
                          phone=str(data['RegPhone']), address=data['RegAdress'], email=data['RegEmail'])

        markup = types.ReplyKeyboardRemove()

        # Language
        if Lang in "ru":

            await callback.message.answer("Вы успешно прошли регистрацию!", reply_markup=markup)
            await callback.message.answer("О каком продукте вы хотите узнать?", reply_markup=ru.ProductListButton)

        elif Lang in "uz":

            await callback.message.answer("Siz ro'yxatdan o'tdiz!", reply_markup=markup)
            await callback.message.edit_text("Qaysi mahsulot haqida ma’lumot olmoqchisiz?", reply_markup=uz.ProductListButton)

        await state.finish()
        await Product.info.set()
