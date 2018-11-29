from flask import session
from flask_restful import Resource, reqparse
from common.util import login_required
from interfaces.identity_interface import IdentityInterface
from interfaces.processing_interface import ProcessingInterface
from var.messages import ERROR_FIELD_EMPTY
from var.network import STATUS_OK, STATUS_UNAUTHORIZED, STATUS_FORBIDDEN


class User(Resource):
    def __init__(self):
        self.identity_interface = IdentityInterface()
        self.processing_interface = ProcessingInterface()

    # получение информации о текущем пользователе
    @login_required
    def get(self, user_id=None):
        auth = {'username': session['username']}

        if user_id is None:
            result, message, user_info = self.identity_interface.get_info(auth)

            if result:
                return {'code': STATUS_OK, 'message': message, 'user_info': user_info}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        elif user_id == 'nearby':
            result, message, user_info = self.identity_interface.get_all_info()

            if result:
                return {'code': STATUS_OK, 'message': message, 'user_info': user_info}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        # Get info by id
        else:
            auth['id'] = user_id
            result, message, user_info = self.identity_interface.get_info_by_id(auth)

            if result:
                return {'code': STATUS_OK, 'message': message, 'user_info': user_info}, STATUS_OK
            else:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

    # создание нового пользователя
    def put(self, user_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)  # location='json'
        parser.add_argument('password', type=str)  # location='json'
        parser.add_argument('firstname', type=str)  # location='json'
        parser.add_argument('lastname', type=str)  # location='json'
        parser.add_argument('passport', type=int)  # location='json'
        parser.add_argument('residence', type=str)  # location='json'
        args = parser.parse_args()

        for field in args:
            if args[field] is None or len(str(args[field])) == 0:
                return {'code': STATUS_FORBIDDEN, 'message': ERROR_FIELD_EMPTY + field}, STATUS_FORBIDDEN

        auth = {'username': args.username,
                'password': args.password}
        passport = {'passport_number': args.passport,
                    'full_name': '{0} {1}'.format(args.firstname, args.lastname),
                    'residence': args.residence}
        identity = {'authentication': auth,
                    'passport': passport}

        result, message = self.identity_interface.set_info(identity)

        if result:
            result, message = self.processing_interface.create_account({'passport': passport['passport_number']})

            if result:
                session['username'] = args.username
                return {'code': STATUS_OK, 'message': message}, STATUS_OK

            else:
                return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

        else:
            return {'code': STATUS_UNAUTHORIZED, 'message': message}, STATUS_UNAUTHORIZED