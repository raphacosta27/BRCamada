class getType():
    def __init__(self, pacote):            
        self.pacote = pacote
        self.head = pacote[0:4]
        self.tipo = self.head[3]

    def getPacketType(self):
        # retorna "Comando", "Dado" ou "ERRO
        if self.tipo == 0x00:
            return 'dado'
        elif self.tipo == 0x10 or self.tipo == 0x11 or self.tipo == 0x12:
            return 'comando'
        else:
            return 'ERRO'

    def getCommandType(self):
        # retorna "SYN", "ACK", "NACK" ou "ERRO"
        if self.tipo == 0x10:
            print("SYN")
            return "SYN" 
        elif self.tipo == 0x11:
            print("ACK")
            return "ACK"
        elif self.tipo == 0x12:
            return "NACK"
        else:
            return "ERRO"