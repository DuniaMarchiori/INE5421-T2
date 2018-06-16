from Source.Model.GLC.Artifacts.Constants import *
from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *


'''
	Classe que representa um simbolo não terminal dado por um agrupamento de símbolos.
'''
class Vn:

	__simbolos = ""

	def __init__(self, simbolos):
		self.__valida_token(simbolos)
		self.__simbolos = simbolos

	def __valida_token(self, simbolos):
		primeiro_loop = True
		for simbolo in simbolos:
			if primeiro_loop:
				if simbolo not in alfabeto_nao_terminais_inicial:
					raise ParsingError(": símbolo Vn esperado mas não encontrado")
				primeiro_loop = False
			else:
				if simbolo not in alfabeto_nao_terminais_seguintes:
					raise ParsingError(": símbolo inesperado após o reconhecimento de um caracter de Vn")

	def get_simbolos(self):
		return self.__simbolos

	def __str__(self):
		return self.__simbolos

	def __eq__(self, other):
		return isinstance(other, Vn) and self.get_simbolos() == other.get_simbolos()

	def __hash__(self):
		return hash(self.__simbolos)
