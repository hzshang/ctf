import grpc


class GrpcException(Exception):
    def __init__(self, message, context, code):
        super().__init__(message)
        context.set_code(code)
        context.set_details(message)


class NotFound(GrpcException):
    def __init__(self, context, desc, tail=True):
        message = f'{desc} not found' if tail else desc
        super().__init__(message, context,
                         grpc.StatusCode.NOT_FOUND)


class DuplicateEntity(GrpcException):
    def __init__(self, context, message):
        super().__init__(message, context,
                         grpc.StatusCode.ALREADY_EXISTS)


class InternalError(GrpcException):
    def __init__(self, context):
        super().__init__('Internal error', context,
                         grpc.StatusCode.INTERNAL)


class InvalidCredentials(GrpcException):
    def __init__(self, context):
        super().__init__('Invalid credentials', context,
                         grpc.StatusCode.UNAUTHENTICATED)


class Unauthenticated(GrpcException):
    def __init__(self, context):
        super().__init__('Unauthenticated request', context,
                         grpc.StatusCode.UNAUTHENTICATED)


class AccessDenied(GrpcException):
    def __init__(self, context):
        super().__init__('Access denied', context,
                         grpc.StatusCode.CANCELLED)


class Unavailable(GrpcException):
    def __init__(self, context):
        super().__init__('Unavailable', context,
                         grpc.StatusCode.UNAVAILABLE)


class ValidationError(GrpcException):
    def __init__(self, context, message):
        super().__init__(message, context,
                         grpc.StatusCode.INVALID_ARGUMENT)
