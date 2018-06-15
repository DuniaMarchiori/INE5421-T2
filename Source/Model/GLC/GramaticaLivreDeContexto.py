from Source.Model.GLC.Artifacts.Constants import *
from Source.Model.GLC.Artifacts.Producao import *
from Source.Model.GLC.Artifacts.Vn import *
from Source.Model.GLC.Artifacts.Vt import *
from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *

from Source.Model.Elemento import *

from collections import OrderedDict
import re

'''
	Classe que representa uma gramática livre de contexto.
'''
class GramaticaLivreDeContexto(Elemento):

	__conjunto_producoes = OrderedDict()
	__terminais = set()
	__nao_terminais = set()
	__vn_inicial = None

	def __init__(self, nome):
		super(GramaticaLivreDeContexto, self).__init__(TipoElemento.GLC, nome)

	def parse(self, entrada):
		inicial_definido = False
		entrada_linhas = entrada.splitlines()
		num_linha = 0
		for linha in entrada_linhas:
			linha_limpa = re.sub("\s+", " ", linha)
			if simb_derivacao in linha_limpa:
				producao_lista = linha_limpa.split(simb_derivacao)
				if len(producao_lista) <= 2:
					produtor = self.__obtem_produtor(producao_lista[0], num_linha)
					if not inicial_definido:
						self.__vn_inicial = produtor
						inicial_definido = True
					producoes = self.__obtem_producoes(produtor, producao_lista[1], num_linha)
					for producao in producoes:
						self.adiciona_producao(produtor, producao)
				else:
					raise ParsingError(": símbolo de derivação (" + simb_derivacao + ") encontrado múltiplas vezes na linha " + str(num_linha))
			else:
				raise ParsingError(": símbolo de derivação (" + simb_derivacao + ") não encontrado na linha " + str(num_linha))
			num_linha += 1

	def __obtem_produtor(self, produtor, linha):
		produtor_limpo = produtor.strip()
		primeiro_loop = True
		for simbolo in produtor_limpo:
			if primeiro_loop:
				if simbolo not in alfabeto_nao_terminais_inicial:
					raise ParsingError(": símbolo inesperado na linha " + str(linha))
				primeiro_loop = False
			else:
				if simbolo not in alfabeto_nao_terminais_seguintes:
					raise ParsingError(": símbolo inesperado na linha " + str(linha))
		vn = Vn(produtor_limpo)
		self.__nao_terminais.add(vn)
		return vn

	def __obtem_producoes(self, vn, producoes, linha):
		producoes_encontradas = producoes.split(simb_ou)

		producoes_resultantes = []
		for producao in producoes_encontradas:
			unidades_encontradas = producao.strip().split(" ")

			unidades_resultantes = []
			for unidade in unidades_encontradas:
				unidade = unidade.strip()
				tipo = -1
				for simbolo in unidade:
					if tipo == -1:
						if simbolo in alfabeto_nao_terminais_inicial:
							tipo = 0
						elif simbolo in alfabeto_terminais:
							tipo = 1
						elif simbolo == epsilon:
							tipo = 2
					elif tipo == 0:
						if simbolo not in alfabeto_nao_terminais_seguintes:
							raise ParsingError(": símbolo inesperado na sintaxe de um não terminal na linha " + str(linha))
					elif tipo == 1:
						if simbolo not in alfabeto_terminais:
							raise ParsingError(": símbolo inesperado na sintaxe de um terminal na linha " + str(linha))
					elif tipo == 2:
						raise ParsingError(": símbolo inesperado após o símbolo & na linha " + str(linha))

				if tipo == 0:
					vn = Vn(unidade)
					unidades_resultantes.append(vn)
					self.__nao_terminais.add(vn)
				elif tipo == 1 or tipo == 2:
					vt = Vt(unidade)
					unidades_resultantes.append(vt)
					if tipo != 2:
						self.__terminais.add(vt)
				else:
					raise ParsingError(": símbolo de Vt ou Vn esperado mas não encontrado na linha " + str(linha))

			producoes_resultantes.append(Producao(vn, unidades_resultantes))
		return producoes_resultantes

	def adiciona_producao(self, vn, producao):
		if vn not in self.__conjunto_producoes:
			self.__conjunto_producoes[vn] = []
		self.__conjunto_producoes[vn].append(producao)

	def to_string(self):
		return self.__str__()

	def __str__(self):
		retorno = ""
		for produtor in self.__conjunto_producoes:
			linha = str(produtor) + " " + simb_derivacao
			for producao in self.__conjunto_producoes[produtor]:
				linha += str(producao) + " |"
			linha = linha[0:-2] + "\n"
			if produtor == self.__vn_inicial:
				retorno = linha + retorno
			else:
				retorno += linha
		return retorno
