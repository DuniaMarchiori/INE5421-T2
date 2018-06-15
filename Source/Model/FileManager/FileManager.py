# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

import os.path

'''
    Classe responsável por salvar e carregar arquivos.
'''
class FileManager:
    
    '''
        Salva um texto em um arquivo .txt.
        \:param nome é o nome do arquivo a ser salvo.
        \:param conteudo é a string contendo o texto que se quer salvar.
    '''
    def salvar(self, caminho, conteudo):
        file = open(caminho, "w")
        file.write(conteudo)
        file.close()

    '''
        Carrega o texto de um arquivo.
        \:param caminho_arquivo é o caminho do arquivo a ser lido.
        \:return o conteúdo do arquivo
    '''
    def abrir(self, caminho_arquivo):
        file = open(caminho_arquivo, "r")
        texto = file.read()
        file.close()
        return texto

    '''
        Obtem o nome do arquivo no caminho especificado.
        \:param caminho_arquivo é o caminho do arquivo.
        \:return o nome do arquivo
    '''
    def nome_do_arquivo(self, caminho_arquivo):
        nome, extensao = os.path.splitext(os.path.basename(caminho_arquivo))
        return nome
