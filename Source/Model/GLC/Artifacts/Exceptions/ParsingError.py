

class ParsingError(Exception):
	PARSING_ERROR = "Erro ao reconhecer os dados de entrada"

	def __init__(self, message="."):
		self.__message = self.PARSING_ERROR + message

	def get_message(self):
		return self.__message
