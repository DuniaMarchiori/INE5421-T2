from Source.Model.GLC.Artifacts.Vn import *
from Source.Model.GLC.Artifacts.Vt import *
from Source.Model.GLC.Artifacts.Exceptions.ProducaoError import *


'''
	Classe que representa uma producao de uma GLC.
'''
class Producao:

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

		self.__terminais = set()
		self.__nao_terminais = set()
		if isinstance(derivacao[0], Vt) and len(derivacao) == 1 and derivacao[0].eh_epsilon():
			self.__derivacao_epsilon = True
		else:
			self.__derivacao_epsilon = False
			for simbolo in derivacao:
				if isinstance(simbolo, Vn):
					self.__nao_terminais.add(simbolo)
				elif isinstance(simbolo, Vt):
					self.__terminais.add(simbolo)
				else:
					raise(ProducaoError(": a produção tem que derivar um Vn ou um Vt"))

	def __str__(self):
		retorno = ""
		for simbolo in self.__derivacao:
			retorno += " " + str(simbolo)
		return retorno
