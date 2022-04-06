import logging

import requests
from termcolor import colored

import helpers


def build_req_body():
    body: str = f"method={helpers.method}" \
                f"&dms={helpers.dms}" \
                f"&list_clinics={','.join([str(c) for c in helpers.list_clinics])}" \
                f"&list_doctors={','.join([str(d) for d in helpers.list_doctors])}" \
                f"&is_online={helpers.is_online}"
    return body


def get_doctors_schedule():
    url = helpers.url
    payload = build_req_body()
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/99.0.4844.51 Safari/537.36'
    }
    try:
        response = requests.request("POST", url=url, headers=headers, data=payload)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response=response)
        if response.text == '':
            raise requests.exceptions.RequestException(response=response)
        response_obj = response.json()
        print(colored(response_obj, "green"))
    except requests.exceptions.RequestException as e:
        logging.error(f"request failed with code {e.response.status_code}")
        exit(-1)


class DoctorSchedule:
    def __init__(self, _schedule: dict, doctor_id: int):
        self.doctor_id = doctor_id
        self._result_schedule = {}
        for k_clinic_id, v_clinic in _schedule.items():
            if v_clinic is not None:
                for k_schedule, v_schedule in v_clinic.items():
                    if str(doctor_id) in v_schedule.keys():
                        pass #TODO:
