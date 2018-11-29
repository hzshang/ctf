import grpc

from ..common.exceptions import (DuplicateEntity, NotFound,
                                 InternalError, Unavailable)


def handle_grpc_error(context, e):
    if isinstance(e, grpc.RpcError):
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise DuplicateEntity(context, e.details())
        elif e.code() == grpc.StatusCode.NOT_FOUND:
            raise NotFound(context, e.details(), tail=False)
        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            raise Unavailable(context)
    raise InternalError(context)
