import json
import requests
from var.messages import ERROR_OK
from var.network import REPORTING_BASE_URL


class ReportingInterface:
    def __init__(self):
        self.base_url = REPORTING_BASE_URL

        self.generate_url = self.base_url + 'generateStatement'

    # generate pdf report
    def generate(self, args):
        try:
            answ = requests.post(self.generate_url, data=json.dumps(args))

            return True, ERROR_OK, answ.content

        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'ReportingInterface.generate()'), None
