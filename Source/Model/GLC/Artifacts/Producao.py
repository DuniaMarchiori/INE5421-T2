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
	__eh_simples = None

	def __init__(self, gerador, derivacao):
		self.__inicializar_atributos(gerador, derivacao)

	def __inicializar_atributos(self, gerador, derivacao):
		self.__gerador = gerador
		self.__derivacao = derivacao

		self.__terminais = set()
		self.__nao_terminais = set()
		if isinstance(derivacao[0], Vt) and len(derivacao) == 1 and derivacao[0].eh_epsilon():
			self.__derivacao_epsilon = True
			self.__eh_simples = False
		else:
			self.__derivacao_epsilon = False
			self.__eh_simples = (len(derivacao) == 1) and isinstance(derivacao[0], Vn)
			for simbolo in derivacao:
				if isinstance(simbolo, Vn):
					self.__nao_terminais.add(simbolo)
				elif isinstance(simbolo, Vt):
					self.__terminais.add(simbolo)
				else:
					raise(ProducaoError(": a produção tem que derivar um Vn ou um Vt"))

	def eh_simples(self):
		return self.__eh_simples

	def __str__(self):
		retorno = ""
		for simbolo in self.__derivacao:
			retorno += " " + str(simbolo)
		return retorno

	def __eq__(self, other):
		return isinstance(other, Producao) and hash(self) == hash(other)

	def __hash__(self):
		return hash(str(self.__gerador) + str(self))
