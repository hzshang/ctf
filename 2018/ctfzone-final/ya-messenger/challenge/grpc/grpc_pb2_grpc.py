# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from challenge.grpc import grpc_pb2 as challenge_dot_grpc_dot_grpc__pb2


class NodeStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CheckHealth = channel.unary_unary(
        '/Node/CheckHealth',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestHealthCheck.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseHealthCheck.FromString,
        )
    self.Register = channel.unary_unary(
        '/Node/Register',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeRegister.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
        )
    self.Login = channel.unary_unary(
        '/Node/Login',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeLogin.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeLogin.FromString,
        )
    self.SendMessage = channel.unary_unary(
        '/Node/SendMessage',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeSendMessage.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
        )
    self.GetPublicKey = channel.unary_unary(
        '/Node/GetPublicKey',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetPublicKey.FromString,
        )
    self.GetUpdates = channel.unary_stream(
        '/Node/GetUpdates',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Event.FromString,
        )
    self.GetMessages = channel.unary_unary(
        '/Node/GetMessages',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeGetMessages.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetMessages.FromString,
        )
    self.GetMessage = channel.unary_unary(
        '/Node/GetMessage',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeGetMessage.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Message.FromString,
        )
    self.AddContact = channel.unary_unary(
        '/Node/AddContact',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeAddContact.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
        )
    self.GetContacts = channel.unary_unary(
        '/Node/GetContacts',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetContacts.FromString,
        )


class NodeServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CheckHealth(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Register(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Login(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPublicKey(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUpdates(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMessages(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddContact(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetContacts(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NodeServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CheckHealth': grpc.unary_unary_rpc_method_handler(
          servicer.CheckHealth,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestHealthCheck.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseHealthCheck.SerializeToString,
      ),
      'Register': grpc.unary_unary_rpc_method_handler(
          servicer.Register,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeRegister.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
      ),
      'Login': grpc.unary_unary_rpc_method_handler(
          servicer.Login,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeLogin.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeLogin.SerializeToString,
      ),
      'SendMessage': grpc.unary_unary_rpc_method_handler(
          servicer.SendMessage,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeSendMessage.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
      ),
      'GetPublicKey': grpc.unary_unary_rpc_method_handler(
          servicer.GetPublicKey,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetPublicKey.SerializeToString,
      ),
      'GetUpdates': grpc.unary_stream_rpc_method_handler(
          servicer.GetUpdates,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Event.SerializeToString,
      ),
      'GetMessages': grpc.unary_unary_rpc_method_handler(
          servicer.GetMessages,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeGetMessages.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetMessages.SerializeToString,
      ),
      'GetMessage': grpc.unary_unary_rpc_method_handler(
          servicer.GetMessage,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeGetMessage.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Message.SerializeToString,
      ),
      'AddContact': grpc.unary_unary_rpc_method_handler(
          servicer.AddContact,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestNodeAddContact.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
      ),
      'GetContacts': grpc.unary_unary_rpc_method_handler(
          servicer.GetContacts,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseNodeGetContacts.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Node', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class CloudStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CheckHealth = channel.unary_unary(
        '/Cloud/CheckHealth',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestHealthCheck.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseHealthCheck.FromString,
        )
    self.RegisterUser = channel.unary_unary(
        '/Cloud/RegisterUser',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudRegisterUser.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudRegisterUser.FromString,
        )
    self.GetUserPublicKey = channel.unary_unary(
        '/Cloud/GetUserPublicKey',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetUserPublicKey.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetUserPublicKey.FromString,
        )
    self.SendMessage = channel.unary_unary(
        '/Cloud/SendMessage',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudSendMessage.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudSendMessage.FromString,
        )
    self.UpdateMessageStatus = channel.unary_unary(
        '/Cloud/UpdateMessageStatus',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudUpdateMessageStatus.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
        )
    self.GetNodeUpdates = channel.unary_stream(
        '/Cloud/GetNodeUpdates',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Event.FromString,
        )
    self.GetMessages = channel.unary_unary(
        '/Cloud/GetMessages',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetMessages.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetMessages.FromString,
        )
    self.GetMessage = channel.unary_unary(
        '/Cloud/GetMessage',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetMessage.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.Message.FromString,
        )
    self.GetNodeUsers = channel.unary_unary(
        '/Cloud/GetNodeUsers',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetNodeUsers.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetNodeUsers.FromString,
        )
    self.GetUserDialogs = channel.unary_unary(
        '/Cloud/GetUserDialogs',
        request_serializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetUserDialogs.SerializeToString,
        response_deserializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetUserDialogs.FromString,
        )


class CloudServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CheckHealth(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RegisterUser(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUserPublicKey(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateMessageStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetNodeUpdates(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMessages(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetNodeUsers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUserDialogs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CloudServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CheckHealth': grpc.unary_unary_rpc_method_handler(
          servicer.CheckHealth,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestHealthCheck.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseHealthCheck.SerializeToString,
      ),
      'RegisterUser': grpc.unary_unary_rpc_method_handler(
          servicer.RegisterUser,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudRegisterUser.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudRegisterUser.SerializeToString,
      ),
      'GetUserPublicKey': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserPublicKey,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetUserPublicKey.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetUserPublicKey.SerializeToString,
      ),
      'SendMessage': grpc.unary_unary_rpc_method_handler(
          servicer.SendMessage,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudSendMessage.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudSendMessage.SerializeToString,
      ),
      'UpdateMessageStatus': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateMessageStatus,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudUpdateMessageStatus.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Empty.SerializeToString,
      ),
      'GetNodeUpdates': grpc.unary_stream_rpc_method_handler(
          servicer.GetNodeUpdates,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.Empty.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Event.SerializeToString,
      ),
      'GetMessages': grpc.unary_unary_rpc_method_handler(
          servicer.GetMessages,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetMessages.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetMessages.SerializeToString,
      ),
      'GetMessage': grpc.unary_unary_rpc_method_handler(
          servicer.GetMessage,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetMessage.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.Message.SerializeToString,
      ),
      'GetNodeUsers': grpc.unary_unary_rpc_method_handler(
          servicer.GetNodeUsers,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetNodeUsers.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetNodeUsers.SerializeToString,
      ),
      'GetUserDialogs': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserDialogs,
          request_deserializer=challenge_dot_grpc_dot_grpc__pb2.RequestCloudGetUserDialogs.FromString,
          response_serializer=challenge_dot_grpc_dot_grpc__pb2.ResponseCloudGetUserDialogs.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Cloud', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))