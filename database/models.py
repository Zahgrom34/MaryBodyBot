from typing import Text
from peewee import *
from .connect import db


class Users(Model):
    name = CharField()
    surname = CharField()
    lang = CharField()
    userid = IntegerField()
    phone = CharField(default="None")
    address = CharField(default="None")
    email = CharField(default="None")
    authorized = BooleanField(default=False)

    class Meta:
        database = db


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    uzname = CharField(max_length=255)
    uzdescription = TextField()
    link = TextField()

    class Meta:
        database = db


class productButtons(Model):
    identy = IntegerField()
    name = CharField(max_length=255)
    uzname = CharField(max_length=255)

    class Meta:
        database = db


class Courses(Model):
    title = CharField(max_length=255)
    uztitle = CharField(max_length=255)
    text = CharField(max_length=15)
    description = TextField()
    uzdescription = TextField()

    class Meta:
        database = db


db.connect()
db.create_tables([Users, Product, productButtons, Courses])
