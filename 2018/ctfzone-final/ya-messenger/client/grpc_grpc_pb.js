// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var challenge_grpc_grpc_pb = require('./grpc_pb.js');

function serialize_Empty(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.Empty)) {
    throw new Error('Expected argument of type Empty');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_Empty(buffer_arg) {
  return challenge_grpc_grpc_pb.Empty.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Event(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.Event)) {
    throw new Error('Expected argument of type Event');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_Event(buffer_arg) {
  return challenge_grpc_grpc_pb.Event.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_Message(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.Message)) {
    throw new Error('Expected argument of type Message');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_Message(buffer_arg) {
  return challenge_grpc_grpc_pb.Message.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudGetMessage(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudGetMessage)) {
    throw new Error('Expected argument of type RequestCloudGetMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudGetMessage(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudGetMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudGetMessages(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudGetMessages)) {
    throw new Error('Expected argument of type RequestCloudGetMessages');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudGetMessages(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudGetMessages.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudGetNodeUsers(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudGetNodeUsers)) {
    throw new Error('Expected argument of type RequestCloudGetNodeUsers');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudGetNodeUsers(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudGetNodeUsers.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudGetUserDialogs(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudGetUserDialogs)) {
    throw new Error('Expected argument of type RequestCloudGetUserDialogs');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudGetUserDialogs(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudGetUserDialogs.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudGetUserPublicKey(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudGetUserPublicKey)) {
    throw new Error('Expected argument of type RequestCloudGetUserPublicKey');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudGetUserPublicKey(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudGetUserPublicKey.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudRegisterUser(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudRegisterUser)) {
    throw new Error('Expected argument of type RequestCloudRegisterUser');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudRegisterUser(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudRegisterUser.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudSendMessage(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudSendMessage)) {
    throw new Error('Expected argument of type RequestCloudSendMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudSendMessage(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudSendMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestCloudUpdateMessageStatus(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestCloudUpdateMessageStatus)) {
    throw new Error('Expected argument of type RequestCloudUpdateMessageStatus');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestCloudUpdateMessageStatus(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestCloudUpdateMessageStatus.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestHealthCheck(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestHealthCheck)) {
    throw new Error('Expected argument of type RequestHealthCheck');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestHealthCheck(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestHealthCheck.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeAddContact(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeAddContact)) {
    throw new Error('Expected argument of type RequestNodeAddContact');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeAddContact(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeAddContact.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeGetMessage(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeGetMessage)) {
    throw new Error('Expected argument of type RequestNodeGetMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeGetMessage(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeGetMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeGetMessages(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeGetMessages)) {
    throw new Error('Expected argument of type RequestNodeGetMessages');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeGetMessages(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeGetMessages.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeLogin(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeLogin)) {
    throw new Error('Expected argument of type RequestNodeLogin');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeLogin(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeLogin.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeRegister(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeRegister)) {
    throw new Error('Expected argument of type RequestNodeRegister');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeRegister(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeRegister.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_RequestNodeSendMessage(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.RequestNodeSendMessage)) {
    throw new Error('Expected argument of type RequestNodeSendMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_RequestNodeSendMessage(buffer_arg) {
  return challenge_grpc_grpc_pb.RequestNodeSendMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudGetMessages(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudGetMessages)) {
    throw new Error('Expected argument of type ResponseCloudGetMessages');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudGetMessages(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudGetMessages.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudGetNodeUsers(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudGetNodeUsers)) {
    throw new Error('Expected argument of type ResponseCloudGetNodeUsers');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudGetNodeUsers(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudGetNodeUsers.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudGetUserDialogs(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudGetUserDialogs)) {
    throw new Error('Expected argument of type ResponseCloudGetUserDialogs');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudGetUserDialogs(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudGetUserDialogs.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudGetUserPublicKey(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudGetUserPublicKey)) {
    throw new Error('Expected argument of type ResponseCloudGetUserPublicKey');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudGetUserPublicKey(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudGetUserPublicKey.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudRegisterUser(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudRegisterUser)) {
    throw new Error('Expected argument of type ResponseCloudRegisterUser');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudRegisterUser(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudRegisterUser.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseCloudSendMessage(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseCloudSendMessage)) {
    throw new Error('Expected argument of type ResponseCloudSendMessage');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseCloudSendMessage(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseCloudSendMessage.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseHealthCheck(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseHealthCheck)) {
    throw new Error('Expected argument of type ResponseHealthCheck');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseHealthCheck(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseHealthCheck.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseNodeGetContacts(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseNodeGetContacts)) {
    throw new Error('Expected argument of type ResponseNodeGetContacts');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseNodeGetContacts(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseNodeGetContacts.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseNodeGetMessages(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseNodeGetMessages)) {
    throw new Error('Expected argument of type ResponseNodeGetMessages');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseNodeGetMessages(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseNodeGetMessages.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseNodeGetPublicKey(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseNodeGetPublicKey)) {
    throw new Error('Expected argument of type ResponseNodeGetPublicKey');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseNodeGetPublicKey(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseNodeGetPublicKey.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_ResponseNodeLogin(arg) {
  if (!(arg instanceof challenge_grpc_grpc_pb.ResponseNodeLogin)) {
    throw new Error('Expected argument of type ResponseNodeLogin');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_ResponseNodeLogin(buffer_arg) {
  return challenge_grpc_grpc_pb.ResponseNodeLogin.deserializeBinary(new Uint8Array(buffer_arg));
}


var NodeService = exports.NodeService = {
  checkHealth: {
    path: '/Node/CheckHealth',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestHealthCheck,
    responseType: challenge_grpc_grpc_pb.ResponseHealthCheck,
    requestSerialize: serialize_RequestHealthCheck,
    requestDeserialize: deserialize_RequestHealthCheck,
    responseSerialize: serialize_ResponseHealthCheck,
    responseDeserialize: deserialize_ResponseHealthCheck,
  },
  register: {
    path: '/Node/Register',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeRegister,
    responseType: challenge_grpc_grpc_pb.Empty,
    requestSerialize: serialize_RequestNodeRegister,
    requestDeserialize: deserialize_RequestNodeRegister,
    responseSerialize: serialize_Empty,
    responseDeserialize: deserialize_Empty,
  },
  login: {
    path: '/Node/Login',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeLogin,
    responseType: challenge_grpc_grpc_pb.ResponseNodeLogin,
    requestSerialize: serialize_RequestNodeLogin,
    requestDeserialize: deserialize_RequestNodeLogin,
    responseSerialize: serialize_ResponseNodeLogin,
    responseDeserialize: deserialize_ResponseNodeLogin,
  },
  sendMessage: {
    path: '/Node/SendMessage',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeSendMessage,
    responseType: challenge_grpc_grpc_pb.Empty,
    requestSerialize: serialize_RequestNodeSendMessage,
    requestDeserialize: deserialize_RequestNodeSendMessage,
    responseSerialize: serialize_Empty,
    responseDeserialize: deserialize_Empty,
  },
  getPublicKey: {
    path: '/Node/GetPublicKey',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.Empty,
    responseType: challenge_grpc_grpc_pb.ResponseNodeGetPublicKey,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_ResponseNodeGetPublicKey,
    responseDeserialize: deserialize_ResponseNodeGetPublicKey,
  },
  getUpdates: {
    path: '/Node/GetUpdates',
    requestStream: false,
    responseStream: true,
    requestType: challenge_grpc_grpc_pb.Empty,
    responseType: challenge_grpc_grpc_pb.Event,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Event,
    responseDeserialize: deserialize_Event,
  },
  getMessages: {
    path: '/Node/GetMessages',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeGetMessages,
    responseType: challenge_grpc_grpc_pb.ResponseNodeGetMessages,
    requestSerialize: serialize_RequestNodeGetMessages,
    requestDeserialize: deserialize_RequestNodeGetMessages,
    responseSerialize: serialize_ResponseNodeGetMessages,
    responseDeserialize: deserialize_ResponseNodeGetMessages,
  },
  getMessage: {
    path: '/Node/GetMessage',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeGetMessage,
    responseType: challenge_grpc_grpc_pb.Message,
    requestSerialize: serialize_RequestNodeGetMessage,
    requestDeserialize: deserialize_RequestNodeGetMessage,
    responseSerialize: serialize_Message,
    responseDeserialize: deserialize_Message,
  },
  addContact: {
    path: '/Node/AddContact',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestNodeAddContact,
    responseType: challenge_grpc_grpc_pb.Empty,
    requestSerialize: serialize_RequestNodeAddContact,
    requestDeserialize: deserialize_RequestNodeAddContact,
    responseSerialize: serialize_Empty,
    responseDeserialize: deserialize_Empty,
  },
  getContacts: {
    path: '/Node/GetContacts',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.Empty,
    responseType: challenge_grpc_grpc_pb.ResponseNodeGetContacts,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_ResponseNodeGetContacts,
    responseDeserialize: deserialize_ResponseNodeGetContacts,
  },
};

exports.NodeClient = grpc.makeGenericClientConstructor(NodeService);
var CloudService = exports.CloudService = {
  checkHealth: {
    path: '/Cloud/CheckHealth',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestHealthCheck,
    responseType: challenge_grpc_grpc_pb.ResponseHealthCheck,
    requestSerialize: serialize_RequestHealthCheck,
    requestDeserialize: deserialize_RequestHealthCheck,
    responseSerialize: serialize_ResponseHealthCheck,
    responseDeserialize: deserialize_ResponseHealthCheck,
  },
  registerUser: {
    path: '/Cloud/RegisterUser',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudRegisterUser,
    responseType: challenge_grpc_grpc_pb.ResponseCloudRegisterUser,
    requestSerialize: serialize_RequestCloudRegisterUser,
    requestDeserialize: deserialize_RequestCloudRegisterUser,
    responseSerialize: serialize_ResponseCloudRegisterUser,
    responseDeserialize: deserialize_ResponseCloudRegisterUser,
  },
  getUserPublicKey: {
    path: '/Cloud/GetUserPublicKey',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudGetUserPublicKey,
    responseType: challenge_grpc_grpc_pb.ResponseCloudGetUserPublicKey,
    requestSerialize: serialize_RequestCloudGetUserPublicKey,
    requestDeserialize: deserialize_RequestCloudGetUserPublicKey,
    responseSerialize: serialize_ResponseCloudGetUserPublicKey,
    responseDeserialize: deserialize_ResponseCloudGetUserPublicKey,
  },
  sendMessage: {
    path: '/Cloud/SendMessage',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudSendMessage,
    responseType: challenge_grpc_grpc_pb.ResponseCloudSendMessage,
    requestSerialize: serialize_RequestCloudSendMessage,
    requestDeserialize: deserialize_RequestCloudSendMessage,
    responseSerialize: serialize_ResponseCloudSendMessage,
    responseDeserialize: deserialize_ResponseCloudSendMessage,
  },
  updateMessageStatus: {
    path: '/Cloud/UpdateMessageStatus',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudUpdateMessageStatus,
    responseType: challenge_grpc_grpc_pb.Empty,
    requestSerialize: serialize_RequestCloudUpdateMessageStatus,
    requestDeserialize: deserialize_RequestCloudUpdateMessageStatus,
    responseSerialize: serialize_Empty,
    responseDeserialize: deserialize_Empty,
  },
  getNodeUpdates: {
    path: '/Cloud/GetNodeUpdates',
    requestStream: false,
    responseStream: true,
    requestType: challenge_grpc_grpc_pb.Empty,
    responseType: challenge_grpc_grpc_pb.Event,
    requestSerialize: serialize_Empty,
    requestDeserialize: deserialize_Empty,
    responseSerialize: serialize_Event,
    responseDeserialize: deserialize_Event,
  },
  getMessages: {
    path: '/Cloud/GetMessages',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudGetMessages,
    responseType: challenge_grpc_grpc_pb.ResponseCloudGetMessages,
    requestSerialize: serialize_RequestCloudGetMessages,
    requestDeserialize: deserialize_RequestCloudGetMessages,
    responseSerialize: serialize_ResponseCloudGetMessages,
    responseDeserialize: deserialize_ResponseCloudGetMessages,
  },
  getMessage: {
    path: '/Cloud/GetMessage',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudGetMessage,
    responseType: challenge_grpc_grpc_pb.Message,
    requestSerialize: serialize_RequestCloudGetMessage,
    requestDeserialize: deserialize_RequestCloudGetMessage,
    responseSerialize: serialize_Message,
    responseDeserialize: deserialize_Message,
  },
  getNodeUsers: {
    path: '/Cloud/GetNodeUsers',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudGetNodeUsers,
    responseType: challenge_grpc_grpc_pb.ResponseCloudGetNodeUsers,
    requestSerialize: serialize_RequestCloudGetNodeUsers,
    requestDeserialize: deserialize_RequestCloudGetNodeUsers,
    responseSerialize: serialize_ResponseCloudGetNodeUsers,
    responseDeserialize: deserialize_ResponseCloudGetNodeUsers,
  },
  getUserDialogs: {
    path: '/Cloud/GetUserDialogs',
    requestStream: false,
    responseStream: false,
    requestType: challenge_grpc_grpc_pb.RequestCloudGetUserDialogs,
    responseType: challenge_grpc_grpc_pb.ResponseCloudGetUserDialogs,
    requestSerialize: serialize_RequestCloudGetUserDialogs,
    requestDeserialize: deserialize_RequestCloudGetUserDialogs,
    responseSerialize: serialize_ResponseCloudGetUserDialogs,
    responseDeserialize: deserialize_ResponseCloudGetUserDialogs,
  },
};

exports.CloudClient = grpc.makeGenericClientConstructor(CloudService);
