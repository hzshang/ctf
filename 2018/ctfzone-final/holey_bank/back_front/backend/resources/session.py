from flask import session
from flask_restful import Resource, reqparse
from common.util import login_required
from interfaces.identity_interface import IdentityInterface
from interfaces.processing_interface import ProcessingInterface
from var.messages import ERROR_EMPTY_LOGIN_OR_PASS, ERROR_OK, ERROR_FIELD_EMPTY
from var.network import STATUS_OK, STATUS_UNAUTHORIZED, STATUS_FORBIDDEN


class Session(Resource):

    def __init__(self):
        self.identity_interface = IdentityInterface()
        self.processing_interface = ProcessingInterface()

    # login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='This field cannot be empty')  # location='json'
        parser.add_argument('password', type=str, help='This field cannot be empty')  # location='json'
        args = parser.parse_args()

        if args.username is None or len(args.username) == 0 or args.password is None or len(args.password) == 0:
            return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_EMPTY_LOGIN_OR_PASS}, STATUS_UNAUTHORIZED

        result, message = self.identity_interface.login(args)

        if result:
            # check if user has passport
            passport, message = self._get_passport_by_username(args.username)
            if passport is None:
                return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

            # check if user has account
            result, message, data = self.processing_interface.get_info({'passport': passport})
            # if he hasn't
            if result:
                session['username'] = args.username
                return {'code': STATUS_OK, 'message': message}, STATUS_OK

            else:
                # try to create account
                result, message = self.processing_interface.create_account({'passport': passport})

                # if created, authenticate user
                if result:
                    session['username'] = args.username
                    return {'code': STATUS_OK, 'message': message}, STATUS_OK

                else:
                    return {'code': STATUS_FORBIDDEN, 'message': message}, STATUS_FORBIDDEN

        else:
            return {'code': STATUS_UNAUTHORIZED, 'message': message}, STATUS_UNAUTHORIZED

    # logout
    @login_required
    def delete(self):
        session.clear()
        return {'code': STATUS_OK, 'message': ERROR_OK}, STATUS_OK

    # Get passport number by username
    def _get_passport_by_username(self, username=None):
        if username is None:
            auth = {'username': session['username']}
        else:
            auth = {'username': username}
        result, message, user_info = self.identity_interface.get_info(auth)
        if result:
            if len(str(user_info['passport_number'])) > 0:
                return int(user_info['passport_number']), message
            else:
                return None, ERROR_FIELD_EMPTY + 'passport_number'
        else:
            return None, message