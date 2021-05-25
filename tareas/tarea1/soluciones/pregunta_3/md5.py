import numpy as np
from copy import deepcopy
from numpy import logical_and as band, logical_or as bor, logical_xor as bxor, logical_not as bnot, roll as shift


def splitstring(s, n):  # divide un iterable en chunks de largo n
  return [s[i:i+n] for i in range(0, len(s), n)]


def b2i(a):  # bin to int
  return a.dot(2**np.arange(a.size)[::-1])


def bsum(a, b):  # suma binaria
    aux = (b2i(a) + b2i(b))%(2**32)
    return np.array(list(bin(aux)[2:].zfill(32)), dtype=np.int)


def leftrotate(x, c):
  return bor(shift(x, -c), shift(x, 32-c))


def md5(message, h0 = 137269462086865085541390238039692956790): # https://en.wikipedia.org/wiki/MD5
    # obtener el mensaje en bits
    mensaje_bits = ''.join([str(bin(b))[2:].zfill(8) for b in  bytearray(message, "utf8")])
    # obtenemos el largo
    largo  = len(mensaje_bits)
    largo_bits = ''.join([str(bin(b))[2:].zfill(8) for b in (len(mensaje_bits)).to_bytes(8, byteorder='little')])
    # agregamos el bit 1 y los 0's de padding
    mensaje_bits += '1'
    zeros =  (512 + (448 - len(mensaje_bits)%512)) % 512
    mensaje_bits += '0'*zeros
    if len(mensaje_bits) % 512 != 448:
        print('wrong number error')
        return
    mensaje_bits += largo_bits

    # definimos s y k
    s =  [7, 12, 17, 22,  7, 12, 17, 22]
    s += [7, 12, 17, 22,  7, 12, 17, 22]
    s += [5,  9, 14, 20,  5,  9, 14, 20]
    s += [5,  9, 14, 20,  5,  9, 14, 20]
    s += [4, 11, 16, 23,  4, 11, 16, 23]
    s += [4, 11, 16, 23,  4, 11, 16, 23]
    s += [6, 10, 15, 21,  6, 10, 15, 21]
    s += [6, 10, 15, 21,  6, 10, 15, 21]

    k = [int(np.floor(np.abs(np.sin(i + 1)) * np.power(2, 32))) for i in range(64)]
    k = [np.array(list(bin(int(i))[2:].zfill(32)), dtype=np.int) for i in k]

    # establecemos los estados iniciales desde h0
    a0 = (h0 // 2 ** (32 * 3)) % (2 ** 32)
    b0 = (h0 // (2 ** (32 * 2))) % (2 ** 32)
    c0 = (h0 // (2 ** 32)) % (2 ** 32)
    d0 = h0 % (2 ** 32)

    a0 = np.array(list(bin(a0)[2:].zfill(32)), dtype=np.int)
    b0 = np.array(list(bin(b0)[2:].zfill(32)), dtype=np.int)
    c0 = np.array(list(bin(c0)[2:].zfill(32)), dtype=np.int)
    d0 = np.array(list(bin(d0)[2:].zfill(32)), dtype=np.int)

    # procesamos los chunks de 512bits
    for chunk in splitstring(mensaje_bits, 512):
        words = [np.array(list(''.join(splitstring(x, 8)[::-1])), dtype=np.int) for x in splitstring(chunk, 32)]
        A = a0
        B = b0
        C = c0
        D = d0

        # main loop
        for i in range(64):
            if i <= 15:
                f = bor(band(B, C), band(bnot(B), D))
                g = i
            elif 16 <= i <= 31:
                f = bor(band(D, B), band(bnot(D), C))
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                f = bxor(bxor(B, C), D)
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                f = bxor(C, bor(B, bnot(D)))
                g = (7*i) % 16

            F = bsum(f, bsum(A, bsum(k[i], words[g])))
            A = deepcopy(D)
            D = deepcopy(C)
            C = deepcopy(B)
            B = bsum(B, leftrotate(F, s[i]))

        a0 = bsum(a0, A)
        b0 = bsum(b0, B)
        c0 = bsum(c0, C)
        d0 = bsum(d0, D)

    tot = ''
    for h in [a0, b0, c0, d0]:
        h = ''.join([str(x) for x in h.tolist()])
        tot += ''.join(splitstring(''.join([hex(int(x, 2))[2:] for x in splitstring(h, 4)]), 2)[::-1])
    return tot
