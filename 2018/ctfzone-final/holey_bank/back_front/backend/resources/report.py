from flask import request, session, make_response
from flask_restful import Resource
from common.util import login_required
from interfaces.identity_interface import IdentityInterface
from interfaces.reporting_interface import ReportingInterface
from interfaces.processing_interface import ProcessingInterface
from var.messages import ERROR_FIELD_EMPTY, ERROR_UNAUTHORIZED
from var.network import STATUS_UNAUTHORIZED, STATUS_FORBIDDEN


class Report(Resource):

    def __init__(self):
        self.identity_interface = IdentityInterface()
        self.reporting_interface = ReportingInterface()
        self.processing_interface = ProcessingInterface()

    # generate report
    @login_required
    def get(self):
        passport, message = self._get_passport_by_username()
        if passport is None:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'user_info': {}}, STATUS_FORBIDDEN

        args = dict(request.args)
        for key, value in args.items():
            if isinstance(value, list):
                args[key] = args[key][0]

        result, message, data = self.processing_interface.get_info({'passport': passport})
        if not result:
            return {'code': STATUS_FORBIDDEN, 'message': message, 'data': {}}, STATUS_FORBIDDEN

        # If no card, use account as id
        if 'Card' not in args or args['Card'] is None or len(args['Card']) == 0:
            args['Card'] = data['account']['id']

        # If has card, check if user is owner of this card
        else:
            has_card = False
            for db_card in data['cards']:
                if str(db_card['id']) == str(args['Card']):
                    has_card = True
                    break
            if not has_card:
                return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_UNAUTHORIZED}, STATUS_UNAUTHORIZED

        if 'Theme' not in args or args['Theme'] is None or len(args['Theme']) == 0:
            args['Theme'] = 'dark'

        args['Username'] = session['username']

        result, message, data = self.reporting_interface.generate(args)

        if result:
            response = make_response(data)
            response.headers['expires'] = '0'
            response.headers['cache-control'] = 'must-revalidate, post-check=0, pre-check=0'
            response.headers['content-type'] = 'application/pdf'
            response.headers['content-disposition'] = 'attachment; filename=report.pdf'
            return response
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