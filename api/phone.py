from urllib.parse import urlencode
from urllib.request import Request, urlopen

from aiogram.types import user
from configuration import PHONE_API_URL, PHONE_SECRET
from random import randint

Code = {}


def SendMessage(userid, phone, lang):
    # Send Message
    global Code

    code = randint(10000, 600000)
    if lang in "ru":

        txt = f"Vash kod podtverjdeniya: {str(code)}"

    elif lang in "uz":
        txt = f"Sizni tasdiqlash kodingiz: {str(code)}"

    Fields = {"key": PHONE_SECRET, "phone": phone, "text": txt}

    Code[userid] = code

    request = Request(PHONE_API_URL, urlencode(Fields).encode())
    json = urlopen(request).read().decode()
    print(json)


def Verify(userid, code):
    global Code

    if userid in Code:

        if code == str(Code[userid]):

            return True

        else:

            return False

    else:

        return False
