from dataclasses import dataclass
import itertools
import gmpy2
import hashlib
import math
import os

from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.backends import default_backend


_hash_func = hashlib.sha1
_h_len = _hash_func().digest_size
backend = default_backend()


def os2ip(x):
    if not x:
        return 0
    n = x[-1]
    t = 1
    for x in x[-2::-1]:
        t *= 256
        n += x * t
    return n


def i2osp(x, l):
    if x >= pow(256, l):
        raise ValueError('Number too long')
    return bytes([(x >> (8 * i)) & 0xFF for i in range(l - 1, -1, -1)])


def int2bytes(n):
    ln = n.bit_length()

    if ln % 8 == 0:
        return i2osp(n, ln // 8)

    return i2osp(n, ln // 8 + 1)


@dataclass
class PubKey(object):
    e: int
    n: int

    def export(self):
        return {
            'e': self.e,
            'n': int2bytes(self.n),
        }

    @classmethod
    def load(cls, e, n):
        return cls(e=e, n=os2ip(n))


@dataclass
class SecKey(object):
    d: int
    p: int
    q: int

    @property
    def n(self):
        return self.p * self.q

    def export(self):
        return {
            'd': int2bytes(self.d),
            'p': int2bytes(self.p),
            'q': int2bytes(self.q),
        }

    @classmethod
    def load(cls, d, p, q):
        return cls(d=os2ip(d), p=os2ip(p), q=os2ip(q))


def random_prime(size):
    seed = int.from_bytes(os.urandom(16), byteorder='little')
    state = gmpy2.random_state(seed)
    rnd = gmpy2.mpz_rrandomb(state, size)
    while True:
        prime = gmpy2.next_prime(rnd)
        if prime.bit_length() == size:
            return prime


def generate_keypair(size=1024, e=65537):
    p = random_prime(size >> 1)
    q = gmpy2.next_prime(p)

    try:
        d = gmpy2.invert(e, (p - 1) * (q - 1))
    except ZeroDivisionError as e:
        return generate_keypair(size, e)

    n = p * q

    if n.bit_length() != size:
        return generate_keypair(size, e)

    pk = PubKey(e, n)
    sk = SecKey(d, p, q)
    return (pk, sk)


def hash_digest(m):
    return _hash_func(m).digest()


def mgf(Z, l):
    if l > pow(2, 32) * _h_len:
        raise Exception('Mask too long')
    T = bytes()
    for counter in range(math.ceil(l / _h_len)):
        C = i2osp(counter, 4)
        T += hash_digest(Z + C)
    return T[:l]


def xor(a, b):
    if b > a:
        a, b = b, a
    return bytes([x ^ y for x, y in zip(a, itertools.cycle(b))])


def encode(m, em_len=None, P=b''):
    m_len = len(m)

    if not em_len:
        em_len = 128

    if len(P) >= pow(2, 61) - 1:
        raise Exception('Parameter string too long')

    if m_len > em_len - 2 * _h_len - 1:
        raise Exception('Message too long')

    ps = b'\x00' * (em_len - m_len - 2 * _h_len - 1)
    p_hash = hash_digest(P)

    db = p_hash + ps + b'\x01' + m

    seed = os.urandom(_h_len)
    db_mask = mgf(seed, em_len - _h_len)
    masked_db = xor(db, db_mask)

    seed_mask = mgf(masked_db, _h_len)
    masked_seed = xor(seed, seed_mask)

    em = masked_seed + masked_db
    return em


def decode(em, P=b''):
    em_len = len(em)
    p_hash = hash_digest(P)

    if len(P) >= pow(2, 61) - 1:
        raise Exception('Parameter string too long')

    if em_len < 2 * _h_len + 1:
        raise Exception('Decoding error')

    masked_seed = em[:_h_len]
    masked_db = em[_h_len:]

    seed_mask = mgf(masked_db, _h_len)
    seed = xor(masked_seed, seed_mask)

    db_mask = mgf(seed, em_len - _h_len)
    db = xor(masked_db, db_mask)
    _p_hash = db[:_h_len]

    if _p_hash != p_hash:
        raise Exception('Decoding error')

    if b'\x01' not in db:
        raise Exception('Decoding error')

    index = db.index(0x01)
    return db[index + 1:]


def _encrypt(m, pk):
    k = pk.n.bit_length() // 8
    em = encode(m, k - 1)
    m = os2ip(em)
    if m < 0 or m > pk.n - 1:
        raise Exception('Message out of range')
    c = gmpy2.powmod(m, pk.e, pk.n)
    return i2osp(c, k)


def encrypt(m, pk):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv),
                    backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(m) + encryptor.finalize()
    enc_key = _encrypt(key, pk)
    return enc_key + iv + ct


def _decrypt(c, sk):
    k = sk.n.bit_length() // 8
    c = os2ip(c)
    em = gmpy2.powmod(c, sk.d, sk.n)
    em = i2osp(em, k - 1)
    return decode(em)


def decrypt(c, sk):
    sk_len = sk.n.bit_length() // 8
    if len(c) < sk_len + 16:
        raise Exception('Ciphertext is too short')
    enc_key = c[:sk_len]
    iv = c[sk_len:sk_len+16]
    ct = c[sk_len+16:]
    key = _decrypt(enc_key, sk)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv),
                    backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()
