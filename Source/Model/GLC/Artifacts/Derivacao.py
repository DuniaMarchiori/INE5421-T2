from GLC.Artifacts import *


class Derivacao:

	__gerador = None
	__derivacao = None
	__terminais = None
	__nao_terminais = None
	__derivacao_epsilon = None

	def __init__(self, gerador, derivacao):
		self.__inicializar_atributos(gerador, derivacao)

	def __inicializar_atributos(self, gerador, derivacao):
		self.__gerador = gerador
		self.__derivacao = derivacao

		self.__terminais = []
		self.__nao_terminais = []
		if len(derivacao) == 1 and derivacao[0].eh_epsilon():
			self.__derivacao_epsilon = True
		else:
			self.__derivacao_epsilon = False
			for simbolo in derivacao:
				if isinstance(simbolo, Vn):
					self.__nao_terminais.append(simbolo)
				elif isinstance(simbolo, Vt):
					self.__terminais.append(simbolo)
				else:
					raise(ProducaoError())

	def __str__(self):
		retorno = ""
		for simbolo in self.__derivacao:
			retorno += " " + str(simbolo)
		return retorno
