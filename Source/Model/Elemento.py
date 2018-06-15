# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from enum import Enum


class Elemento:

	__nome = None
	__tipo = None

	def __init__(self, tipo, nome):
		self.__tipo = tipo
		self.__nome = nome

	def get_nome(self):
		return self.__nome

	def set_nome(self, novo_nome):
		self.__nome = novo_nome

	def get_tipo(self):
		return self.__tipo

	def to_string(self):
		return ""


class TipoElemento(Enum):
	GLC = 0
	CONJ = 1
