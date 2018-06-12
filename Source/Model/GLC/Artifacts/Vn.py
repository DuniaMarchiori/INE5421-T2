

class Vn:

	__simbolos = ""

	def __init__(self, simbolos):
		self.__simbolos = simbolos

	def get_simbolos(self):
		return self.__simbolos

	def __str__(self):
		return self.__simbolos

	def __eq__(self, other):
		return isinstance(other, Vn) and self.get_simbolos() == other.get_simbolos()

	def __hash__(self):
		return hash(self.__simbolos)
