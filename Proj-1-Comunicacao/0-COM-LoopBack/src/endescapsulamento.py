from construct import *
import os
import binascii

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


dados = bytes([0x00,0x00,0x00])
alo = Empacotamento()
build = alo.buildDataPacket(dados)
print(build[6:])
print(binascii.unhexlify(build[6:]))
    # def extensionToBinary (name):
    #     nome, ext = os.path.splitext(name)
    #     binario = bytearray(ext, encoding = 'ascii')
    #     print(len(binario))

# constant/constant/type/len2/len1/len0/CRC(CheckSum)/PayLoad
