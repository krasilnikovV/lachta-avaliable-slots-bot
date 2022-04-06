import logging
from termcolor import colored
import requests

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
        print(colored(response.json(), "green"))
    except requests.exceptions.RequestException as e:
        logging.error(f"request failed with code {e.response.status_code}")
        exit(-1)
