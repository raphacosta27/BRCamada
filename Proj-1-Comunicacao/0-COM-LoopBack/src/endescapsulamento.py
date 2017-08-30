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
                                "type"/ Int8ub)
        self.HEADTYPE = self.HeadTypes()
    def buildHead(self, dataLen, type):
        head = self.headStruct.build(dict(
        start = self.headSTART,
        size = dataLen,
        type = type))
        return (head)

    def buildEOP (self):
        final = "pandatata"
        finalByte = bytearray(final, encoding="ascii")
        return binascii.hexlify(finalByte)

    def buildDataPacket(self, data):
        pacote = self.buildHead(len(data), 0x00)
        pacote += data
        pacote += self.buildEOP()
        return(pacote)

    def get_bin(self, x):
        return format(x, 'b').zfill(16)

    def unpackage (self, packet):
        #print(packet)
        head = packet[0:4]
        payload_len = head[1:3]
        tipo = head[3]
        size = int.from_bytes(payload_len, byteorder = 'big')
        payload = packet[len(head):]

        if size == 0:
            return head
        else:
            return payload

    def buildSynPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.SYN)
        p += self.buildEOP()
        return(p)

    def buildAckPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.ACK)
        p += self.buildEOP()
        return(p)

    def buildNackPacket(self):
        p = self.buildHead(0x00, self.HEADTYPE.NACK)
        p += self.buildEOP()
        return(p)

    def getPacketLen(self, packet):
        head = packet[0:4]
        time.sleep(1)
        payload_len = head[1:3]
        size = int.from_bytes(payload_len, byteorder = 'big')
        print(size)
        return size


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
