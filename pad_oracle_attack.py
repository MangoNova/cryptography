

'''
try IV[15] from 0x00 to 0xFF, find out which(called G[15]) will make the c1[15] = 0x01, 
and get the plain message[15].
Use G[15] to get the G_p which will make the end of plain text end of 0x02
set IV[15] = G_p and try IV[14] from 0x00 to 0xFF,  find out G[14] that make the c1[14] = 0x02, 
and get the plain message[15].
so on to get all the bytes
and then xor the last term bytes with 0x10, to get the plain text.
notice that c2 maybe padded, so should decode it to utf-8 after cut the padding bytes.
'''
from pwn import *
server_ip = ip
server_port = 1336

O_IV = '53656375726549566973536563757265'

message = 'baf9cbeff9097d1ed163e9209354a2acdb8c5c6facdf68b15b14b29823bc8114'
c1 = message[:32]
c2 = message[32:]
p_IV = [['0' * 32 for _ in range(16)] for _ in range(2)]


def poa(c, idx):
    for i in range(16):
        for j in range(256):
            io = remote(server_ip, server_port)
            received_data = io.recv(1024)
            p_IV[idx][i] = p_IV[idx][i][:32 - (i + 1) * 2] + format(j, '02X') + p_IV[idx][i][32 - i * 2:]
            data_to_send = p_IV[idx][i]
            print('p_IV:', data_to_send)
            io.sendline(data_to_send.encode('utf-8'))
            received_data = io.recv(1024)
            io.sendline(c.encode('utf-8'))
            received_data = io.recv(1024)
            print('reveived:', received_data.decode('utf-8'))
            io.close()
            if received_data != 'Invalid Padding!\n'.encode('utf-8'):
                if 15 == i:
                    break
                for k in range(i + 1):
                    p_IV[idx][i + 1] = p_IV[idx][i + 1][:32 - (k + 1) * 2] + format(
                        int(p_IV[idx][i][32 - (k + 1) * 2:32 - k * 2], 16) ^ (i + 2) ^ (i + 1),
                        '02X') + p_IV[idx][i + 1][32 - k * 2:]
                break


if __name__ == '__main__':
    poa(c1, 0)
    poa(c2, 1)
    print('IVs:', p_IV.__str__())

    print('P1 bytes:', format(int(p_IV[0][15], 16) ^ int(O_IV, 16) ^ int('10' * 16, 16), '02X'))
    print('P2 bytes:', format(int(p_IV[1][15], 16) ^ int(c1, 16) ^ int('10' * 16, 16), '02X'))


    print('P1', bytes.fromhex(format(int(p_IV[0][15], 16) ^ int(O_IV, 16) ^ int('10' * 16, 16), '02X')).decode('utf-8'))
    print('P2', bytes.fromhex(format(int(p_IV[1][15], 16) ^ int(c1, 16) ^ int('10' * 16, 16), '02X'))[:-1].decode('utf-8'))


