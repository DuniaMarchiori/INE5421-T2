

class ProducaoError(Exception):
	NOT_VALID_SYMBOL = "Simbolo desconhecido"

	def __init__(self, message="."):
		self.__message = self.NOT_VALID_SYMBOL + message

	def get_message(self):
		return self.__message
