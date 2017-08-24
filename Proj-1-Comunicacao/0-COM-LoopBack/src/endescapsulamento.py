from construct import *
import os
import binascii
import struct
import codecs

class Empacotamento():
    
    def __init__(self):
        self.headSTART = 0xBB
        self.headStruct = Struct("start"/ Int8ub,
                                "size" / Int16ub)

    def buildHead(self, dataLen):
        head = self.headStruct.build(dict(
        start = self.headSTART,
        size = dataLen))
        return (head)

    def buildEOP (self):
        final = "pandatata"
        finalByte = bytearray(final, encoding="ascii")
        return binascii.hexlify(finalByte)

    def buildDataPacket(self, data):
        pacote = self.buildHead(len(data))
        pacote += data
        pacote += self.buildEOP()
        return(pacote)

    def get_bin(self, x):
        return format(x, 'b').zfill(16)

    def unpackage (self, packet):
    
        head = packet[0:3]
        print(len(head))
        payload_len = head[1:]
        size = int.from_bytes(payload_len, byteorder = 'big')

        payload = packet[len(head):]
        print(len(payload))

        return payload

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
