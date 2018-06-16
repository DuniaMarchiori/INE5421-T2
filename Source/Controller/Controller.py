# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Model import Model
from Source.View.View import View

from Source.Model.GLC.Artifacts.Exceptions.ParsingError import *

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
	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
	def cb_remover_elemento(self, indice):
		self.__model.remover_elemento(indice)
		self.__view.remover_elemento_da_lista(indice)

	'''
		Método que é chamado ao alterar o elemento selecionado na lista.
		\:param indice é o índice do elemento na lista.
	'''
	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
	def cb_alterar_elemento_selecionado(self, indice):
		elemento = None
		if indice is not None:
			elemento = self.__model.obter_elemento_por_indice(indice)
		self.__view.atualiza_elemento_selecionado(indice, elemento)

	'''
		Altera um elemento.
		\:param indice é o índice do autômato na lista.
		\:param tamanho é o tamanho das sentenças que serão enumeradas.
	'''
	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
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

	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
	def cb_duplica_elemento(self, indice):
		copia = self.__model.duplicar(indice)
		self.__adicionar_unico_elemento(copia)

	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
	def cb_salvar_elemento(self, indice):
		elemento = self.__model.obter_elemento_por_indice(indice)
		caminho = self.__view.salvar_arquivo(elemento.get_nome())
		resultado = self.__model.salvar_elemento(caminho, indice)
		if resultado:
			self.__view.mostrar_aviso("Elemento salvo com sucesso.", titulo="Sucesso")
		else:
			self.__view.mostrar_aviso("Falha ao salvar arquivo.")

	# NÃO ADAPTADO. VERIFICAR O QUE PRECISA SER ADAPTADO
	def cb_carregar_gr(self, caminho):
		try:
			conteudo = self.__model.carregar_elemento(caminho)
			nome_elemento = self.__model.nome_arquivo(caminho)
			resultado = self.cb_nova_gramatica(nome_elemento, conteudo)
			if resultado:
				self.__view.mostrar_aviso("Gramática carregada com sucesso.", titulo="Sucesso")
		except Exception:
			self.__view.mostrar_aviso("Erro ao carregar arquivo.")
