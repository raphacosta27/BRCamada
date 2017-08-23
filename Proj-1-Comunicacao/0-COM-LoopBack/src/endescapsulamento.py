from construct import *
import os
import binascii
import struct

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
        # return final.encode(encoding = "hex")

    def buildDataPacket(self, data):
        pacote = self.buildHead(len(data))
        pacote += data
        pacote += self.buildEOP()
        return(pacote)

    def unpackage (self, packet):
        payload = bytes([])
        head = packet[0:3]
        payload_len = head[1:]
        # numero = binascii.b2a_hex(payload_len) #isso da 1768 que é 5992 em hex
        # print(payload_len.decode('utf-8'))
        palavra_byte = payload_len.decode('utf-8')
        print(palavra_byte)
        # print(int(numero, 2))

        # payload = packet[3:payload_len]


teste = open('./imgs/panda.jpg', 'rb').read()
#/Proj-1-Comunicacao/0-COM-LoopBack/src
# dados = bytes([])
alo = Empacotamento()
build = alo.buildDataPacket(teste)
alo.unpackage(build)


#5992 em decimal é 5992, em hex é 1768 e o python entende como 0x17h

# alo.unpackage(build)




# print(binascii.b2a_hex(build[1:3]))


# print(binascii.b2a_hex(build[1]))
    # def extensionToBinary (name):
    #     nome, ext = os.path.splitext(name)
    #     binario = bytearray(ext, encoding = 'ascii')
    #     print(len(binario))

# constant/constant/type/len2/len1/len0/CRC(CheckSum)/PayLoad
