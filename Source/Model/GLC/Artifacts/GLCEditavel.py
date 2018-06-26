from Source.Model.GLC.GramaticaLivreDeContexto import *


'''
	Classe que representa uma gramática livre de contexto com alguns métodos à mais,
	que permitem sua edição. Porém é instável, pois pode possuir não terminais não definidos, vindos do fato de que essa
	classe deve ser utilizada durante o processo de criação de uma nova GLC em código.
	Após sua GLC estiver construída obtenha uma GLC padrão pelo método "obter_glc_padrao()"
'''
class GLCEditavel(GramaticaLivreDeContexto):

	def __init__(self, base=None):
		if base is None:
			base_final = ""
			nome = ""
		else:
			base_final = base.to_string()
			nome = base.get_nome()

		super(GLCEditavel, self).__init__(nome, base_final)

	def set_inicial(self, novo_inicial):
		if not isinstance(novo_inicial, Vn) or not self.vn_pertence(novo_inicial):
			raise Exception("Erro Interno")

		self.__vn_inicial = novo_inicial

	def remove_producao(self, gerador, producao):
		if not isinstance(producao, Producao) or not self.vn_pertence(gerador):
			raise Exception("Erro Interno")

		producoes = self._conjunto_producoes[gerador]
		producoes.remove(producao)
		if not producoes:
			self._conjunto_producoes.pop(gerador, None)

	def adiciona_producao(self, gerador, producao):
		if not isinstance(producao, Producao) or not self.vn_pertence(gerador) or gerador != producao.get_gerador():
			raise Exception("Erro Interno")

		if not self.vn_pertence(gerador):
			self._conjunto_producoes[gerador] = set()
			self._nao_terminais.add(gerador)
		self._conjunto_producoes[gerador].add(producao)
		for unidade in producao.get_derivacao():
			self._terminais.add(unidade)

	# Esse método remove Vn's tanto da lista de produções quanto remove produções que contém ele.
	def remove_vn(self, vn):
		if not isinstance(vn, Vn) or not self.vn_pertence(vn):
			raise Exception("Erro Interno")

		self._conjunto_producoes.pop(vn, None)
		self._nao_terminais.remove(vn)

		for gerador in self._conjunto_producoes:
			producoes = self._conjunto_producoes[gerador]
			producoes_a_remover = []
			for producao in producoes:
				derivacao = producao.get_derivacao()
				for simbolo in derivacao:
					if simbolo == vn:
						producoes_a_remover.append(producao)
						break
			for producao_a_remover in producoes_a_remover:
				producoes.remove(producao_a_remover)

	def obter_glc_padrao(self, nome):
		return GramaticaLivreDeContexto(nome, self.to_string())
