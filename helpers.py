from urllib3 import util as url_util

import config

clinics = {
    "Савушкина": 228,
    "Ковенский": 259
}

doctors = {
    "Костин Антон Сергеевич": 4480,
    "Пальчикова Екатерина Игоревна": 5576
}

url = url_util.Url(scheme="https", host="lahtaclinic.ru", path="/app/app.php")

method = "get_doctors_schedule_available_for_clinics"
is_online = config.is_online
oms = config.oms
list_clinics = []
list_doctors = []