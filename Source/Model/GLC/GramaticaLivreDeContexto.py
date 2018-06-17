from Source.Model.GLC.Artifacts.Constants import *
from Source.Model.GLC.Artifacts.Producao import *
from Source.Model.GLC.Artifacts.Vn import *
from Source.Model.GLC.Artifacts.Vt import *
from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *
from Source.Model.Exceptions.OperacaoError import *


from Source.Model.Elemento import *

from collections import OrderedDict
import re

'''
	Classe que representa uma gramática livre de contexto.
'''
class GramaticaLivreDeContexto(Elemento):

	def __init__(self, nome, entrada):
		super(GramaticaLivreDeContexto, self).__init__(TipoElemento.GLC, nome)
		self.__conjunto_producoes = OrderedDict()
		self.__terminais = set()
		self.__nao_terminais = set()
		self.__vn_inicial = None
		self.__parse(entrada)
		self.nf = None

	def __parse(self, entrada):
		inicial_definido = False
		entrada_linhas = entrada.splitlines()
		num_linha = 0
		for linha in entrada_linhas:
			if linha: # Se a linha não for em branco
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
							self.__adiciona_producao(produtor, producao)
					else:
						raise ParsingError(": símbolo de derivação (" + simb_derivacao + ") encontrado múltiplas vezes na linha " + str(num_linha))
				else:
					raise ParsingError(": símbolo de derivação (" + simb_derivacao + ") não encontrado na linha " + str(num_linha))
				num_linha += 1
		if self.__existe_vn_indefinido():
			raise ParsingError(": existem símbolos de Vn que não tiveram suas produções definidas")

	def __existe_vn_indefinido(self):
		for vn in self.__nao_terminais:
			if vn not in self.__conjunto_producoes:
				return True
		return False

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
				primeiro_simbolo = unidade[0]
				try:
					if primeiro_simbolo in alfabeto_nao_terminais_inicial:
						vn = Vn(unidade)
						unidades_resultantes.append(vn)
						self.__nao_terminais.add(vn)
					elif primeiro_simbolo in (alfabeto_terminais + epsilon):
						vt = Vt(unidade)
						unidades_resultantes.append(vt)
						self.__terminais.add(vt)
					else:
						raise ParsingError(": símbolo de Vt ou Vn esperado mas não encontrado")
				except ParsingError as e:
					raise ParsingError(e.get_message() + " na linha " + str(linha))
			producoes_resultantes.append(Producao(vn, unidades_resultantes))
		return producoes_resultantes

	def __adiciona_producao(self, vn, producao):
		if vn not in self.__conjunto_producoes:
			self.__conjunto_producoes[vn] = set()
		self.__conjunto_producoes[vn].add(producao)

	def vn_pertence(self, vn):
		return vn in self.__nao_terminais

	def vt_pertence(self, vt):
		return vt in self.__terminais

	def remove_recursao_esq(self):
		if self.existe_recursao_esq():
			raise OperacaoError(" a gramática não possui recursão à esquerda")
		elif not self.eh_propria():
			raise OperacaoError(" a gramática não é própria")
		else:
			print()
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obter quais não terminais possuem recursão à esquerda e pra cada um, se são recursões diretas ou indiretas
			#       - Essa estrutura pode ser um dicionário, onde as chaves são os não terminais e o valor é o tipo da recursividade
			#   - Cria uma nova GLC sem recursão à esquerda usando o algoritmo.
			#   - Retorna a GLC e também a estrutura dos terminais que possuem recursão

	def existe_recursao_esq(self):
		pass
		# TODO
		# Deve:
		#   - Verificar se existem recursões à esquerda nessa gramática (retorna True ou False)

	def transforma_epsilon_livre(self):
		if self.eh_epsilon_livre():
			raise OperacaoError(" a gramática já é epsilon-livre")
		else:
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obtem o conjunto Ne com o método self.obtem_ne()
			#   - Cria uma nova GLC epsilon-livre usando o algoritmo com base no conjunto.
			#   - Retorna a gramática e o conjunto, nessa ordem

	def eh_epsilon_livre(self):
		pass
		# TODO
		# Deve:
		#   - Verificar se é &-livre (retorna True ou False)

	def obtem_ne(self):
		pass
		# TODO
		# Deve:
		#   - Retornar o conjunto Ne utilizado no método de transformação em &-livre

	def remove_simples(self):
		if not self.existe_producoes_simples():
			raise OperacaoError(" a gramática não possui nenhuma produção simples")
		else:
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obtem os conjuntos NA com o método self.obtem_na()
			#   - Cria uma nova GLC sem produções simples usando o algoritmo, com base nos conjuntos.
			#   - Retorna a gramática e os conjuntos, nessa ordem

	def existe_producoes_simples(self):
		for vn in self.__conjunto_producoes:
			for derivacao in self.__conjunto_producoes[vn]:
				if derivacao.eh_simples():
					return True
		return False

	def obtem_na(self):
		pass
		# TODO
		# Deve:
		#   - Retornar os conjuntos NA pra cada A E Vn, utilizados no método de remoção de produções simples
		#       - Esses NA podem ser representados por um dicionário em que cada chave 'x' é o conjunto Nx por exemplo

	def remove_inferteis(self):
		if not self.existe_inferteis():
			raise OperacaoError(" a gramática não possui nenhuma produção infértil")
		else:
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obtem o conjunto NF com o método self.obtem_nf()
			#   - Cria uma nova GLC sem produções inférteis usando o algoritmo, com base no conjunto.
			#   - Retorna a gramática e o conjunto, nessa ordem

	def existe_inferteis(self):
		nf = self.obtem_nf()
		return nf != set()

	def obtem_nf(self):
		if self.nf != None:
			return self.nf

		nf = set()
		nf_atual = set()
		continua = True
		nt = set(self.__conjunto_producoes)

		while continua:
			nf = set(nf_atual)
			for A in nt:
				adicionado = False
				producoes = self.__conjunto_producoes[A]
				for x in producoes:
					if not adicionado:
						prod = x.get_derivacao()
						for simbolo in prod:
							if any(simbolo not in nf_atual and simbolo not in self.__terminais for simbolo in prod):
								break
							else:
								nf_atual.add(A)
								adicionado = True
								break
					else:
						break
			nt = nt - nf_atual
			continua = (nf != nf_atual)

		self.nf = nf
		return self.nf


	def remove_inalcancaveis(self):
		if not self.existe_inalcancavel():
			raise OperacaoError(" a gramática não possui nenhuma produção inalcançável")
		else:
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obtem o conjunto Vi com o método self.obtem_vi()
			#   - Cria uma nova GLC sem produções inalcançáveis usando o algoritmo, com base no conjunto.
			#   - Retorna a gramática e o conjunto, nessa ordem

	def existe_inalcancavel(self):
		pass
		# TODO
		# Deve:
		#   - Verificar se existem produções inalcancaveis (retorna True ou False)

	def obtem_vi(self):
		pass
		# TODO
		# Deve:
		#   - Retornar o conjunto Vi utilizado no método de remoção de inalcançáveis

	def existem_inuteis(self):
		return self.existe_inferteis() or self.existe_inalcancavel()

	def eh_propria(self):
		return self.eh_epsilon_livre() and (not self.existe_producoes_simples()) and (not self.existem_inuteis())

	# Propriedades

	'''
		:return 0 se for vazia, 1 se for finita ou 2 se for infinita
	'''
	def finitude(self):
		ferteis = self.obtem_nf()
		if self.__vn_inicial not in ferteis:
			return 0
		elif self.__infinita():
			return 2
		else:
			return  1

	def __infinita(self):
		for A in self.__conjunto_producoes:
			producoes = self.__conjunto_producoes[A]
			for x in producoes:
				prod = x.get_derivacao()
				if A in prod:
					return True

				prox_deriv = set(self.__nao_terminais.intersection(set(prod)))
				visitados = set([A])
				while any(simbolo not in visitados for simbolo in prox_deriv):
					for y in prox_deriv:
						visitados.add(y)
						producoes = self.__conjunto_producoes[y]
						for z in producoes:
							prod = z.get_derivacao()
							if A in prod:
								return True
					prox_deriv = set(self.__nao_terminais.intersection(set(prod)))

		return False

	def first(self, simb):
		pass
		# TODO
		# Deve:
		#   - Verificar se vn pertence à Vn
		#   - Retornar o conjunto de First de vn

	def follow(self, simb):
		pass
		# TODO
		# Deve:
		#   - Verificar se vn pertence à Vn
		#   - Retornar o conjunto de Follow de vn

	def first_nt(self, simb):
		pass
		# TODO
		# Deve:
		#   - Verificar se vn pertence à Vn
		#   - Retornar o conjunto de First-NT de vn

	def esta_fatorada(self):
		for vn in self.__conjunto_producoes:
			firsts_das_derivacoes = set()
			for derivacao in self.__conjunto_producoes[vn]:
				first_dessa_derivacao = self.first(str(derivacao))
				if firsts_das_derivacoes & first_dessa_derivacao:  # intersecção não é nula:
					return False
		return True

	def eh_fatoravel_em_n_passos(self, n):
		pass
		# TODO
		# Deve:
		#   - (Lembrete: Utilizar classe GLCEditavel pra construir cada passo da GLC durante a fatoração)
		#   - Tentar fatorar em no máximo n passos
		#   - Só precisa retornar True ou False por enquanto

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

# Imports colocados abaixo para contornar dependência circular
from Source.Model.GLC.Artifacts.GLCEditavel import GLCEditavel
