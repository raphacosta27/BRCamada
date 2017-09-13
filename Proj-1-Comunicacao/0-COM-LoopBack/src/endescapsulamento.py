from construct import *
import os
import binascii
import struct
import codecs
import time

class Empacotamento():
    
    class HeadTypes():
        
        def __init__(self):
            self.SYN = 0x10
            self.ACK = 0x11
            self.NACK = 0x12
    
    def __init__(self):
        self.headSTART = 0xBB
        self.headStruct = Struct("start"/ Int8ub,
                                "size" / Int16ub,
                                "type"/ Int8ub,
                                "n"/ Int8ub,
                                "total"/ Int8ub)
        self.HEADTYPE = self.HeadTypes()

    def buildHead(self, dataLen, type, n, total):
        head = self.headStruct.build(dict(
        start = self.headSTART,
        size = dataLen,
        type = type,
        n = n,
        total = total))
        return (head)

    def buildEOP (self):
        final = "pandatata"
        finalByte = bytearray(final, encoding="ascii")
        return binascii.hexlify(finalByte)

    def buildDataPacket(self ,data, n, total):
        head = self.buildHead(len(data), 0x00, n, total)
        pacote = head
        key = self.getKey()

        crcHead = self.encodeData(str(head), key)
        hexKeyHead = self.stringToHex(crcHead)

        crcPayload = self.encodeData(str(data), key)
        hexKeyPayload = self.stringToHex(crcPayload)

        pacote += hexKeyHead
        pacote += data
        pacote += hexKeyPayload
        pacote += self.buildEOP()
        return(pacote)

    def get_bin(self, x):
        return format(x, 'b').zfill(16)

    def unpackage (self, packet):
        #print(packet)
        head = packet[0:6]
        payload_len = head[1:3]
        tipo = head[3]
        size = int.from_bytes(payload_len, byteorder = 'big')
        payload = packet[len(head):]

        if size == 0:
            return head
        else:
            return payload

    def getHeadParameters (self, packet):
        head = packet[0:6]
        n = head[4]
        total = head[5]
        # n = int.from_bytes(head[4], byteorder = 'big')
        # total = int.from_bytes(head[5], byteorder = 'big')
        return n, total


    def buildSynPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.SYN, 0x00, 0x00)
        p += self.buildEOP()
        return(p)

    def buildAckPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.ACK, 0x00, 0x00)
        p += self.buildEOP()
        return(p)

    def buildNackPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.NACK, 0x00, 0x00)
        p += self.buildEOP()
        return(p)

    def getPacketLen(self, packet):
        head = packet[0:4]
        time.sleep(1)
        payload_len = head[1:3]
        size = int.from_bytes(payload_len, byteorder = 'big')
        print(payload_len)
        return size

    def xor(self, a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
 
        return ''.join(result)

    def mod2div(self, divident, divisor):

        pick = len(divisor)
        tmp = divident[0 : pick]
    
        while pick < len(divident):
    
            if tmp[0] == '1':
                tmp = self.xor(divisor, tmp) + divident[pick]
    
            else: 
                tmp = self.xor('0'*pick, tmp) + divident[pick]
    
            pick += 1
    
        if tmp[0] == '1':
            tmp = self.xor(divisor, tmp)
        else:
            tmp = self.xor('0'*pick, tmp)
    
        checkword = tmp
        return checkword

    def encodeData(self, data, key):
    
        l_key = len(key)

        appended_data = data + '0'*(l_key-1)
        remainder = self.mod2div(appended_data, key)
    
        codeword = data + remainder

        return remainder
        
    def getKey(self):
        key = "10011"
        return key

    def stringToHex(self, data):
        dataByte = bytearray(data, encoding = "ascii")
        dataHex = binascii.hexlify(dataByte)
        return dataHex

# found = False
# teste = open('./imgs/panda.jpg', 'rb').read()
# #/Proj-1-Comunicacao/0-COM-LoopBack/src
# # dados = bytes([])
# alo = Empacotamento()
# build = alo.buildDataPacket(teste)

# eop = codecs.decode(alo.buildEOP(), "hex")

# while(found == False):
#     if(build.found(eop)) != -1:
#         print("achei")
#         found = True
#         print(build[:eop])
#     else: 
#         print("nao achei")


# alo.unpackage(build)


#5992 em decimal é 5992, em hex é 1768 e o python entende como 0x17h

# alo.unpackage(build)

# print(binascii.b2a_hex(build[1:3]))


# print(binascii.b2a_hex(build[1]))
    # def extensionToBinary (name):
    #     nome, ext = os.path.splitext(name)
    #     binario = bytearray(ext, encoding = 'ascii')
    #     print(len(binario))

# constant/constant/type/len2/len1/len0/CRC(CheckSum)/PayLoad
