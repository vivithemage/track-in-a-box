import json
import requests
import xmltodict

from log import tlog

tc_endpoints = {
    'entries': 'https://app.timecamp.com/third_party/api/entries',
    'timer': 'https://app.timecamp.com/third_party/api/timer'
}

# Seperate api keys, makes it easy to switch during testing
api_key = {
    'key':  'Your programming API token', # your key
}


# All interactions with timecamp.
class TimecampApi:
    def __init__(self):
        self.headers = {
            'authorization': api_key['key'],
            'Content-Type': "application/json"
        }

    def start_timer(self, task_id):
        tlog("Starting timer")
        payload = {'action': 'start',
                   'task_id': task_id}

        # TODO: issue lies with this triggering the whole process again.
        response = requests.request("POST", tc_endpoints['timer'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        tlog("Timecamp timer start response")
        data_dict = xmltodict.parse(response.text)

        return data_dict.get('xml')['entry_id']

    def set_description(self, entry_id, description):
        tlog("Writing description to timer")
        payload = {'id': entry_id, 'description': description}

        # TODO: issue lies with this triggering the whole process again.
        response = requests.request("PUT", tc_endpoints['entries'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        data_dict = xmltodict.parse(response.text)
        # print(data_dict)

    def stop_timer(self):
        tlog("Stopping timer")
        payload = {'action': "stop"}

        response = requests.request("POST", tc_endpoints['timer'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        data_dict = xmltodict.parse(response.text)
