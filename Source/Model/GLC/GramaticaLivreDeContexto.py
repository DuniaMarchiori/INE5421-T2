from GLC import *

from collections import OrderedDict
import re


class GramaticaLivreDeContexto:

	__conjunto_producoes = OrderedDict()
	__terminais = set()
	__nao_terminais = set()
	__vn_inicial = None

	def __init__(self, entrada):
		self.__parse(entrada)

	def __parse(self, entrada):
		inicial_definido = False
		entrada_linhas = entrada.splitlines()
		num_linha = 0
		for linha in entrada_linhas:
			linha_limpa = re.sub("\s+", " ", linha)
			if simb_derivacao in linha_limpa:
				producao_lista = linha_limpa.split(simb_derivacao)
				if len(producao_lista) <= 2:
					produtor = self.__obtem_produtor(producao_lista[0], l)
					if not inicial_definido:
						self.__vn_inicial = produtor
						inicial_definido = True
					derivacoes = self.__obtem_derivacoes(produtor, producao_lista[1], l)
					for derivacao in derivacoes:
						self.adiciona_derivacao(produtor, derivacao)
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

	def __obtem_derivacoes(self, vn, derivacoes, linha):
		derivacoes_encontradas = derivacoes.split(simb_ou)

		derivacoes_resultantes = []
		for derivacao in derivacoes_encontradas:
			unidades_encontradas = derivacao.strip().split(" ")

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
							raise ParsingError(": símbolo inesperado na linha " + str(linha))
					elif tipo == 1:
						if simbolo not in alfabeto_terminais:
							raise ParsingError(": símbolo inesperado na linha " + str(linha))
					elif tipo == 2:
						raise ParsingError(": símbolo inesperado após o & na linha " + str(linha))

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

			derivacoes_resultantes.append(Derivacao(vn, unidades_resultantes))
		return derivacoes_resultantes

	def adiciona_derivacao(self, vn, producao):
		if vn not in self.__conjunto_producoes:
			self.__conjunto_producoes[vn] = []
		self.__conjunto_producoes[vn].append(producao)

	def __str__(self):
		retorno = ""
		for produtor in self.__conjunto_producoes:
			linha = str(produtor) + " " + simb_derivacao
			for derivacao in self.__conjunto_producoes[produtor]:
				linha += str(derivacao) + " |"
			linha = linha[0:-2] + "\n"
			if produtor == self.__vn_inicial:
				retorno = linha + retorno
			else:
				retorno += linha
		return retorno
