from .models import Courses, Users, Product, productButtons


def getUser(user_id):
    getUser = Users.select().where(Users.userid == int(user_id)).get()
    return getUser


def IsUserExists(user_id):
    UserQuery = Users.select().where(Users.userid == int(user_id))
    return bool(UserQuery.exists())


def AddUser(user_id, lang):
    createUser = Users.create(
        name="None", surname="None", lang=lang, userid=user_id)
    return bool(createUser)


def Lang(user_id):
    UserLang = getUser(user_id=user_id).lang
    return UserLang


def ChangeLang(user_id, lang):
    # GetUser Lang
    language = Users.select().where(Users.userid == int(user_id)).get()

    language.lang = lang
    language.save()
    return lang


def SupplementUser(user_id, first_name, last_name, phone, address, email="None"):
    # Get User
    User = Users.select().where(Users.userid == int(user_id)).get()

    # Update data
    User.name = first_name
    User.surname = last_name
    User.phone = phone
    User.address = address
    User.email = email
    User.authorized = True

    User.save()
    return User


def SuppliedUser(user_id):
    # Get User
    User = Users.select().where(Users.userid == int(user_id)).get()

    # Return data
    return bool(User.authorized)


# Products

def getProduct(product_id):
    # get product
    GetProduct = Product.select().where(Product.id == int(product_id)).get()

    return GetProduct


def getProducts():
    # get all products
    GetProducts = Product.select()

    return GetProducts

# Product 3 state buttons


def GetButtons(Identy):
    # Get Buttons
    GetBttns = productButtons.select().where(productButtons.identy == int(Identy))

    return GetBttns


def GetButtonsById(Id):
    # Get Buttons
    GetBtns = productButtons.select().where(productButtons.id == int(Id)).get()

    return GetBtns


# Courses

def getCourses():
    # Get Courses
    GetCourses = Courses.select()

    return GetCourses


def getCourse(name):
    # Get Course
    GetCourse = Courses.select().where(Courses.text == name).get()

    return GetCourse


def CourseExists(name):
    # Check
    Exists = Courses.select().where(Courses.text == name)

    return bool(Exists.exists())
