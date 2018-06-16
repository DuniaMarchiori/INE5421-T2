# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Model import Model
from Source.View.View import View

from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *
from Source.Model.Exceptions.OperacaoError import *
from Source.Model.Exceptions.VnError import *

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
			glcs_criadas = self.__model.remover_recursao(elemento)
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
			# TODO ver como vai mostrar os conjuntos (ne, na, nf e vi)
			glcs_criadas, conjuntos = self.__model.transformar_em_propria(elemento)
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
			# TODO ver como vai mostrar o conjunto (ne)
			glc_criada, ne = self.__model.transformar_epsilon_livre(elemento)
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
			# TODO ver como vai mostrar o conjunto (na)
			glc_criada, na = self.__model.remover_simples(elemento)
			self.__adicionar_multiplos_elementos(glc_criada)
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
			# TODO ver como vai mostrar os conjuntos (nf e vi)
			glcs_criadas, conjuntos = self.__model.remover_inuteis(elemento)
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
			# TODO ver como vai mostrar o conjunto (nf)
			glc_criada, nf = self.__model.remover_inferteis(elemento)
			self.__adicionar_multiplos_elementos(glc_criada)
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
			# TODO ver como vai mostrar o conjunto (vi)
			glc_criada, vi = self.__model.remover_inalcancaveis(elemento)
			self.__adicionar_multiplos_elementos(glc_criada)
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
		Obtem o First do Vn passado por parâmetro.
		\:param indice é o índice da GLC na lista.
		\:param vn é o simbolo pertencente à Vn cujo First será calculado.
	'''
	def cb_propriedade_first(self, indice, vn):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			first = self.__model.calcular_first(elemento, vn)
			self.__view.mostrar_aviso("O First de " + vn + " é: {" + ', '.join(first) + "}", titulo="First")
		except VnError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Obtem o Follow do Vn passado por parâmetro.
		\:param indice é o índice da GLC na lista.
		\:param vn é o simbolo pertencente à Vn cujo Follow será calculado.
	'''
	def cb_propriedade_follow(self, indice, vn):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			follow = self.__model.calcular_follow(elemento, vn)
			self.__view.mostrar_aviso("O Follow de " + vn + " é: {" + ', '.join(follow) + "}", titulo="Follow")
		except VnError as e:
			self.__view.mostrar_aviso(e.get_message())
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")

	'''
		Obtem o First-NT do Vn passado por parâmetro.
		\:param indice é o índice da GLC na lista.
		\:param vn é o simbolo pertencente à Vn cujo First será calculado.
	'''
	def cb_propriedade_first_nt(self, indice, vn):
		elemento = self.__model.obter_elemento_por_indice(indice)
		try:
			first_nt = self.__model.calcular_first_nt(elemento, vn)
			self.__view.mostrar_aviso("O First-NT de " + vn + " é: {" + ', '.join(first_nt) + "}", titulo="First-NT")
		except VnError as e:
			self.__view.mostrar_aviso(e.get_message())
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
			fatoravel = self.__model.verificar_fatoravel(elemento, n)
			if fatoravel:
				self.__view.mostrar_aviso("Esta GLC é fatorável em " + str(n) + " passos.", titulo="Fatorável")
			else:
				self.__view.mostrar_aviso("Esta GLC não é fatorável em " + str(n) + " passos.", titulo="Fatorável")
		except:
			self.__view.mostrar_aviso("Erro ao verificar a propriedade.")
