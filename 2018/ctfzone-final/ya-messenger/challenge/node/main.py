import os
import grpc
import time

from concurrent import futures
from threading import Thread

from ..grpc import (grpc_pb2_grpc, grpc_pb2)
from ..common.logger import logger
from . import jgt
from .auth import TokenAuthValidatorInterceptor
from .service import (NodeServicer, get_updates)
from .models import models_init


logger = logger.getChild('main')


def check_cloud(cloud_stub):
    req = grpc_pb2.RequestHealthCheck()
    res = cloud_stub.CheckHealth(req, timeout=15)
    if res.status != grpc_pb2.ResponseHealthCheck.SERVING:
        raise Exception('Fail to connect to the cloud')


def main(**args):
    # Init database
    models_init(os.environ.get('NODE_DATABASE') or 'sqlite:///node.db')

    token_key = jgt.Key.unserialize(os.environ.get('NODE_AUTH_SECRET'))

    auth_validator = TokenAuthValidatorInterceptor(
        token_key,
        exclude=['/Node/Login',
                 '/Node/Register',
                 '/Node/CheckHealth',
                 '/Node/GetPublicKey'])

    # Init server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=(auth_validator,))

    # Connect to the cloud
    channel = grpc.insecure_channel(os.environ.get('NODE_CLOUD_ADDR')
                                    or ':31337')
    cloud_stub = grpc_pb2_grpc.CloudStub(channel)

    grpc_pb2_grpc.add_NodeServicer_to_server(
        NodeServicer(cloud_stub, token_key),
        server)
    port = os.environ.get('NODE_PORT') or '31338'
    server.add_insecure_port('0.0.0.0:%s' % port)

    server.start()
    logger.info('Started server on :%s' % port)

    updates_thread = Thread(
        target=get_updates, args=(cloud_stub, ))
    updates_thread.start()

    while True:
        try:
            logger.debug('Start checking cloud...')
            check_cloud(cloud_stub)
            logger.debug('Cloud is OK')
            logger.debug('Updates alive: %r' % updates_thread.is_alive())
            time.sleep(30)
        except Exception:
            logger.exception('Fail to connect to the cloud')
