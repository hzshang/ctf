import colorlog
import logging
import sys
import os


handler = colorlog.StreamHandler(sys.stdout)
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s]%(reset)s %(white)s[%(asctime)s]%(reset)s %(purple)s[%(name)s]%(reset)s %(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'black,bold',
        'INFO':     'blue,bold',
        'WARNING':  'yellow,bold',
        'ERROR':    'red,bold',
        'CRITICAL': 'white,bold,bg_red',
    },
    secondary_log_colors={},
    style='%',
))

loglevel = logging.DEBUG if os.environ.get('DEBUG') == '1' else logging.INFO

logger = colorlog.getLogger('app')
logger.propagate = False
logger.setLevel(loglevel)
logger.addHandler(handler)

if os.environ.get('DEBUG_DATABASE'):
    peewee = logging.getLogger('peewee')
    peewee.setLevel(loglevel)
    peewee.addHandler(handler)
