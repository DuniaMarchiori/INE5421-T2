# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from Source.Model.Elemento import *
from Source.Model.ListaElementos import *
from Source.Model.GLC.GramaticaLivreDeContexto import *
from Source.Model.FileManager.FileManager import *

from Source.Model.Exceptions.OperacaoError import *
from Source.Model.Exceptions.VnError import *

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
        glc = GramaticaLivreDeContexto(nome, entrada)
        return glc

    # Operações

    '''
        Método que remove recursão à esquerda de uma gramática.
        \:param gramatica é a gramática cujas recursões à esquerda serão removidas.
        \:return a gramática sem recursões à esquerda e todas as gramáticas intermediárias
    '''
    def remover_recursao(self, gramatica):
        if not gramatica.existe_recursao_esq():
            raise OperacaoError("a gramática não possui nenhuma recursão à esquerda")
        else:
            resultantes = []

            try:
                propria, conjuntos = self.transformar_em_propria(gramatica)
                resultantes.extend(propria)
            except OperacaoError as e:
                propria = [gramatica]

            sem_recursao, recursoes_diretas, recursoes_indiretas = propria[-1].remove_recursao_esq()
            resultantes.append(sem_recursao)

            return resultantes, recursoes_diretas, recursoes_indiretas

    '''
        Método que transforma uma gramática em própria
        \:param gramatica é a gramática que será transformada em propria.
        \:return a gramática propria e todas as gramáticas intermediárias
        \:return os conjuntos Ne, NA, NF e Vi
    '''
    def transformar_em_propria(self, gramatica):
        if gramatica.eh_propria():
            raise OperacaoError(" a gramática já é própria")
        else:
            resultantes = []
            conjuntos = []

            try:
                epsilon_livre, ne = self.transformar_epsilon_livre(gramatica)
                resultantes.append(epsilon_livre)
                conjuntos.append(ne)
            except OperacaoError as e:
                epsilon_livre = gramatica
                conjuntos.append(epsilon_livre.obtem_ne())

            try:
                sem_simples, na = self.remover_simples(epsilon_livre)
                resultantes.append(sem_simples)
                conjuntos.append(na)
            except OperacaoError as e:
                sem_simples = epsilon_livre
                conjuntos.append(sem_simples.obtem_na())

            try:
                sem_inuteis, nf_vi = self.remover_inuteis(sem_simples)
                resultantes.extend(sem_inuteis)
                conjuntos.extend(nf_vi)
            except OperacaoError as e:
                sem_inuteis = [sem_simples]
                conjuntos.extend([sem_simples.obtem_nf(), sem_simples.obtem_vi()])

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
            raise OperacaoError(" a gramática já é epsilon-livre")
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
            raise OperacaoError(" a gramática não possui produções simples")
        elif not gramatica.eh_epsilon_livre():
            raise OperacaoError(" a gramática deve ser epsilon-livre")
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
            raise OperacaoError(" a gramática não possui produções inúteis")
        else:
            resultantes = []
            conjuntos = []

            try:
                sem_infertil, nf = self.remover_inferteis(gramatica)
                resultantes.append(sem_infertil)
                conjuntos.append(nf)
            except OperacaoError as e:
                sem_infertil = gramatica
                conjuntos.append(sem_infertil.obtem_nf())

            try:
                sem_inalcancavel, vi = self.remover_inalcancaveis(sem_infertil)
                conjuntos.append(vi)
            except OperacaoError as e:
                sem_inalcancavel = sem_infertil
                conjuntos.append(sem_inalcancavel.obtem_vi())

            sem_inalcancavel.set_nome(gramatica.get_nome() + " (sem inúteis)")
            resultantes.append(sem_inalcancavel)

            return resultantes, conjuntos

    '''
        Método que remove produções inférteis de uma gramática.
        \:param gramatica é a gramática cujas produções inférteis serão removidas.
        \:return a gramática sem produções inférteis
        \:return o conjunto NF
    '''
    def remover_inferteis(self, gramatica):
        if not gramatica.existe_inferteis():
            raise OperacaoError(" a gramática não possui produções inférteis")
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
            raise OperacaoError(" a gramática não possui produções inalcançáveis")
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
        Método que calcula o First de uma gramática.
        \:param gramatica onde vn se encontra.
    '''
    def calcular_first(self, gramatica):
        firsts = gramatica.first()

        first_string = ""
        for vn in firsts:
            first_string += "First(" + str(vn) + ") = { "
            i = 0
            for first in firsts[vn]:
                first_string += str(first)
                if i < len(firsts[vn]) - 1:
                    first_string += ", "
                i += 1
            first_string += " }\n"
        return first_string

    '''
        Método que calcula o Follow de uma gramática.
        \:param gramatica onde vn se encontra.
    '''
    def calcular_follow(self, gramatica):
        follows = gramatica.follow()

        follow_string = ""
        for vn in follows:
            follow_string += "Follow(" + str(vn) + ") = { "
            i = 0
            for first in follows[vn]:
                follow_string += str(first)
                if i < len(follows[vn]) - 1:
                    follow_string += ", "
                i += 1
            follow_string += " }\n"
        return follow_string

    '''
        Método que calcula o First-NT de uma gramática.
        \:param gramatica onde vn se encontra.
    '''
    def calcular_first_nt(self, gramatica):
        firsts_nt = gramatica.first_nt()

        firsts_nt_string = ""
        for vn in firsts_nt:
            firsts_nt_string += "First-NT(" + str(vn) + ") = { "
            i = 0
            for first in firsts_nt[vn]:
                firsts_nt_string += str(first)
                if i < len(firsts_nt[vn]) - 1:
                    firsts_nt_string += ", "
                i += 1
            firsts_nt_string += " }\n"
        return firsts_nt_string

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
        if gramatica.existe_recursao_esq():
            raise OperacaoError(" a gramática possui derivações à esquerda")
        if n > 0:
            return gramatica.eh_fatoravel_em_n_passos(n)
        else:
            raise OperacaoError(" n deve ser um inteiro maior que zero")
