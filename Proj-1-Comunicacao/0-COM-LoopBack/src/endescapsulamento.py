import construct

class Empacotamento():

	headSTART = 0xFF
	headStruct = Struct("start" / Int8ub,
						"size" / Int16ub)

	def buildHead(self, dataLen):
		head = headStruct.build(dict(
									start = self.headSTART,
									size = dataLen))
		return (head)
