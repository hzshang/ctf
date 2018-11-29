from datetime import (date, datetime)
from base64 import b64encode


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return b64encode(obj).decode()
    raise TypeError('Type %s not serializable' % type(obj))
