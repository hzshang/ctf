import re
import urllib.request
from flask import session
from flask_restful import Resource, reqparse
from common.util import login_required
from interfaces.identity_interface import IdentityInterface
from interfaces.processing_interface import ProcessingInterface
from var.messages import ERROR_FIELD_EMPTY, ERROR_UNAUTHORIZED
from var.network import STATUS_OK, STATUS_UNAUTHORIZED, STATUS_FORBIDDEN


class Processing(Resource):

    def __init__(self):
        self.identity_interface = IdentityInterface()
        self.processing_interface = ProcessingInterface()

        # Regex for links
        self.link_regex = re.compile(r'[a-z]{3,5}:\/\/[\S]*')

    # get card/account info or history
    @login_required
    def get(self, type=None):
        passport, message = self._get_passport_by_username()
        if passport is None:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        # @deprecated
        if type == 'cards_history':
            parser = reqparse.RequestParser()
            parser.add_argument('cards', type=str)  # location='json'
            args = parser.parse_args()
            for field in args:
                if args[field] is None or len(str(args[field])) == 0:
                    return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

            args = {'cards': args['cards'], 'passport': passport}
            result, message, data = self.processing_interface.get_cards_history(args)
            if result:
                return {'code': STATUS_OK, 'message': message, 'data': data}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        elif type == 'history':
            result, message, data = self.processing_interface.get_history({'passport': passport})

            if result:
                return {'code': STATUS_OK, 'message': message, 'data': data}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        elif type == 'full_history':
            result, message, data = self.processing_interface.get_full_history({'passport': passport})

            if result:
                return {'code': STATUS_OK, 'message': message, 'data': data}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        # Get info
        else:
            result, message, data = self.processing_interface.get_info({'passport': passport})

            if result:
                return {'code': STATUS_OK, 'message': message, 'data': data}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

    # add transaction, type = {a2a, c2c, a2c, c2a}
    @login_required
    def post(self, type=None):
        passport, message = self._get_passport_by_username()
        if passport is None:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        if type == 'c2c':
            return self._c2c(passport)
        elif type == 'c2a':
            return self._c2a(passport)
        elif type == 'a2c':
            return self._a2c(passport)
        else:
            return self._a2a(passport)

    # add card
    @login_required
    def put(self, type=None):
        passport, message = self._get_passport_by_username()
        if passport is None:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        result, message = self.processing_interface.create_card({'passport': passport})

        if result:
            return {'code': STATUS_OK, 'message': message}, STATUS_OK
        else:
            return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

    # a2a transaction
    def _a2a(self, passport):
        parser = reqparse.RequestParser()
        parser.add_argument('to', type=int)  # location='json'
        parser.add_argument('comment', type=str)  # location='json'
        parser.add_argument('sum', type=int)  # location='json'
        args = parser.parse_args()

        for field in args:
            if args[field] is None or len(str(args[field])) == 0:
                return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

        args['comment'] = self._preview_link(args['comment'])
        args['passport'] = passport
        result, message = self.processing_interface.a2a(args)

        if result:
            return {'code': STATUS_OK, 'message': message}, STATUS_OK
        else:
            return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

    # a2c transaction
    def _a2c(self, passport):
        parser = reqparse.RequestParser()
        parser.add_argument('to', type=int)  # location='json'
        parser.add_argument('comment', type=str)  # location='json'
        parser.add_argument('sum', type=int)  # location='json'
        args = parser.parse_args()

        for field in args:
            if args[field] is None or len(str(args[field])) == 0:
                return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

        args['comment'] = self._preview_link(args['comment'])
        args['passport'] = passport

        result, message, data = self.processing_interface.get_info({'passport': passport})

        if not result:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        has_card = False
        for db_card in data['cards']:
            if db_card['id'] == str(args['to']):
                has_card = True
                break

        if not has_card:
            return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_UNAUTHORIZED}, STATUS_UNAUTHORIZED

        result, message = self.processing_interface.a2c(args)

        if result:
            return {'code': STATUS_OK, 'message': message}, STATUS_OK
        else:
            return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

    # c2a transaction
    def _c2a(self, passport):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=int)  # location='json'
        parser.add_argument('comment', type=str)  # location='json'
        parser.add_argument('sum', type=int)  # location='json'
        args = parser.parse_args()

        for field in args:
            if args[field] is None or len(str(args[field])) == 0:
                return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

        args['comment'] = self._preview_link(args['comment'])
        args['passport'] = passport

        result, message, data = self.processing_interface.get_info({'passport': passport})

        if not result:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        has_card = False
        for db_card in data['cards']:
            if db_card['id'] == str(args['from']):
                has_card = True
                break

        if not has_card:
            return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_UNAUTHORIZED}, STATUS_UNAUTHORIZED

        result, message = self.processing_interface.c2a(args)

        if result:
            return {'code': STATUS_OK, 'message': message}, STATUS_OK
        else:
            return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

    # c2a transaction
    def _c2c(self, passport):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=int)  # location='json'
        parser.add_argument('to', type=int)  # location='json'
        parser.add_argument('comment', type=str)  # location='json'
        parser.add_argument('sum', type=int)  # location='json'
        args = parser.parse_args()

        for field in args:
            if args[field] is None or len(str(args[field])) == 0:
                return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

        args['comment'] = self._preview_link(args['comment'])
        args['passport'] = passport

        result, message, data = self.processing_interface.get_info({'passport': passport})

        if not result:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        has_card = False
        for db_card in data['cards']:
            if db_card['id'] == str(args['from']):
                has_card = True
                break

        if not has_card:
            return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_UNAUTHORIZED}, STATUS_UNAUTHORIZED

        result, message = self.processing_interface.c2c(args)

        if result:
            return {'code': STATUS_OK, 'message': message}, STATUS_OK
        else:
            return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

    # Get passport number by username
    def _get_passport_by_username(self):
        auth = {'username': session['username']}
        result, message, user_info = self.identity_interface.get_info(auth)
        if result:
            if len(str(user_info['passport_number'])) > 0:
                return int(user_info['passport_number']), message
            else:
                return None, ERROR_FIELD_EMPTY + 'passport_number'
        else:
            return None, message

    # Find substring between two other strings
    def _substr(self, search, start, finish):
        return search[search.find(start) + len(start): search.find(finish, search.find(start) + len(start))]

    # Preview link in comment
    def _preview_link(self, comment):
        try:
            link = self.link_regex.search(comment)

            if link is not None:
                url = link.group()

                try:
                    with urllib.request.urlopen(url) as response:
                        html = response.read().decode('unicode_escape')
                        response_text = self._substr(html, '<body>', '</body>')
                except Exception as ex:
                    response_text = str(ex)

                return self.link_regex.sub(response_text, comment)

            else:
                return comment

        except Exception as ex:
            return comment
