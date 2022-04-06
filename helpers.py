import logging
from functools import partial
from operator import is_not

from urllib3 import util as url_util

import config

clinics = {
    "савушкина": 228,
    "ковенский": 259
}

doctors = {
    "костин антон сергеевич": 4480,
    "пальчикова екатерина игоревна": 5576
}

url = url_util.Url(scheme="https", host="lahtaclinic.ru", path="/app/app.php")

method = "get_doctors_schedule_available_for_clinics"
is_online = config.is_online
dms = config.dms
list_clinics = list(filter(partial(is_not, None), [clinics.get(c.lower(), None) for c in config.clinics]))
list_doctors = list(filter(partial(is_not, None), [doctors.get(d.lower(), None) for d in config.doctors]))
logging.info(f"List of clinics: {str(list_clinics)}")
logging.info(f"List of doctors: {str(list_doctors)}")
