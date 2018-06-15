# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Elemento import *
from Source.Model.ListaElementos import *
from Source.Model.GLC.GramaticaLivreDeContexto import *
from Source.Model.FileManager.FileManager import *

from copy import deepcopy


'''
    Fachada do módulo model.
'''
class Model:

    __lista_de_elementos = None
    __file_manager = None

    def __init__(self):
        self.__lista_de_elementos = ListaElementos()
        self.__file_manager = FileManager()

    def adicionar_elemento_na_lista(self, elemento):
        self.__lista_de_elementos.adiciona_elemento(elemento)

    '''
        Método que recebe um nome e a entrada de uma gramática e o retorna.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
    '''
    def criar_gramatica(self, nome, entrada):
        glc = GramaticaLivreDeContexto(nome)
        glc.parse(entrada)
        return glc

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def remover_elemento(self, indice):
        self.__lista_de_elementos.remove_elemento(indice)

    '''
        Obtém uma cópia do elemento indicado.
        \:param indice é o índice do elemento na lista.
        \:return uma cópia do elemento requisitado.
    '''
    def duplicar(self, indice):
        elemento = self.obter_elemento_por_indice(indice)
        copia = deepcopy(elemento)
        copia.set_nome(copia.get_nome() + " (cópia)")
        return copia

    def operacao_glr(self, indice, operacao):
        gramatica_um = self.obter_elemento_por_indice(indice)

        if operacao == 0:  # União
            gramatica_resultante = gramatica_um.fechamento()
        elif operacao == 1:  # Concatenação
            gramatica_resultante = gramatica_um.fechamento()
        else:  # Fecho
            gramatica_resultante = gramatica_um.fechamento()

        return gramatica_resultante
    '''
        Obtem o elemento correspondente ao indice passado.
        \:param indice é o índice do elemento na lista.
        \:return o elemento naquele indice.
    '''
    def obter_elemento_por_indice(self, indice):
        return self.__lista_de_elementos.get_elemento(indice)

    def salvar_elemento(self, caminho, indice):
        if indice is not None:
            elemento = self.obter_elemento_por_indice(indice)
            try:
                self.__file_manager.salvar(caminho, elemento.to_string())
                return True
            except:
                return False
        else:
            return False

    def carregar_elemento(self, caminho):
        return self.__file_manager.abrir(caminho)

    def nome_arquivo(self, caminho):
        return self.__file_manager.nome_do_arquivo(caminho)

    def reposiciona_elemento_editado(self, indice):
        self.__lista_de_elementos.reposiciona_elemento_editado(indice)