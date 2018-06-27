# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Model import Model
from Source.View.View import View

from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *
from Source.Model.Exceptions.OperacaoError import *
from Source.Model.Exceptions.VnError import *

from Source.Model.Exceptions.OperacaoError import OperacaoError

'''
	Controller do padrão MVC.
'''
class Controller:

	__model = None  # Fachada do modelo
	__view = None  # Tela principal da aplicação

	'''
	   Método construtor.
	'''
	def __init__(self):
		self.__model = Model()  # Fachada do modelo
		self.__view = View(self)  # Tela principal da aplicação
		self.__view.start()

	def __adicionar_multiplos_elementos(self, lista_de_elementos):
		for elemento in lista_de_elementos:
			self.__adicionar_unico_elemento(elemento)

	def __adicionar_unico_elemento(self, elemento):
		self.__model.adicionar_elemento_na_lista(elemento)
		self.__view.adicionar_elemento_na_lista(elemento.get_nome(), elemento.get_tipo())

	def __representacao_textual_de_conjunto(self, nome_conjunto, conjunto):
		representacao = nome_conjunto + " = {"
		for simbolo in conjunto:
			representacao += str(simbolo) + ", "
		if conjunto:
			representacao = representacao[:-2]
		representacao += "}"
		return representacao

	# Callbacks da interface

	'''
		Método que recebe um nome e a entrada de uma gramática e a adiciona no sistema, mostrando erro caso aconteça.
		\:param nome é o nome da gramática que será criada.
		\:param entrada é a representação textual da gramática.
		\:return True se a operação foi bem sucedida, False caso contrário.
	'''
	def cb_nova_gramatica(self, nome, entrada):
		try:
			glc = self.__model.criar_gramatica(nome, entrada)
			self.__adicionar_unico_elemento(glc)
			return True
		except ParsingError as e:
			self.__view.mostrar_aviso(e.get_message())
			return False
		except Exception:
			self.__view.mostrar_aviso("Erro ao criar gramática.")
			return False

	'''
		Método que recebe um índice e remove esse objeto da lista.
		\:param indice é o índice do elemento na lista.
	'''
	def cb_remover_elemento(self, indice):
		self.__model.remover_elemento(indice)
		self.__view.remover_elemento_da_lista(indice)

	'''
		Método que é chamado ao alterar o elemento selecionado na lista.
		\:param indice é o índice do elemento na lista.
	'''
	def cb_alterar_elemento_selecionado(self, indice):
		elemento = None
		if indice is not None:
			elemento = self.__model.obter_elemento_por_indice(indice)
		self.__view.atualiza_elemento_selecionado(indice, elemento)

	'''
		Altera um elemento.
		\:param indice é o índice do elemento na lista.
	'''
	def cb_alterar_elemento(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			sucesso = self.__view.abrir_janela_edicao_de_elemento(elemento.get_nome(), elemento.to_string())
			if sucesso:
				self.__view.reposiciona_elemento_editado(indice)
				self.__model.reposiciona_elemento_editado(indice)
				self.cb_alterar_elemento_selecionado(indice)
		except Exception:
			self.__view.mostrar_aviso("O elemento não foi alterado.")

	def cb_duplica_elemento(self, indice):
		copia = self.__model.duplicar(indice)
		self.__adicionar_unico_elemento(copia)

	# Callbacks das Operações

	'''
		Remove recursão à esquerda.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_remover_recursao_esq(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glcs_criadas, recursoes_diretas, recursoes_indiretas = self.__model.remover_recursao(elemento)
			mensagem = "As recursões diretas são:\n"
			for simbolo in recursoes_diretas:
				for producao in recursoes_diretas[simbolo]:
					mensagem += str(simbolo) + " ->" + str(producao) + "\n"
			mensagem += "\nAs recursões indiretas são:\n"
			for simbolo in recursoes_indiretas:
				for producao in recursoes_indiretas[simbolo]:
					mensagem += str(simbolo) + " ->" + str(producao) + "\n"

			self.__view.mostrar_aviso(mensagem, titulo="Recursões")
			self.__adicionar_multiplos_elementos(glcs_criadas)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Transforma a gramática em própria.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_propria(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glcs_criadas, conjuntos = self.__model.transformar_em_propria(elemento)
			ne = conjuntos[0]
			na = conjuntos[1]
			nf = conjuntos[2]
			vi = conjuntos[3]
			mensagem = "O conjunto Ne dessa gramática é:\n" + self.__representacao_textual_de_conjunto("Ne", ne)
			mensagem += "\n\nOs conjuntos NA da gramática &-livre são:\n"
			for simbolo in na:
				mensagem += "N" + self.__representacao_textual_de_conjunto(simbolo.get_simbolos(), na[simbolo]) + "\n"
			mensagem += "\nO conjunto NF da gramática com as produções simples removidas é:\n" + self.__representacao_textual_de_conjunto("NF", nf)
			mensagem += "\n\nO conjunto Vi da gramática com os inférteis removidos é:\n" + self.__representacao_textual_de_conjunto("Vi", vi)

			self.__view.mostrar_aviso(mensagem, titulo="Conjuntos Ne, NA, NF e Vi")
			self.__adicionar_multiplos_elementos(glcs_criadas)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Transforma a gramática em epsilon-livre.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_epsilon(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glc_criada, ne = self.__model.transformar_epsilon_livre(elemento)
			ne_string = "O conjunto Ne dessa gramática é:\n" + self.__representacao_textual_de_conjunto("Ne", ne)
			self.__view.mostrar_aviso(ne_string, titulo="Conjunto Ne")
			self.__adicionar_unico_elemento(glc_criada)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Remove produções simples.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_simples(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glc_criada, na = self.__model.remover_simples(elemento)
			mensagem = "Os conjuntos NA dessa gramática são:\n"
			for simbolo in na:
				mensagem += self.__representacao_textual_de_conjunto(simbolo.get_simbolos(), na[simbolo]) + "\n"
			self.__view.mostrar_aviso(mensagem, titulo="Conjuntos NA")
			self.__adicionar_unico_elemento(glc_criada)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Remove produções inúteis.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_inuteis(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glcs_criadas, conjuntos = self.__model.remover_inuteis(elemento)
			vi = conjuntos[0]
			nf = conjuntos[1]
			mensagem = "O conjunto Vi dessa gramática é:\n" + self.__representacao_textual_de_conjunto("Vi", vi)
			mensagem += "\n\nO conjunto NF da gramática com os inférteis removidos é:\n" + self.__representacao_textual_de_conjunto("NF", nf)
			self.__view.mostrar_aviso(mensagem, titulo="Conjuntos Vi e NF")
			self.__adicionar_multiplos_elementos(glcs_criadas)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Remove produções inférteis.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_inferteis(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glc_criada, nf = self.__model.remover_inferteis(elemento)
			nf_string = "O conjunto NF dessa gramática é:\n" + self.__representacao_textual_de_conjunto("NF", nf)
			self.__view.mostrar_aviso(nf_string, titulo="Conjunto NF")
			self.__adicionar_unico_elemento(glc_criada)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	'''
		Remove produções inalcançáveis.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_operacao_inalcancaveis(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			glc_criada, vi = self.__model.remover_inalcancaveis(elemento)
			vi_string = "O conjunto Vi dessa gramática é:\n" + self.__representacao_textual_de_conjunto("Vi", vi)
			self.__view.mostrar_aviso(vi_string, titulo="Conjunto Vi")
			self.__adicionar_unico_elemento(glc_criada)
		except OperacaoError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao realizar a operação.")

	# Callbacks das Propriedades

	'''
		Verifica se a GLC é vazia, finita ou infinita.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_propriedade_finitude(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			resultado = self.__model.verificar_finitude(elemento)
			if resultado == 0:
				self.__view.mostrar_aviso("A GLC é Vazia.", titulo="Finitude")
			elif resultado == 1:
				self.__view.mostrar_aviso("A GLC é Finita.", titulo="Finitude")
			elif resultado == 2:
				self.__view.mostrar_aviso("A GLC é Infinita.", titulo="Finitude")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Obtem o First de uma gramática.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_propriedade_first(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			first = self.__model.calcular_first(elemento)
			self.__view.mostrar_aviso("O first dessa GLC é:\n" + str(first), titulo="First")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Obtem o Follow de uma gramática.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_propriedade_follow(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			follow = self.__model.calcular_follow(elemento)
			self.__view.mostrar_aviso("O follow dessa GLC é:\n" + str(follow), titulo="Follow")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Obtem o First-NT de uma gramática.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_propriedade_first_nt(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			first_nt = self.__model.calcular_first_nt(elemento)
			self.__view.mostrar_aviso("O first-nt dessa GLC é:\n" + str(first_nt), titulo="First-NT")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Verifica se a GLC está fatorada ou não.
		\:param indice é o índice da GLC na lista.
	'''
	def cb_propriedade_fatorada(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			fatorada = self.__model.verificar_fatorada(elemento)
			if fatorada:
				self.__view.mostrar_aviso("Esta GLC está fatorada.", titulo="Fatorada")
			else:
				self.__view.mostrar_aviso("Esta GLC não está fatorada.", titulo="Fatorada")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Verifica se uma GLC é fatorável em n passos.
		\:param indice é o índice da GLC na lista.
		\:param n é o número de passos máximo para verificar se é fatoravel.
	'''
	def cb_propriedade_fatoravel(self, indice, n):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			n = int(n)
			fatoravel, glc_criada = self.__model.verificar_fatoravel(elemento, n)
			if fatoravel:
				self.__view.mostrar_aviso("Esta GLC é fatorável em " + str(n) + " passos.", titulo="Fatorável")
				self.__adicionar_unico_elemento(glc_criada)
			else:
				self.__view.mostrar_aviso("Esta GLC não é fatorável em " + str(n) + " passos.", titulo="Fatorável")
		except ValueError:
			self.__view.mostrar_aviso("N deve ser um número inteiro.")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")
