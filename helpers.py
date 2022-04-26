import logging
from datetime import datetime, date
from functools import partial
from operator import is_not

from urllib3 import util as url_util

import config

clinics = {
    "савушкина": 228,
    "ковенский": 259
}

clinics_ids = {
    '228': "Савушкина",
    '259': "Ковенский"
}

doctors = {
    "костин антон сергеевич": 4480,
    "пальчикова екатерина игоревна": 5576,
    "aaaa": 113  # TODO: remove this
}

doctors_ids = {
    '4480': "Костин Антон Сергеевич \(Психиатр\)",
    '5576': "Пальчикова Екатерина Игоревна \(Психиатр\)",
    '113': "ГРААaaa"  # TODO: remove this
}

url = url_util.Url(scheme="https", host="lahtaclinic.ru", path="/app/app.php")

method = "get_doctors_schedule_available_for_clinics"
is_online = config.is_online
dms = config.dms
list_clinics = list(filter(partial(is_not, None), [clinics.get(c.lower(), None) for c in config.clinics]))
list_doctors = list(filter(partial(is_not, None), [doctors.get(d.lower(), None) for d in config.doctors]))
logging.info(f"List of clinics: {str(list_clinics)}")
logging.info(f"List of doctors: {str(list_doctors)}")


def default_json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, url_util.Url):
        return obj.url
    else:
        try:
            return str(obj)
        except:
            pass
    raise TypeError("Type %s not serializable" % type(obj))
