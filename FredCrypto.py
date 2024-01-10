"""
INPUT: bitstring message m of length < 2**32 bits
Pad m with a 32-bit encoding of the length of m
c := emptystring
while there are still bits to take from m:
Take the next bit from m and append it to c
c := c << 1
Take the next |c| bits from m and xor them into c
Truncate c to 64 bits, if necessary
OUTPUT: c
"""


def FredCrypto(m):
    length = len(m)
    length_encoding = format(length, '032b')
    m += length_encoding
    c = ""
    i = 0
    while i < len(m):
        c += m[i]
        temp = c[0]
        c = c[1:]
        c += temp
        i += 1
        if i + len(c) < len(m):
            xor_bits = m[i:len(c) + i]
            c = "".join(['1' if a != b else '0' for a, b in zip(c, xor_bits)])
            i += len(c)
        else:
            xor_bits = m[i:]
            xor_bits += "0" * (i + len(c) - len(m))
            c = "".join(['1' if a != b else '0' for a, b in zip(c, xor_bits)])
            i += len(c)
    c = c[:64]
    return c


if __name__ == '__main__':
    my_dict = {}
    for i in range(1023):
        m = bin(i)[2:]
        result = FredCrypto(m)
        if result not in my_dict:
            my_dict[result] = m
        else:
            print('collision!', my_dict[result], m, 'hashValue', result)
