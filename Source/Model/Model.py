# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Elemento import *
from Source.Model.ListaElementos import *
from Source.Model.GLC.GramaticaLivreDeContexto import *
from Source.Model.FileManager.FileManager import *
from Source.Model.Exceptions.OperacaoError import *

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

    '''
        Obtem o elemento correspondente ao indice passado.
        \:param indice é o índice do elemento na lista.
        \:return o elemento naquele indice.
    '''
    def obter_elemento_por_indice(self, indice):
        return self.__lista_de_elementos.get_elemento(indice)

    def reposiciona_elemento_editado(self, indice):
        self.__lista_de_elementos.reposiciona_elemento_editado(indice)

    '''
        Método que recebe um nome e a entrada de uma gramática e a retorna.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
    '''
    def criar_gramatica(self, nome, entrada):
        glc = GramaticaLivreDeContexto(nome)
        glc.parse(entrada)
        return glc

    # Operações

    '''
        Método que remove recursão à esquerda de uma gramática.
        \:param gramatica é a gramática cujas recursões à esquerda serão removidas.
        \:return a gramática sem recursões à esquerda e todas as gramáticas intermediárias
    '''
    def remover_recursao(self, gramatica):
        if not gramatica.existe_recursao_esq():
            raise OperacaoError("a gramática não possúi nenhuma recursão à esquerda")
        else:
            resultantes = []

            propria, conjuntos = self.transformar_em_propria(gramatica)
            resultantes.extend(propria)

            sem_recursao = propria[-1].remove_recursao_esq()
            resultantes.append(sem_recursao)

            return resultantes

    '''
        Método que transforma uma gramática em própria
        \:param gramatica é a gramática que será transformada em propria.
        \:return a gramática propria e todas as gramáticas intermediárias
        \:return os conjuntos Ne, NA, NF e Vi
    '''
    def transformar_em_propria(self, gramatica):
        if gramatica.eh_propria():
            raise OperacaoError("a gramática já é própria")
        else:
            resultantes = []
            conjuntos = []

            epsilon_livre, ne = self.transformar_epsilon_livre(gramatica)
            resultantes.append(epsilon_livre)
            conjuntos.append(ne)

            sem_simples, na = self.remover_simples(epsilon_livre)
            resultantes.append(sem_simples)
            conjuntos.append(na)

            sem_inuteis, nf_vi = self.remover_inuteis(sem_simples)
            resultantes.extend(sem_inuteis)
            conjuntos.extend(nf_vi)

            propria = sem_inuteis[-1]
            propria.set_nome(gramatica.get_nome() + " (própria)")

            return resultantes, conjuntos

    '''
        Método que transforma uma gramática em epsilon-livre
        \:param gramatica é a gramática que será transformada em epsilon-livre.
        \:return a gramática epsilon-livre
        \:return o conjunto Ne
    '''
    def transformar_epsilon_livre(self, gramatica):
        if gramatica.eh_epsilon_livre():
            raise OperacaoError("a gramática já é epsilon-livre")
        else:
            nova_gramatica, ne = gramatica.transforma_epsilon_livre()
            return nova_gramatica, ne

    '''
        Método que remove produções simples de uma gramática.
        \:param gramatica é a gramática cujas produções simples serão removidas.
        \:return a gramática sem produções simples
        \:return o conjunto NA
    '''
    def remover_simples(self, gramatica):
        if not gramatica.existe_producoes_simples():
            raise OperacaoError("a gramática não possúi produções simples")
        else:
            nova_gramatica, na = gramatica.remove_simples()
            return nova_gramatica, na

    '''
        Método que remove produções inúteis de uma gramática.
        \:param gramatica é a gramática cujas produções inférteis serão removidas.
        \:return a gramática sem produções inúteis e todas as gramáticas intermediárias
        \:return os conjuntos NF e Vi
    '''
    def remover_inuteis(self, gramatica):
        if not gramatica.existem_inuteis():
            raise OperacaoError("a gramática não possúi produções inúteis")
        else:
            resultantes = []
            conjuntos = []

            sem_infertil, nf = self.remover_inferteis(gramatica)
            resultantes.append(sem_infertil)
            conjuntos.append(nf)

            sem_inalcancavel, vi = self.remover_inalcancaveis(sem_infertil)
            sem_inalcancavel.set_nome(gramatica.get_nome() + " (sem inúteis)")
            resultantes.append(sem_inalcancavel)
            conjuntos.append(vi)

            return resultantes, conjuntos

    '''
        Método que remove produções inférteis de uma gramática.
        \:param gramatica é a gramática cujas produções inférteis serão removidas.
        \:return a gramática sem produções inférteis
        \:return o conjunto NF
    '''
    def remover_inferteis(self, gramatica):
        if not gramatica.existe_inferteis():
            raise OperacaoError("agramática não possúi produções inférteis")
        else:
            nova_gramatica, nf = gramatica.remove_inferteis()
            return nova_gramatica, nf

    '''
        Método que remove produções inalcançáveis de uma gramática.
        \:param gramatica é a gramática cujas produções inalcançáveis serão removidas.
        \:return a gramática sem produções inalcançáveis
        \:return o conjunto Vi
    '''
    def remover_inalcancaveis(self, gramatica):
        if not gramatica.existe_inalcancavel():
            raise OperacaoError("a gramática não possúi produções inalcançáveis")
        else:
            nova_gramatica, vi = gramatica.remove_inalcancaveis()
            return nova_gramatica, vi

    # Propriedades

    '''
        Método que verifica a finitude de uma gramática.
        \:param gramatica é a gramática cuja finitude será analizada.
    '''
    def verificar_finitude(self, gramatica):
        return gramatica.finitude()

    '''
        Método que calcula o First de um Vn qualquer de uma gramática.
        \:param gramatica onde vn se encontra.
        \:param vn é o simbolo pertencente à Vn cujo First será calculado.
    '''
    def calcular_first(self, gramatica, vn):
        obj_vn = None
        # obj_vn = Vn(vn) TODO
        return gramatica.first(obj_vn)

    '''
        Método que calcula o Follow de um Vn qualquer de uma gramática.
        \:param gramatica onde vn se encontra.
        \:param vn é o simbolo pertencente à Vn cujo Follow será calculado.
    '''
    def calcular_follow(self, gramatica, vn):
        obj_vn = None
        # obj_vn = Vn(vn) TODO
        return gramatica.follow(obj_vn)

    '''
        Método que calcula o First-NT de um Vn qualquer de uma gramática.
        \:param gramatica onde vn se encontra.
        \:param vn é o simbolo pertencente à Vn cujo First-NT será calculado.
    '''
    def calcular_first_nt(self, gramatica, vn):
        obj_vn = None
        # obj_vn = Vn(vn) TODO
        return gramatica.first_nt(obj_vn)

    '''
        Método que verifica se uma gramática está fatorada.
        \:param gramatica é a gramática cuja fatoração será analizada.
    '''
    def verificar_fatorada(self, gramatica):
        return gramatica.esta_fatorada()

    '''
        Método que verifica se uma gramática é fatorável em n passos.
        \:param gramatica é a gramática cuja fatorabilidade em n passos será analizada.
        \:param n é o numero de passos da tentativa de fatoração.
    '''
    def verificar_fatoravel(self, gramatica, n):
        return gramatica.eh_fatoravel_em_n_passos(n)
