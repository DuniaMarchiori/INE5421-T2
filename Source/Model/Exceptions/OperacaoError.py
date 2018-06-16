

class OperacaoError(Exception):
	PARSING_ERROR = "Erro ao aplicar a operação"

	def __init__(self, message="."):
		self.__message = self.PARSING_ERROR + message

	def get_message(self):
		return self.__message
