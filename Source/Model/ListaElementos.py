# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

class ListaElementos:

    __lista_de_elementos = None

    def __init__(self):
        self.__lista_de_elementos = []

    def adiciona_elemento(self, elemento):
        self.__lista_de_elementos.append(elemento)

    def remove_elemento(self, indice):
        self.__lista_de_elementos.pop(indice)

    def get_elemento(self, indice):
        return self.__lista_de_elementos[indice]

    def reposiciona_elemento_editado(self, indice):
        novo = self.__lista_de_elementos.pop()
        self.__lista_de_elementos[indice] = novo