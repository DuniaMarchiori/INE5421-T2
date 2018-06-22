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
		self.__nf = None
		self.__vi = None
		self.__first_memo = None
		self.__follow_memo = None
		self.__first_nt_memo = None

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

	def __obtem_producoes(self, gerador, producoes, linha):
		producoes_encontradas = producoes.split(simb_ou)

		producoes_resultantes = []
		for producao in producoes_encontradas:
			try:
				unidades_resultantes = self.__obtem_producao(producao)
			except ParsingError as e:
				raise ParsingError(e.get_message() + " na linha " + str(linha))
			producoes_resultantes.append(Producao(gerador, unidades_resultantes))
		return producoes_resultantes

	def __obtem_producao(self, producao):
		unidades_encontradas = producao.strip().split(" ")

		unidades_resultantes = []
		for unidade in unidades_encontradas:
			unidade = unidade.strip()
			primeiro_simbolo = unidade[0]
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
		return unidades_resultantes

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
		return bool(self.__nao_terminais.difference(nf)) # Retorna falso se a diferença resulta em um conjunto vazio

	def obtem_nf(self):
		if self.__nf is not None:
			return self.__nf

		nf = set()
		nf_atual = set()
		continua = True
		nt = set(self.__nao_terminais)

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

		self.__nf = nf
		return self.__nf


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
		vi = self.obtem_vi()
		return bool(self.__nao_terminais.difference(vi))  # Retorna falso se a diferença resulta em um conjunto vazio

	def obtem_vi(self):
		if self.__vi is not None:
			return self.__vi

		vi = set()
		vi_atual = set()
		vi_atual.add(self.__vn_inicial)
		visitados = set()

		while vi != vi_atual:
			vi = set(vi_atual)
			for X in set(vi - visitados):
				visitados.add(X)
				producoes = self.__conjunto_producoes[X]
				for y in producoes:
					prod = y.get_derivacao()
					vi_atual = vi_atual.union(set(self.__nao_terminais.intersection(set(prod))))

		self.__vi = vi
		return self.__vi

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
		simbolos_uteis = self.obtem_nf().intersection(self.obtem_vi())
		for A in simbolos_uteis:
			producoes = self.__conjunto_producoes[A]
			for x in producoes:
				prod = x.get_derivacao()
				contem_terminal = any(simbolo in self.__terminais for simbolo in prod)
				if A in prod and contem_terminal:
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
								contem_terminal = contem_terminal or any(simbolo in self.__terminais for simbolo in prod)
								if contem_terminal:
									return True
					prox_deriv = set(self.__nao_terminais.intersection(set(prod)))

		return False

	def first(self):
		if self.__first_memo is not None:
			return self.__first_memo

		firsts = OrderedDict()
		epsilon_vt = Vt(epsilon)
		epsilon_set = set([epsilon_vt])
		houve_mudanca = True
		while houve_mudanca:
			houve_mudanca = False
			for vn in self.__conjunto_producoes:
				if vn not in firsts:
					firsts[vn] = set()
				for producao in self.__conjunto_producoes[vn]:
					derivacao = producao.get_derivacao()
					incluir_epsilon = True
					for simbolo in derivacao:
						if isinstance(simbolo, Vt):
							if simbolo not in firsts[vn]:
								firsts[vn].add(simbolo)
								houve_mudanca = True
							incluir_epsilon = False
							break
						elif isinstance(simbolo, Vn):
							if simbolo not in firsts:
								firsts[simbolo] = set()
							if (firsts[simbolo] - epsilon_set) - firsts[vn]:  # Se a diferença entre os firsts não for nula
								firsts[vn] = firsts[vn].union(firsts[simbolo] - epsilon_set)
								houve_mudanca = True
							if epsilon_vt not in firsts[simbolo]:
								incluir_epsilon = False
								break
					if incluir_epsilon and epsilon_vt not in firsts[vn]:
						firsts[vn].add(Vt(epsilon))
						houve_mudanca = True
		self.__first_memo = firsts
		return self.__first_memo

	def first_producao(self, producao):
		epsilon_vt = Vt(epsilon)
		epsilon_set = set([epsilon_vt])
		first_vns = self.first()
		first = set()
		inclui_epsilon = True
		derivacao = producao.get_derivacao()
		for simbolo in derivacao:
			if isinstance(simbolo, Vt):
				first.add(simbolo)
				inclui_epsilon = False
				break
			elif isinstance(simbolo, Vn):
				firsts_do_vn = first_vns[simbolo]
				first = first.union(firsts_do_vn - epsilon_set)
				if epsilon_vt not in firsts_do_vn:
					inclui_epsilon = False
					break
		if inclui_epsilon:
			first.add(epsilon_vt)
		return first

	def follow(self):
		if self.__follow_memo is not None:
			return self.__follow_memo

		#final_de_sentenca = Vt(simb_final_de_sentenca)
		final_de_sentenca = simb_final_de_sentenca
		epsilon_vt = Vt(epsilon)
		epsilon_set = set([epsilon_vt])
		follows = OrderedDict()

		# Passo 1
		for vn in self.__conjunto_producoes:
			follows[vn] = set()
			if vn == self.__vn_inicial:
				follows[vn].add(final_de_sentenca)

		# Passo 2
		first_betas = {}
		for vn in self.__nao_terminais:
			for producao in self.__conjunto_producoes[vn]:
				derivacao = producao.get_derivacao()
				for i in range(0, len(derivacao)):
					if i < len(derivacao) - 1:
						simbolo = derivacao[i]
						if isinstance(simbolo, Vn):
							beta = Producao(producao.get_gerador(), derivacao[i+1:])
							if beta not in first_betas:
								first_betas[beta] = self.first_producao(beta)
							follows[simbolo] = follows[simbolo].union(first_betas[beta] - epsilon_set)

		# Passo 3
		houve_mudanca = True
		while houve_mudanca:
			houve_mudanca = False
			for vn in self.__nao_terminais:
				follow_gerador = follows[vn]
				for producao in self.__conjunto_producoes[vn]:
					derivacao = producao.get_derivacao()
					for i in range(0, len(derivacao)):
						simbolo = derivacao[i]
						if isinstance(simbolo, Vn):
							if i < len(derivacao) - 1:
								beta = Producao(producao.get_gerador(), derivacao[i + 1:])
							else:
								beta = Producao(producao.get_gerador(), [epsilon_vt])
							if beta not in first_betas:
								first_betas[beta] = self.first_producao(beta)

							if epsilon_vt in first_betas[beta]:
								novo_follow = follows[simbolo].union(follow_gerador)
								if follows[simbolo].symmetric_difference(novo_follow):
									follows[simbolo] = novo_follow
									houve_mudanca = True

		self.__follow_memo = follows
		return self.__follow_memo

	def first_nt(self):
		if self.__first_nt_memo is not None:
			return self.__first_nt_memo

		firsts_nt = OrderedDict()
		firsts = self.first()
		epsilon_vt = Vt(epsilon)
		houve_mudanca = True
		while houve_mudanca:
			houve_mudanca = False
			for vn in self.__conjunto_producoes:
				if vn not in firsts_nt:
					firsts_nt[vn] = set()
				for producao in self.__conjunto_producoes[vn]:
					derivacao = producao.get_derivacao()
					for simbolo in derivacao:
						if isinstance(simbolo, Vn):
							firsts_nt[vn].add(simbolo)
							if epsilon_vt not in firsts[simbolo]:
								break
						else:
							break

		self.__first_nt_memo = firsts_nt
		return self.__first_nt_memo

		pass
		# TODO
		# Deve:
		#   - Retornar o conjunto de First-NT de vn

	def esta_fatorada(self):
		for vn in self.__nao_terminais:
			firsts_das_derivacoes = set()
			for producao in self.__conjunto_producoes[vn]:
				first_producao = self.first_producao(producao)
				if firsts_das_derivacoes.intersection(first_producao):
					return False
				else:
					firsts_das_derivacoes = firsts_das_derivacoes.union(first_producao)
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
