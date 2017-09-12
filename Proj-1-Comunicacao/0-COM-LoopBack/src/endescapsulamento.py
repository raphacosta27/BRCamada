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
        pacote = self.buildHead(len(data), 0x00, bytes([n]), bytes([total]))
        pacote += data
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
        n = int.from_bytes(head[4], byteorder = 'big')
        total = int.from_bytes(head[5], byteorder = 'big')
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
