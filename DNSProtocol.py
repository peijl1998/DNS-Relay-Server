import struct
import random


def getDomainName(data):
    fileds = []
    data = data[12:]
    i = 0
    count = data[0]

    while count != 0:
        fileds.append(data[i + 1:i + count + 1].decode('ascii'))
        i += count + 1
        count = data[i]

    return '.'.join(fileds)

def getPacketId(data):
    return struct.unpack('!H', data[:2])[0]

def getPacketIp(data):
    an_count = struct.unpack('!H', data[6:8])[0]
    ns_count = struct.unpack('!H', data[8:10])[0]
    ar_count = struct.unpack('!H', data[10:12])[0]
    if an_count > 1 or ns_count != 0 or ar_count != 0:
        return data[6:]
    ip1, ip2, ip3, ip4 = struct.unpack('!BBBB', data[-4:])
    return "{}.{}.{}.{}".format(ip1, ip2, ip3, ip4)

def createResponsePacket(addr, data, ip):
    id = data[:2]  
    q_count = b'\x00\x01'  
    if ip != "0.0.0.0":
        flags = b'\x81\x80'  
        ans_RRs = b'\x00\x01' 
    else:
        flags = b'\x81\x83' 
        ans_RRs = b'\x00\x00'  
    auth_RRs = b'\x00\x00' 
    add_RRs = b'\x00\x00' 
    header = id + flags + q_count + ans_RRs + auth_RRs + add_RRs

    if type(ip) == type(b'\x00'):
        return id + flags + q_count + ip

    queries = data[12:]  

    name = b'\xc0\x0c' 
    rtype = b'\x00\x01' 
    a_class = b'\x00\x01'  
    ttl = struct.pack('!L', 3600) 
    data_length = struct.pack('!H', 4)  
    ip_num = ip.split('.')  
    address = struct.pack('!BBBB', int(ip_num[0]), int(ip_num[1]), int(ip_num[2]), int(ip_num[3]))
    answers = name + rtype + a_class + ttl + data_length + address

    return header + queries + answers


def createQueryPacket(data, id, dname):
    data = struct.pack('!H', id) + data[2:]

    return data

def createId(addr, mapping):
    id = random.randint(0, 65535)
    while id in mapping:
        id = random.randint(0, 65535)

    return id
