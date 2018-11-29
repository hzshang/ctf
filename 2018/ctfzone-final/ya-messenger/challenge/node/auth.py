import grpc
import re

from ..common.logger import logger
from . import jgt


logger = logger.getChild('auth')


def _terminator(code, details):

    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class TokenAuthValidatorInterceptor(grpc.ServerInterceptor):

    def __init__(self, key, exclude=[]):
        self._key = key
        self._terminator = _terminator(grpc.StatusCode.UNAUTHENTICATED,
                                       'Unauthenticated request')
        self._exclude = exclude

    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method

        for pattern in self._exclude:
            if re.match(pattern, method):
                return continuation(handler_call_details)

        metadata = dict(handler_call_details.invocation_metadata)

        if 'auth' in metadata:
            token = metadata['auth']
            try:
                jgt.decode(token, self._key)
            except Exception:
                logger.debug('Auth failed for token="%s"' % token,
                             exc_info=True)
                return self._terminator

            return continuation(handler_call_details)

        return self._terminator
