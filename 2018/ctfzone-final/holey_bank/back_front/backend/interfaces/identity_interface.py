import json
import requests
from var.messages import ERROR_OK, ERROR_NO_MESSAGE
from var.network import IDENTITY_BASE_URL


class IdentityInterface:
    def __init__(self):
        self.base_url = IDENTITY_BASE_URL

        self.register_url       = self.base_url + 'register'
        self.auth_url           = self.base_url + 'authenticate'
        self.set_info_url       = self.base_url + 'set_info'
        self.get_info_url       = self.base_url + 'authentication_get_info'
        self.get_all_info_url   = self.base_url + 'get_all_users'
        self.get_info_by_id_url = self.base_url + 'get_info/'

    # authentication
    def login(self, args):
        try:
            answ = requests.post(self.auth_url, data=json.dumps(args)).json()

            if 'message' in answ:
                message = answ['message']
            else:
                message = ERROR_NO_MESSAGE

            return ('result' in answ), message

        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.login()')

    # registration
    def register(self, args):
        try:
            answ = requests.post(self.register_url, data=json.dumps(args)).json()

            if 'message' in answ:
                message = answ['message']
            else:
                message = ERROR_NO_MESSAGE

            return ('result' in answ), message
        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.register()')

    # set_info
    def set_info(self, args):
        try:
            answ = requests.post(self.set_info_url, data=json.dumps(args)).json()

            if 'message' in answ:
                message = answ['message']
            else:
                message = ERROR_NO_MESSAGE

            return ('result' in answ), message
        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.set_info()')

    # get_info
    def get_info(self, args):
        try:
            answ = requests.post(self.get_info_url, data=json.dumps(args)).json()

            if 'error' in answ:
                return False, answ['error'], None

            user_data = {'username': answ['authentication']['username'],
                         'passport_number': answ['passport']['passport_number'],
                         'full_name': answ['passport']['full_name'],
                         'residence': answ['passport']['residence']}
            return True, ERROR_OK, user_data

        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.get_info()'), None

    # get_all_info
    def get_all_info(self):
        try:
            answ = requests.get(self.get_all_info_url).json()

            if 'error' in answ:
                return False, answ['error'], None

            users = []
            for user in answ['authentications']:
                users.append({'id': user['id'], 'username': user['username']})

            user_data = {'users': users}
            return True, ERROR_OK, user_data

        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.get_all_info()'), None

    # get_info_by_id
    def get_info_by_id(self, args):
        try:
            answ = requests.get(self.get_info_by_id_url + args['id']).json()

            if 'error' in answ:
                return False, answ['error'], None

            if answ['authentication']['username'] == args['username']:

                user_data = {'username': answ['authentication']['username'],
                             'passport_number': answ['passport']['passport_number'],
                             'full_name': answ['passport']['full_name'],
                             'residence': answ['passport']['residence']}

            else:
                user_data = {'username': answ['authentication']['username']}
            return True, ERROR_OK, user_data

        except Exception as ex:
            return False, 'Exception: {0} at {1}'.format(str(ex), 'IdentityInterface.get_info_by_id()'), None