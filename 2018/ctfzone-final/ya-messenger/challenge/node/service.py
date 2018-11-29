import bcrypt
import queue
import threading
import peewee
import time

from datetime import (datetime, timedelta)
from playhouse.signals import (post_save, pre_save)

from ..grpc import (grpc_pb2_grpc, grpc_pb2)
from ..common.logger import logger
from ..common.queue import Queues
from ..common.exceptions import (InternalError, Unauthenticated,
                                 NotFound, InvalidCredentials,
                                 AccessDenied)
from . import (crypto, jgt)
from .models import (database,
                     User, Message, PublicKey, PrivateKey)
from .utils import handle_grpc_error


logger = logger.getChild('service')


def get_user_id(context):
    metadata = dict(context.invocation_metadata())
    payload = jgt.decode(metadata['auth'], None, verify=False)
    if 'user_id' in payload and payload['user_id'] != 0:
        return payload['user_id']
    raise Unauthenticated(context)


def update_message_status(cloud, message_id, status_name):
    try:
        req = grpc_pb2.RequestCloudUpdateMessageStatus()
        req.message_id = message_id
        req.status = grpc_pb2.MessageStatus.Value(status_name)

        cloud.UpdateMessageStatus(req)
    except Exception:
        logger.debug('Fail to update message id=%d status' %
                     message_id)


def process_event(cloud, event):
    event_type = event.WhichOneof('payload')

    logger.debug('New event: %s' % event_type)

    if event_type == 'event_message':
        msg = event.event_message.message

        user = User.get_or_none(
            User.cloud_id == msg.user_to.id)

        if user is None:
            update_message_status(cloud, msg.id, 'MISSING_USER')
            return

        sk = crypto.SecKey.load(p=user.private_key.p.tobytes(),
                                q=user.private_key.q.tobytes(),
                                d=user.private_key.d.tobytes())

        try:
            data = crypto.decrypt(msg.data, sk)
        except ValueError:
            update_message_status(cloud, msg.id, 'CORRUPTED')
            return
        except Exception:
            update_message_status(cloud, msg.id, 'ERROR')
            return

        message = Message.get_or_none(
            Message.cloud_id == msg.id)

        if message is None:
            message = Message()
            message.cloud_id = msg.id
            message.user_from_name = msg.user_from.name
            message.user_to_name = msg.user_to.name
            message.data = data

            message.status = grpc_pb2.MessageStatus.Value('DELIVERED')

            try:
                message.save()
            except Exception:
                logger.debug('Fail to save message with cloud_id=%s' % msg.id,
                             exc_info=True)
                update_message_status(cloud, msg.id, 'MISSING_MESSAGE')
                return

        update_message_status(cloud, msg.id, 'DELIVERED')

    elif event_type == 'event_message_status':
        logger.debug(event)

        message_id = event.event_message_status.message_id
        status = event.event_message_status.status

        message = Message.get_or_none(
            Message.cloud_id == message_id)

        if message is None:
            return

        if message.status == status:
            return

        message.status = status

        try:
            message.save()
        except Exception:
            logger.debug('Fail to save message with cloud_id=%s' % message_id,
                         exc_info=True)
            return


def get_updates(cloud):
    while True:
        logger.info('Start getting updates')
        try:
            events = cloud.GetNodeUpdates(grpc_pb2.Empty())
            for event in events:
                process_event(cloud, event)
        except Exception:
            logger.exception('Fail to get updates.')
            time.sleep(10)
            continue
        except KeyboardInterrupt:
            return


def on_message_pre_save(model_class, message, created):
    # Save changed fields
    message._dirty_fields = message.dirty_fields


def on_message_post_save(queues):
    def _inner(model_class, message, created):
        users = []
        event = None

        # Skip system
        if message.cloud_id is None:
            return

        if created:
            # New message
            event = grpc_pb2.EventMessage()
            event.message.id = message.id
            event.message.user_from.name = message.user_from_name
            event.message.user_to.name = message.user_to_name
            event.message.data = message.data
            event.message.status = message.status
            event.message.created_at = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

            # Event is for user to
            user = User.get_or_none(
                User.name == message.user_to_name)

            if user is None:
                return

            users.append(user.id)
        else:
            for field in message._dirty_fields:
                if field.name == 'status':
                    logger.debug('Update status of message')

                    # Message status updated
                    event = grpc_pb2.EventMessageStatus()
                    event.message_id = message.id
                    event.status = message.status

                    # Event is for user from
                    user_from = User.get_or_none(
                        User.name == message.user_from_name)

                    if user_from is not None:
                        users.append(user_from.id)

                    user_to = User.get_or_none(
                        User.name == message.user_to_name)

                    if user_to is not None:
                        users.append(user_to.id)

                    logger.debug('User from id=%r' % users)
                    break

        if event is not None and len(users) > 0:
            for user_id in users:
                logger.debug('Sending update to user %d' % user_id)
                for q in queues.all_for_entity(user_id):
                    q.put(event)

    return _inner


