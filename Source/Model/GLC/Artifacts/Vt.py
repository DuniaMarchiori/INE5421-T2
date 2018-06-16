from Source.Model.GLC.Artifacts.Constants import *

'''
	Classe que representa um simbolo terminal dado por um agrupamento de símbolos.
'''
class Vt:

	__simbolos = ""
	__epsilon = False

	def __init__(self, simbolos):
		self.__simbolos = simbolos
		self.__epsilon = simbolos == epsilon

	def get_simbolos(self):
		return self.__simbolos

	def eh_epsilon(self):
		return self.__epsilon

	def __str__(self):
		return self.__simbolos

	def __eq__(self, other):
		return isinstance(other, Vt) and self.get_simbolos() == other.get_simbolos()

	def __hash__(self):
		return hash(self.__simbolos)
