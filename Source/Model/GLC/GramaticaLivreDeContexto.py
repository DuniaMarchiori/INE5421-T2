from Source.Model.GLC.Artifacts.Constants import *
from Source.Model.GLC.Artifacts.Producao import *
from Source.Model.GLC.Artifacts.Vn import *
from Source.Model.GLC.Artifacts.Vt import *
from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *
from Source.Model.Exceptions.OperacaoError import *


from Source.Model.Elemento import *

from collections import OrderedDict
import re
from itertools import *

'''
	Classe que representa uma gramática livre de contexto.
'''
class GramaticaLivreDeContexto(Elemento):

	def __init__(self, nome, entrada):
		super(GramaticaLivreDeContexto, self).__init__(TipoElemento.GLC, nome)
		self._conjunto_producoes = OrderedDict()
		self._terminais = set()
		self._nao_terminais = set()
		self._vn_inicial = None
		self.__parse(entrada)
		self.__nf = None
		self.__vi = None
		self.__ne = None
		self.__na = None
		self.__first_memo = None
		self.__follow_memo = None
		self.__first_nt_memo = None

	def __parse(self, entrada):
		inicial_definido = False
		entrada_linhas = entrada.splitlines()
		num_linha = 0
		for linha in entrada_linhas:
			if linha:  # Se a linha não for em branco
				linha_limpa = re.sub("\s+", " ", linha)
				if simb_derivacao in linha_limpa:
					producao_lista = linha_limpa.split(simb_derivacao)
					if len(producao_lista) <= 2:
						produtor = self.__obtem_produtor(producao_lista[0], num_linha)
						if not inicial_definido:
							self._vn_inicial = produtor
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
		for vn in self._nao_terminais:
			if vn not in self._conjunto_producoes:
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
		self._nao_terminais.add(vn)
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
				self._nao_terminais.add(vn)
			elif primeiro_simbolo in (alfabeto_terminais + epsilon):
				vt = Vt(unidade)
				unidades_resultantes.append(vt)
				self._terminais.add(vt)
			else:
				raise ParsingError(": símbolo de Vt ou Vn esperado mas não encontrado")
		return unidades_resultantes

	def __adiciona_producao(self, vn, producao):
		if vn not in self._conjunto_producoes:
			self._conjunto_producoes[vn] = set()
		self._conjunto_producoes[vn].add(producao)

	def vn_pertence(self, vn):
		return vn in self._nao_terminais

	def vt_pertence(self, vt):
		return vt in self._terminais

	def remove_recursao_esq(self):
		if not self.existe_recursao_esq():
			raise OperacaoError(" a gramática não possui recursão à esquerda")
		elif not self.eh_propria():
			raise OperacaoError(" a gramática não é própria")
		else:
			recursoes_diretas = {}
			recursoes_indiretas = {}

			# Construir os conjuntos de recursões diretas e indiretas
			for vn in self._nao_terminais:
				for producao in self._conjunto_producoes[vn]:
					if self._eh_recursivo_direto(vn, producao):
						if vn not in recursoes_diretas:
							recursoes_diretas[vn] = set()
						recursoes_diretas[vn].add(producao)
					if self._eh_recursivo_indireto(vn, producao):
						if vn not in recursoes_indiretas:
							recursoes_indiretas[vn] = set()
						recursoes_indiretas[vn].add(producao)

			epsilon_vt = Vt(epsilon)
			glc_sem_recursao = GLCEditavel(self)
			vns_em_ordem = list(self._conjunto_producoes)
			for i in range(0, len(vns_em_ordem)):
				vni = vns_em_ordem[i]
				for j in range(0, i):
					vnj = vns_em_ordem[j]

					producoes_a_remover = []
					producoes_novas = []
					for producao in glc_sem_recursao._conjunto_producoes[vni]:
						if glc_sem_recursao._eh_recursivo_indireto(vni, producao):
							derivacao = producao.get_derivacao()
							for k in range(0, len(derivacao)):
								simbolo = derivacao[k]
								if simbolo == vnj:
									producoes_a_remover.append(producao)
									producoes_substituidas = glc_sem_recursao._substitui_vn_por_producao(producao, k)
									producoes_novas.extend(producoes_substituidas)
									break
								elif epsilon_vt not in glc_sem_recursao.first()[simbolo]:
									break
								elif isinstance(simbolo, Vt):
									break

					for producao in producoes_a_remover:
						glc_sem_recursao.remove_producao(vni, producao)
					for producao in producoes_novas:
						glc_sem_recursao.adiciona_producao(vni, producao)
				glc_sem_recursao = glc_sem_recursao._remove_recursao_direta(vni)

			glc_padrao = glc_sem_recursao.obter_glc_padrao(self.get_nome() + " (sem rec. esquerda)")
			return glc_padrao, recursoes_diretas, recursoes_indiretas
			pass
			# TODO
			# Fazer:
			#   - (Lembrete: Utilizar classe GLCEditavel pra construir a GLC resultante)
			#   - Obter quais não terminais possuem recursão à esquerda e pra cada um, se são recursões diretas ou indiretas
			#       - Essa estrutura pode ser um dicionário, onde as chaves são os não terminais e o valor é o tipo da recursividade
			#   - Cria uma nova GLC sem recursão à esquerda usando o algoritmo.
			#   - Retorna a GLC e também a estrutura dos terminais que possuem recursão


	def existe_recursao_esq(self):
		firsts_nt = self.first_nt()
		for vn in firsts_nt:
			if vn in firsts_nt[vn]:
				return True
		return False

	def _substitui_vn_por_producao(self, producao, posicao_do_vn):
		derivacao = producao.get_derivacao()
		gerador = producao.get_gerador()

		derivacao_pre = derivacao[:posicao_do_vn]
		vn = derivacao[posicao_do_vn]
		derivacao_pos = derivacao[posicao_do_vn+1:]
		producoes_geradas = []
		for producao in self._conjunto_producoes[vn]:
			nova_derivacao = derivacao_pre + producao.get_derivacao() + derivacao_pos
			nova_producao = Producao(gerador, nova_derivacao)
			producoes_geradas.append(nova_producao)

		return producoes_geradas

	def _remove_recursao_direta(self, vn):
		sem_recursao_direta = GLCEditavel(self)
		producoes_com_recursao = []
		producoes_sem_recursao = []
		for producao in sem_recursao_direta._conjunto_producoes[vn]:
			derivacao = producao.get_derivacao()
			for simbolo in derivacao:
				if isinstance(simbolo, Vt):
					producoes_sem_recursao.append(producao)
					break
				else:
					if simbolo == vn:
						producoes_com_recursao.append(producao)
						break
					elif Vt(epsilon) not in sem_recursao_direta.first()[simbolo]:
						producoes_sem_recursao.append(producao)
						break

		if producoes_com_recursao:
			sem_recursao_direta._conjunto_producoes[vn].clear()
			novo_vn = Vn(sem_recursao_direta.novo_simbolo(vn.get_simbolos()[0]))
			for producao in producoes_com_recursao:
				nova_derivacao = producao.get_derivacao()[1:] + [novo_vn]
				nova_producao = Producao(novo_vn, nova_derivacao)
				sem_recursao_direta.adiciona_producao(novo_vn, nova_producao)
			sem_recursao_direta.adiciona_producao(novo_vn, Producao(novo_vn, [Vt(epsilon)]))

			for producao in producoes_sem_recursao:
				nova_derivacao = producao.get_derivacao() + [novo_vn]
				nova_producao = Producao(vn, nova_derivacao)
				sem_recursao_direta.adiciona_producao(vn, nova_producao)

		return sem_recursao_direta

	def _eh_recursivo_direto(self, vn, producao):
		first = self.first()
		epsilon_vt = Vt(epsilon)
		derivacao = producao.get_derivacao()
		for simbolo in derivacao:
			if isinstance(simbolo, Vt):
				return False
			else:
				if simbolo == vn:
					return True
				elif epsilon_vt not in first[simbolo]:
					return False
		return False

	def _eh_recursivo_indireto(self, vn, producao):
		first_nt = self.first_nt()
		derivacao = producao.get_derivacao()
		for simbolo in derivacao:
			if isinstance(simbolo, Vt):
				return False
			else:
				if simbolo != vn and vn in first_nt[simbolo]:
					return True
		return False


	def transforma_epsilon_livre(self):
		if self.eh_epsilon_livre():
			raise OperacaoError(" a gramática já é epsilon-livre")
		else:
			sem_epsilon = GLCEditavel(self)
			ne = self.obtem_ne()  # Símbolos que derivam &

			for A in self._nao_terminais:
				producoes = self._conjunto_producoes[A]
				for x in producoes:
					indices = []
					prod = x.get_derivacao()
					if x.eh_epsilon():
						sem_epsilon.remove_producao(A, x)
					else:
						for y in prod:
							if y in ne:
								indices.append(prod.index(y))
						if len(prod) > 1 and len(indices) > 0:
							powerset = list(self.__powerset(indices))
							powerset.pop(0)  # Remove conjunto vazio
							for item in powerset:
								nova_prod = list(prod)
								index = ''.join(str(s) for s in list(item))
								index = int(index)
								nova_prod.pop(index)
								sem_epsilon.adiciona_producao(A, Producao(A, nova_prod))

		if self._vn_inicial in ne:
			novo_inicial = Vn(sem_epsilon.novo_simbolo(self._vn_inicial.get_simbolos()[0]))
			prod_s = Producao(novo_inicial, [self._vn_inicial])
			sem_epsilon.adiciona_producao(novo_inicial, prod_s)
			prod_epsilon = Producao(novo_inicial, [Vt(epsilon)])
			sem_epsilon.adiciona_producao(novo_inicial, prod_epsilon)
			sem_epsilon.set_inicial(novo_inicial)

		glc = sem_epsilon.obter_glc_padrao(self.get_nome() + " (& livre)")
		return glc, ne

	def eh_epsilon_livre(self):
		ne = self.obtem_ne()
		if not ne:
			return True
		elif ne == set([self._vn_inicial]):
			for vn in self._conjunto_producoes:
				for producao in self._conjunto_producoes[vn]:
					derivacao = producao.get_derivacao()
					for simbolo in derivacao:
						if simbolo == self._vn_inicial:
							return False
			return True
		else:
			return False


	def obtem_ne(self):
		if self.__ne is not None:
			return self.__ne

		ne = set()

		# Não terminais que derivam & diretamente
		for A in self._nao_terminais:
			producoes = self._conjunto_producoes[A]
			for prod in producoes:
				deriv = prod.get_derivacao()
				if len(deriv) == 1:
					x = deriv[0]
					if isinstance(x, Vt) and x.eh_epsilon():
						ne.add(A)
						break

		# Não terminais que derivam & indiretamente
		ne_atual = ()
		while ne_atual != ne:
			ne_atual = set(ne)
			for A in self._nao_terminais:
				i = 0
				producoes = self._conjunto_producoes[A]
				for x in producoes:
					prod = x.get_derivacao()
					for y in prod:
						if y in ne_atual:
							i += 1  # Conta quantos simbolos de uma produção derivam &
					if i == len(prod):  # Se todos derivam &, então A deriva & indiretamente
						ne.add(A)

		self.__ne = ne
		return self.__ne

	def __powerset(self, lista):
		# powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
		return chain.from_iterable(combinations(lista, r) for r in range(len(lista) + 1))

	def remove_simples(self):
		if not self.existe_producoes_simples():
			raise OperacaoError(" a gramática não possui nenhuma produção simples")
		else:
			na = self.obtem_na()

			sem_simples = GLCEditavel(self)
			# Remove produções simples
			for A in sem_simples._conjunto_producoes:
				producoes = list(sem_simples._conjunto_producoes[A])
				for derivacao in producoes:
					if derivacao.eh_simples():
						sem_simples.remove_producao(A, derivacao)

			# Adiciona produções
			for A in sem_simples._conjunto_producoes:
				for B in set(na[A]) - set([A]):
					for prod in sem_simples._conjunto_producoes[B]:
						sem_simples.adiciona_producao(A, Producao(A, list(prod.get_derivacao())))

			# Atualiza produções
			houve_mudança = True
			while houve_mudança:
				houve_mudança = False
				for A in sem_simples._conjunto_producoes:
					for B in set(na[A]) - set([A]):
						diff = set(sem_simples._conjunto_producoes[B]) - set(sem_simples._conjunto_producoes[A])
						if len(diff) > 0:
							for prod in diff:
								sem_simples.adiciona_producao(A, Producao(A, list(prod.get_derivacao())))
								houve_mudança = True

			glc = sem_simples.obter_glc_padrao(self.get_nome() + " (sem prod. simples)")
			return glc, na

	def existe_producoes_simples(self):
		for vn in self._conjunto_producoes:
			for derivacao in self._conjunto_producoes[vn]:
				if derivacao.eh_simples():
					return True
		return False

	def obtem_na(self):

		if self.__na is not None:
			return self.__na

		n = dict()

		# Inicializa conjuntos
		for A in self._nao_terminais:
			n[A] = [A]

		# Derivações diretas (A deriva B)
		for A in self._conjunto_producoes:
			for derivacao in self._conjunto_producoes[A]:
				if derivacao.eh_simples():
					n[A].extend(derivacao.get_derivacao())

		# Atualização das derivações (A deriva B que deriva C, logo, A deriva C)
		houve_mudança = True
		while houve_mudança:
			houve_mudança = False
			for A in self._conjunto_producoes:
				for prod in self._conjunto_producoes[A]:
					if prod.eh_simples():
						derivacao = prod.get_derivacao()[0]
						diff = set(n[derivacao]) - set(n[A])
						if len(diff) > 0:
							n[A].extend(diff)
							houve_mudança = True
		self.__na = n
		return self.__na

	def remove_inferteis(self):
		if not self.existe_inferteis():
			raise OperacaoError(" a gramática não possui nenhuma produção infértil")
		else:
			sem_inferteis = GLCEditavel(self)
			nf = self.obtem_nf()  # Símbolos férteis

			if self._vn_inicial not in nf:
				raise OperacaoError(" a gramática representa uma linguagem vazia")

			inferteis = self._nao_terminais.difference(nf)
			for simbolo in inferteis:
				sem_inferteis.remove_vn(simbolo)

			glc = sem_inferteis.obter_glc_padrao(self.get_nome() + " (sem inférteis)")
			return glc, inferteis

	def existe_inferteis(self):
		nf = self.obtem_nf()
		return bool(self._nao_terminais.difference(nf)) # Retorna falso se a diferença resulta em um conjunto vazio

	def obtem_nf(self):
		if self.__nf is not None:
			return self.__nf

		nf = set()
		nf_atual = set()
		continua = True
		nt = set(self._nao_terminais)

		while continua:
			nf = set(nf_atual)
			for A in nt:
				adicionado = False
				producoes = self._conjunto_producoes[A]
				for x in producoes:
					if not adicionado:
						prod = x.get_derivacao()
						for simbolo in prod:
							if any(simbolo not in nf_atual and simbolo not in self._terminais for simbolo in prod):
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
			sem_inalc = GLCEditavel(self)
			vi = self.obtem_vi() # Símbolos alcançáveis
			inalcancaveis = self._nao_terminais.difference(vi)
			for simbolo in inalcancaveis:
				sem_inalc.remove_vn(simbolo)

			glc = sem_inalc.obter_glc_padrao(self.get_nome() + " (sem inalcançáveis)")
			return glc, inalcancaveis

	def existe_inalcancavel(self):
		vi = self.obtem_vi()
		return bool(self._nao_terminais.difference(vi))  # Retorna falso se a diferença resulta em um conjunto vazio

	def obtem_vi(self):
		if self.__vi is not None:
			return self.__vi

		vi = set()
		vi_atual = set()
		vi_atual.add(self._vn_inicial)
		visitados = set()

		while vi != vi_atual:
			vi = set(vi_atual)
			for X in set(vi - visitados):
				visitados.add(X)
				producoes = self._conjunto_producoes[X]
				for y in producoes:
					prod = y.get_derivacao()
					vi_atual = vi_atual.union(set(self._nao_terminais.intersection(set(prod))))

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
		if self._vn_inicial not in ferteis:
			return 0
		elif self.__infinita():
			return 2
		else:
			return  1

	def __infinita(self):
		simbolos_uteis = self.obtem_nf().intersection(self.obtem_vi())
		for A in simbolos_uteis:
			producoes = self._conjunto_producoes[A]
			for x in producoes:
				prod = x.get_derivacao()
				contem_terminal = any(simbolo in self._terminais for simbolo in prod)
				if A in prod and contem_terminal:
					return True

				prox_deriv = set(self._nao_terminais.intersection(set(prod)))
				visitados = set([A])
				while any(simbolo not in visitados for simbolo in prox_deriv):
					for y in prox_deriv:
						visitados.add(y)
						producoes = self._conjunto_producoes[y]
						for z in producoes:
							prod = z.get_derivacao()
							if A in prod:
								contem_terminal = contem_terminal or any(simbolo in self._terminais for simbolo in prod)
								if contem_terminal:
									return True
					prox_deriv = set(self._nao_terminais.intersection(set(prod)))

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
			for vn in self._conjunto_producoes:
				if vn not in firsts:
					firsts[vn] = set()
				for producao in self._conjunto_producoes[vn]:
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
		for vn in self._conjunto_producoes:
			follows[vn] = set()
			if vn == self._vn_inicial:
				follows[vn].add(final_de_sentenca)

		# Passo 2
		first_betas = {}
		for vn in self._nao_terminais:
			for producao in self._conjunto_producoes[vn]:
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
			for vn in self._nao_terminais:
				follow_gerador = follows[vn]
				for producao in self._conjunto_producoes[vn]:
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
			for vn in self._conjunto_producoes:
				if vn not in firsts_nt:
					firsts_nt[vn] = set()
				for producao in self._conjunto_producoes[vn]:
					derivacao = producao.get_derivacao()
					for simbolo in derivacao:
						if isinstance(simbolo, Vn):
							if simbolo not in firsts_nt:
								firsts_nt[simbolo] = set()
							tam_anterior = len(firsts_nt[vn])
							firsts_nt[vn].add(simbolo)
							firsts_nt[vn] = firsts_nt[vn].union(firsts_nt[simbolo])
							tam_depois = len(firsts_nt[vn])
							if tam_depois > tam_anterior:
								houve_mudanca = True
							if epsilon_vt not in firsts[simbolo]:
								break
						else:
							break

		self.__first_nt_memo = firsts_nt
		return self.__first_nt_memo

	def esta_fatorada(self):
		for vn in self._nao_terminais:
			firsts_das_derivacoes = set()
			for producao in self._conjunto_producoes[vn]:
				first_producao = self.first_producao(producao)
				if firsts_das_derivacoes.intersection(first_producao):
					return False
				else:
					firsts_das_derivacoes = firsts_das_derivacoes.union(first_producao)
		return True

	def eh_fatoravel_em_n_passos(self, n):
		if self.esta_fatorada():
			raise OperacaoError(" a gramática já está fatorada")
		else:
			i = 0
			fatorada = GLCEditavel(self)
			nao_terminais = []
			nao_terminais.extend(self._nao_terminais)
			while nao_terminais:
				nt = nao_terminais[0]
				if not fatorada.__nt_esta_fatorado(fatorada, nt):
					if i < n:
						producoes = list(fatorada._conjunto_producoes[nt])
						j = 0
						firsts = []
						while j < len(producoes)-1:
							k = j + 1
							producao = producoes[j]
							first_prod = fatorada.first_producao(producao)
							if not(first_prod in firsts):  # Se esse first já não foi analizado
								outras_prod = []
								while k < len(producoes):
									prod = producoes[k]
									first_outra_prod = fatorada.first_producao(prod)
									if first_outra_prod not in firsts:
										intersec = first_prod.intersection(first_outra_prod)
										if intersec:
											firsts.extend(intersec)
											outras_prod.append(prod)
									k += 1
								if outras_prod:
									todas_producoes = list(set(outras_prod).union(set([producao])))
									novas_prod = []
									for x in todas_producoes:
										if len(x.get_derivacao()) > 0:
											simb = x.get_derivacao()[0]
											novas_prod.append(x)
											if not isinstance(simb, Vt):  # ND indireto
												prox_deriv = []
												prox_deriv.append(simb)
												while prox_deriv:
													outro_simb = prox_deriv[0]
													derivacao = fatorada._conjunto_producoes[outro_simb]

													indexes = []  # indices das produções com o nao terminal
													for y in novas_prod:
														if y.get_derivacao()[0] == outro_simb:
															indexes.append(novas_prod.index(y))

													for d in derivacao:
														for index in indexes:
															di = list(novas_prod[index].get_derivacao())
															di.pop(0)
															if di is None:
																di = []
															nova_deriv = []
															if not d.eh_epsilon() or di == list():
																nova_deriv = list(d.get_derivacao())
															nova_deriv.extend(di)
															novas_prod.append(Producao(novas_prod[index].get_gerador(), nova_deriv))
															if isinstance(nova_deriv[0], Vn):
																prox_deriv.append(nova_deriv[0])
													v = 0
													for index in indexes:
														if index-v < 0:
															novas_prod.pop(0)
														else:
															novas_prod.pop(index-v)
														v += 1
													prox_deriv.remove(outro_simb)

									# Commom substring
									a = 0
									b = 1
									commom_subtrings = set()
									removidos = set()
									while a < len(novas_prod):
										sa = str(novas_prod[a])
										b = a + 1
										while b < len(novas_prod):
											if a != b:
												start = self.__common_start(sa, str(novas_prod[b]))
												if start != '' and start != ' ':
													strings = set(commom_subtrings)
													if strings:
														for c in strings:
															com_sub = self.__common_start(c, start)
															if com_sub != '' and com_sub != ' ':
																commom_subtrings.add(com_sub)
																removidos.add(c)
															else:
																commom_subtrings.add(start)
													else:
														commom_subtrings.add(start)
											b += 1
										a += 1
									for r in removidos:
										commom_subtrings.remove(r)

									adicionar = list(novas_prod)
									for common_s in commom_subtrings:
										# Fatora
										simbolos = []
										common_s = common_s.replace(" ", "")
										for s in common_s:
											if s.islower():
												simbolos.append(Vt(s))
											else:
												simbolos.append(Vn(s))
										novo_nt = fatorada.novo_simbolo(str(nt)[0])
										novo_nt = Vn(novo_nt)
										simbolos.append(novo_nt)
										nao_terminais.append(novo_nt)
										fatorada.adiciona_nao_terminal(novo_nt)
										fatorada.adiciona_producao(nt, Producao(nt, simbolos))

										# Produções do novo não terminal
										fim_commom = len(common_s)
										for p in novas_prod:
											if p.get_derivacao()[0] == simbolos[0]:
												resto_prod = p.get_derivacao()[fim_commom:]
												if len(resto_prod) == 0:
													resto_prod = [Vt("&")]
												fatorada.adiciona_producao(novo_nt, Producao(novo_nt, resto_prod))
												adicionar.remove(p)

									for a in adicionar:
										fatorada.adiciona_producao(nt, Producao(nt, a.get_derivacao()))

									# Remover producoes não fatoradas anteriores
									for p in todas_producoes:
										fatorada.remove_producao(nt, p)

									i += 1  # Um passo feito
							j += 1
					else:
						return False, None
				nao_terminais.remove(nt)

			glc = fatorada.obter_glc_padrao(self.get_nome() + "(fatorada)")
			return True, glc

	def __nt_esta_fatorado(self, gramatica, nt):
		firsts_das_derivacoes = set()
		for producao in gramatica._conjunto_producoes[nt]:
			first_producao = gramatica.first_producao(producao)
			if firsts_das_derivacoes.intersection(first_producao):
				return False
			else:
				firsts_das_derivacoes = firsts_das_derivacoes.union(first_producao)
		return True

	def __common_start(self, sa, sb):
		# returns the longest common substring from the beginning of sa and sb
		def _iter():
			for a, b in zip(sa, sb):
				if a == b:
					yield a
				else:
					return

		return ''.join(_iter())

	def to_string(self):
		return self.__str__()

	def __str__(self):
		retorno = ""
		for produtor in self._conjunto_producoes:
			linha = str(produtor) + " " + simb_derivacao
			for producao in self._conjunto_producoes[produtor]:
				linha += str(producao) + " |"
			linha = linha[0:-2] + "\n"
			if produtor == self._vn_inicial:
				retorno = linha + retorno
			else:
				retorno += linha
		return retorno

# Imports colocados abaixo para contornar dependência circular
from Source.Model.GLC.Artifacts.GLCEditavel import GLCEditavel