class NodeServicer(grpc_pb2_grpc.NodeServicer):
    def __init__(self, cloud_stub, token_key):
        self.cloud = cloud_stub
        self.token_key = token_key

        # Queues
        self.queues = Queues()

        pre_save.connect(on_message_pre_save,
                         sender=Message)
        post_save.connect(on_message_post_save(self.queues),
                          sender=Message)

    def CheckHealth(self, request, context):
        response = grpc_pb2.ResponseHealthCheck()
        response.status = grpc_pb2.ResponseHealthCheck.SERVING
        return response

    def Register(self, request, context):
        pk, sk = crypto.generate_keypair()

        try:
            public_key = grpc_pb2.PublicKey(**pk.export())

            req = grpc_pb2.RequestCloudRegisterUser()
            req.name = request.name
            req.public_key.CopyFrom(public_key)

            res = self.cloud.RegisterUser(req)
        except Exception as e:
            logger.debug('Fail to register user on cloud')
            handle_grpc_error(context, e)

        password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())

        private_key = PrivateKey(**sk.export())
        public_key = PublicKey(**pk.export())

        user = User()
        user.cloud_id = res.user_id
        user.name = request.name
        user.password = password
        user.private_key = private_key
        user.public_key = public_key

        try:
            with database.atomic():
                private_key.save()
                public_key.save()
                user.save()
        except Exception:
            logger.debug('Fail to save user: name=%s' % request.name)
            raise InternalError(context)

        response = grpc_pb2.Empty()

        return response

    def Login(self, request, context):
        user = User.get_or_none(User.name == request.name)

        if user is None:
            raise NotFound(context, 'User with name=%s' % request.name)

        if not bcrypt.checkpw(request.password.encode('utf-8'),
                              user.password.encode('utf-8')):
            raise InvalidCredentials(context)

        token = jgt.encode({'user_id': user.id}, self.token_key)

        response = grpc_pb2.ResponseNodeLogin()

        response.token = token

        return response

    def SendMessage(self, request, context):
        # Load current user id
        user_id = get_user_id(context)

        # Load current user
        user = User.get_or_none(
            User.id == user_id)

        if user is None:
            raise NotFound(context, 'User with id=%s' % user_id)

        # Get recipient's public key
        try:
            req = grpc_pb2.RequestCloudGetUserPublicKey()
            req.name = request.user_to_name

            res = self.cloud.GetUserPublicKey(req)
        except Exception as e:
            logger.debug('Fail to get user name=%s key from cloud' %
                         request.user_to_name)
            handle_grpc_error(context, e)

        pk = crypto.PubKey.load(res.public_key.e, res.public_key.n)

        try:
            encrypted_data = crypto.encrypt(request.data.encode('utf-8'), pk)
        except Exception:
            logger.debug('Fail to encrypt message', exc_info=True)
            raise InternalError(context)

        try:
            req = grpc_pb2.RequestCloudSendMessage()
            req.user_to_name = request.user_to_name
            req.user_from_name = user.name
            req.encrypted_data = encrypted_data

            res = self.cloud.SendMessage(req)
        except Exception as e:
            logger.debug('Fail to send message to cloud')
            handle_grpc_error(context, e)

        message = Message()
        message.cloud_id = res.message_id
        message.user_to_name = request.user_to_name
        message.user_from_name = user.name
        message.data = request.data.encode('utf-8')
        message.status = grpc_pb2.MessageStatus.Value('PENDING')

        try:
            message.save()
        except Exception:
            logger.debug('Fail to save message: cloud_id=%s' % res.message_id,
                         exc_info=True)

        response = grpc_pb2.Empty()

        return response

    def GetMessages(self, request, context):
        user_id = get_user_id(context)

        user = User.get_or_none(User.id == user_id)

        if user is None:
            raise NotFound(context, 'User with id=%d' % user_id)

        query = (Message
                 .select(Message)
                 .where(Message.cloud_id.is_null(False))
                 .where(((Message.user_to_name == request.user_name) &
                         (Message.user_from_name == user.name)) |
                        ((Message.user_to_name == user.name) &
                         (Message.user_from_name == request.user_name)))
                 .order_by(Message.cloud_id)
                 .namedtuples())

        messages = []
        for row in query:
            message = grpc_pb2.Message()
            message.id = row.cloud_id
            message.user_from.name = row.user_from_name
            message.user_to.name = row.user_to_name
            message.data = row.data.encode('utf-8')
            message.created_at = row.created_at.strftime('%Y-%m-%d %H:%M:%S')
            message.status = row.status
            messages.append(message)

        response = grpc_pb2.ResponseNodeGetMessages()

        response.messages.extend(messages)

        return response

    def GetMessage(self, request, context):
        user_id = get_user_id(context)

        user = User.get_or_none(User.id == user_id)

        if user is None:
            raise NotFound(context, 'User with id=%d' % user_id)

        message = Message.get_or_none(
            Message.cloud_id == request.message_id)

        if message is None:
            raise NotFound(context, 'Message with id=%d'
                           % request.message_id)

        if message.user_from_name != user.name and \
                message.user_to_name != user.name:
            raise AccessDenied(context)

        response = grpc_pb2.Message()

        response.id = message.cloud_id
        response.user_from.name = message.user_from_name
        response.user_to.name = message.user_to_name
        response.data = message.data.encode('utf-8')
        response.created_at = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        response.status = message.status

        return response

    def GetPublicKey(self, request, response):
        response = grpc_pb2.ResponseNodeGetPublicKey()

        response.key = self.token_key.serialize_public()

        return response

    def AddContact(self, request, context):
        user_id = get_user_id(context)

        user = User.get_or_none(User.id == user_id)

        if user is None:
            raise NotFound(context, 'User with id=%d' % user_id)

        # Check user name in cloud
        try:
            req = grpc_pb2.RequestCloudGetUserPublicKey()
            req.name = request.user_name

            self.cloud.GetUserPublicKey(req)
        except Exception as e:
            logger.debug('Fail to get user name=%s from cloud' %
                         request.user_name)
            handle_grpc_error(context, e)

        # Create system message
        message = Message()
        message.user_to_name = request.user_name
        message.user_from_name = user.name
        message.data = ''
        message.status = 0

        try:
            message.save()
        except Exception:
            logger.debug('Fail to save message', exc_info=True)

        response = grpc_pb2.Empty()

        return response

    def GetContacts(self, request, context):
        user_id = get_user_id(context)

        user = User.get_or_none(User.id == user_id)

        if user is None:
            raise NotFound(context, 'User with id=%d' % user_id)

        contacts = set()

        subq = (Message
                .select(Message.user_to_name.alias('name'),
                        Message.created_at.alias('created_at'))
                .where((Message.user_from_name == user.name) |
                       (Message.user_to_name == user.name))
                .distinct())

        subq = subq.union(Message
                          .select(Message.user_from_name.alias('name'),
                                  Message.created_at.alias('created_at'))
                          .where((Message.user_from_name == user.name) |
                                 (Message.user_to_name == user.name))
                          .distinct())

        query = (Message
                 .select(peewee.SQL('name'))
                 .from_(subq)
                 .order_by(peewee.SQL('created_at').desc()))

        for row in query:
            contacts.add(row.name)

        if len(contacts) == 0:
            contacts.add(user.name)

        response = grpc_pb2.ResponseNodeGetContacts()

        response.user_names.extend(list(contacts))

        return response

    def GetUpdates(self, request, context):
        user_id = get_user_id(context)
        peer = context.peer()

        logger.info(f'User {user_id} connected from {peer}')

        stop = threading.Event()

        def on_disconnect(stop):
            def _inner():
                stop.set()
                logger.info(f'User {user_id} {peer} disconnected')
                self.queues.delete(user_id, peer)
            return _inner

        context.add_callback(on_disconnect(stop))

        q = self.queues.get(user_id, peer)

        while True:
            try:
                if stop.is_set():
                    return

                event = q.get(timeout=1)
                response = grpc_pb2.Event()
                if isinstance(event, grpc_pb2.EventMessage):
                    response.event_message.CopyFrom(event)
                elif isinstance(event, grpc_pb2.EventMessageStatus):
                    response.event_message_status.CopyFrom(event)
                logger.debug('Sending new event to user id=%d %s'
                             % (user_id, peer))
                yield response
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                return
