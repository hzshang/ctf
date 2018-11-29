from functools import wraps
from flask import session
from var.messages import ERROR_UNAUTHORIZED
from var.network import STATUS_UNAUTHORIZED


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print(session)
        # print(session.get('username'))
        if not session.get('username'):
            return {'code': STATUS_UNAUTHORIZED, 'message': ERROR_UNAUTHORIZED}, STATUS_UNAUTHORIZED
        return f(*args, **kwargs)

    return decorated_function
