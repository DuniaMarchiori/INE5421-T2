from Source.Model.GLC.GramaticaLivreDeContexto import *


'''
	Classe que representa uma gramática livre de contexto com alguns métodos à mais,
	que permitem sua edição. Porém é instável, pois pode possuir não terminais não definidos, vindos do fato de que essa
	classe deve ser utilizada durante o processo de criação de uma nova GLC em código.
	Após sua GLC estiver construída obtenha uma GLC padrão pelo método "obter_glc_padrao()"
'''
class GLCEditavel(GramaticaLivreDeContexto):

	def __init__(self, nome=None, base=None):
		if nome is None:
			nome_final = base.get_nome()
		else:
			nome_final = nome

		if base is None:
			base_final = ""
		else:
			base_final = base.to_string()

		super(GLCEditavel, self).__init__(nome_final, base_final)

	def set_inicial(self, novo_inicial):
		if not isinstance(novo_inicial, Vn) or not self.vn_pertence(novo_inicial):
			raise Exception("Erro Interno")

		self.__vn_inicial = novo_inicial

	def remove_producao(self, gerador, producao):
		if not isinstance(producao, Producao) or not self.vn_pertence(gerador):
			raise Exception("Erro Interno")

		producoes = self.__conjunto_producoes[gerador]
		producoes.remove(producao)
		if not producoes:
			self.__conjunto_producoes.pop(gerador, None)

	def adiciona_producao(self, gerador, producao):
		if not isinstance(producao, Producao) or not self.vn_pertence(gerador) or gerador != producao.get_gerador():
			raise Exception("Erro Interno")

		if not self.vn_pertence(gerador):
			self.__conjunto_producoes[gerador] = set()
			self.__nao_terminais.add(gerador)
		self.__conjunto_producoes[gerador].add(producao)
		for unidade in producao.get_derivacao():
			self.__terminais.add(unidade)

	def obter_glc_padrao(self):
		return GramaticaLivreDeContexto(self.get_nome(), self.to_string())
