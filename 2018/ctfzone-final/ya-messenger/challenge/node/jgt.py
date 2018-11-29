"""
JSON GRPC Tokens
"""

import json

from hashlib import sha512
from base64 import (b64encode, b64decode)

from . import bn256


class Key(object):
    def __init__(self, x, X, j, J, k, K):
        self.x = x
        self.X = X
        self.j = j
        self.J = J
        self.k = k
        self.K = K

    def serialize(self):
        return '.'.join([b64encode(i.to_bytes(32, byteorder='big')).decode()
                         for i in [self.x, self.j, self.k]])

    def serialize_public(self):
        return _serialize_x(self.X) + '.' \
            + '.'.join([_serialize(i)
                        for i in [self.J, self.K]])

    @classmethod
    def unserialize(cls, data):
        if data is None:
            raise ValueError('Empty token key')

        parts = data.split('.')

        if len(parts) != 3:
            raise ValueError('Invalid token key')

        x, j, k = [int.from_bytes(b64decode(i), byteorder='big')
                   for i in parts]

        X = bn256.g2_scalar_base_mult(x)
        J = bn256.g1_scalar_base_mult(j)
        K = bn256.g1_scalar_base_mult(k)

        return cls(x, X, j, J, k, K)


def genkey():
    k, K = bn256.g1_random()
    j, J = bn256.g1_random()
    x, X = bn256.g2_random()
    return Key(x, X, J, K)


def _hash(msg, J, K):
    h = sha512(msg).hexdigest()

    h1 = int(h[:64], 16)
    h2 = int(h[64:], 16)

    H1 = J.scalar_mul(h1)
    H2 = K.scalar_mul(h2)

    H = H1.add(H2)

    return H


def _serialize_x(X):
    return '.'.join([_serialize(i) for i in [X.x, X.y]])


def _serialize(P):
    if 'force_affine' in dir(P):
        P.force_affine()
    p1 = P.x.to_bytes()
    p2 = P.y.to_bytes()
    return '.'.join([b64encode(p1).decode(), b64encode(p2).decode()])


def _unserialize(p):
    pp = p.split('.')

    if len(pp) != 2:
        raise ValueError('Invalid format')

    try:
        p1 = int.from_bytes(b64decode(pp[0]), byteorder='big')
        p2 = int.from_bytes(b64decode(pp[1]), byteorder='big')
    except Exception:
        raise ValueError('Invalid encoding')

    return bn256.curve_point(bn256.gfp_1(p1),
                             bn256.gfp_1(p2))


def _sign(msg, key):
    H = _hash(msg, key.J, key.K)
    S = H.scalar_mul(key.x)
    return _serialize(S)


def _verify(msg, s, key):
    H = _hash(msg, key.J, key.K)
    S = _unserialize(s)

    p1 = bn256.optimal_ate(key.X, H)
    p2 = bn256.optimal_ate(bn256.twist_G, S)

    return p1 == p2


def encode(payload, key):
    data = json.dumps(payload).encode('utf-8')
    signature = _sign(data, key)
    return b64encode(data).decode() + '.' + signature


def decode(token, key, verify=True):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError('Invalid token format')

    data = b64decode(parts[0])

    if verify:
        signature = parts[1] + '.' + parts[2]
        if not _verify(data, signature, key):
            raise Exception('Invalid signature')

    return json.loads(data)
