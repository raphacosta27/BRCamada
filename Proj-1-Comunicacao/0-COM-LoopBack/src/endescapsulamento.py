from construct import *
import os

class Empacotamento():

    headSTART = 0xBB
    headStruct = Struct("start"/ Int8ub,
                        "type" / Int32ub,
                        "size" / Int16ub)

    def buildHead(self, tipo ,dataLen):
        head = headStruct.build(dict(
        start = self.headSTART,
        type = tipo,
        size = dataLen))
        return (head)

    def buildEOP (self):
        final = "pandatata"
        return final.encode(encoding = "hex")

    def buildDataPacket(self, data, name):
        pacote = self.buildHead(len(Data))
        name, ext = os.path.splitext('file.txt')
        pacote += data
        pacote += self.buildEOP()
        return(pacote)

    def extensionToBinary (name):
        nome, ext = os.path.splitext(name)
        binario = bytearray(ext, encoding = 'ascii')
        print(len(binario))



# constant/constant/type/len2/len1/len0/CRC(CheckSum)/PayLoad
