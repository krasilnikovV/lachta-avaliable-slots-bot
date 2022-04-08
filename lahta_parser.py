import logging
from datetime import datetime

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
        return response_obj
    except requests.exceptions.RequestException as e:
        logging.error(f"request failed with code {e.response.status_code}")
        exit(-1)


class DoctorSchedule:
    def __init__(self, _schedule: dict, doctor_id: int):
        self.__schedule = None
        self.doctor_id = doctor_id
        self._doctor_id_str = str(doctor_id)
        self._result_schedule = {}
        for k_clinic_id, v_clinic in _schedule.items():
            if v_clinic is not None:
                for k_schedule, v_schedule in v_clinic.items():
                    if v_schedule is not None and self._doctor_id_str in v_schedule.keys():
                        doctor_schedule = v_schedule.pop(self._doctor_id_str)
                        if self._result_schedule.get(self._doctor_id_str, None) is None:
                            self._result_schedule[self._doctor_id_str] = {}
                        if self._result_schedule[self._doctor_id_str].get(str(k_clinic_id), None) is None:
                            self._result_schedule[self._doctor_id_str][str(k_clinic_id)] = {}
                        if self._result_schedule[self._doctor_id_str][str(k_clinic_id)].get(k_schedule, None) is None:
                            self._result_schedule[self._doctor_id_str][str(k_clinic_id)][k_schedule] = []
                        for time in doctor_schedule:
                            self._result_schedule[self._doctor_id_str][str(k_clinic_id)][k_schedule].append(
                                time.get("from", None)
                            )
        return

    def get_pretty_schedule(self):
        if not self._result_schedule:
            return None
        if self.__schedule:
            return self.__schedule
        self.__schedule = {}
        for k_doctor, v_doctor in self._result_schedule.items():
            doc = helpers.doctors_ids[k_doctor]
            self.__schedule[doc] = {}
            self.__schedule[doc]["url"] = helpers.url_util.Url(
                scheme=helpers.url.scheme,
                host=helpers.url.host,
                path='/app/',
                fragment=f"doctor={k_doctor}"
            )
            for k_clinic, v_clinic in v_doctor.items():
                cli = helpers.clinics_ids[k_clinic]
                self.__schedule[doc][cli] = []
                for k_data, v_data in v_clinic.items():
                    for time in v_data:
                        dt = datetime.strptime(k_data + " " + time, "%Y-%m-%d %H:%M")
                        self.__schedule[doc][cli].append(dt)
        return self.__schedule
