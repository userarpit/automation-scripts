#! python 3

import pyperclip
import re
import pprint

# pprint.pprint(pyperclip.paste())

phonenumberregex = re.compile(r"""(\d{5}-\d{5})""", re.VERBOSE)
emailregex = re.compile(
    r"""[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}""", re.VERBOSE
)

mo_phone = phonenumberregex.findall(pyperclip.paste())
mo_email = emailregex.findall(pyperclip.paste())
pprint.pprint(mo_phone)
pprint.pprint(mo_email)
pprint.pprint(len(mo_phone))
pprint.pprint(len(mo_email))
phone_and_email = []
for p, e in zip(mo_phone, mo_email):
    phone_and_email.append(p + " " + e)

pyperclip.copy("\n".join(phone_and_email))
