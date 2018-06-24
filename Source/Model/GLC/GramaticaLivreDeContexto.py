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
			sem_epsilon = GLCEditavel(self)
			ne = self.obtem_ne()  # Símbolos que derivam &

			for A in self._nao_terminais:
				producoes = self._conjunto_producoes[A]
				for x in producoes:
					indices = []
					prod = x.get_derivacao()
					if Vt("&") in prod:
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
			prod = Producao(self._vn_inicial, [Vt("&")])
			sem_epsilon.adiciona_producao(self._vn_inicial, prod)

		glc = sem_epsilon.obter_glc_padrao(self.get_nome() + " (& livre)")
		return glc, ne

	def eh_epsilon_livre(self):
		ne = self.obtem_ne()
		return not bool(ne)  # bool() retorna falso o conjunto for vazio

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
		"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
		return chain.from_iterable(combinations(lista, r) for r in range(len(lista) + 1))

	def remove_simples(self):
		if not self.existe_producoes_simples():
			raise OperacaoError(" a gramática não possui nenhuma produção simples")
		else:
			# TODO
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

		return n

	def remove_inferteis(self):
		if not self.existe_inferteis():
			raise OperacaoError(" a gramática não possui nenhuma produção infértil")
		else:
			sem_inferteis = GLCEditavel(self)
			nf = self.obtem_nf()  # Símbolos férteis
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
							firsts_nt[vn].add(simbolo)
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
