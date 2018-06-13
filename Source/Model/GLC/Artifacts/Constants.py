import string

'''
	Arquivo com algumas constantes úteis para GLC.
'''

simb_ou = "|"
simb_derivacao = "->"
epsilon = "&"

alfabeto_nao_terminais_inicial = string.ascii_uppercase
alfabeto_nao_terminais_seguintes = string.digits
alfabeto_terminais = (string.ascii_lowercase + string.digits + string.punctuation).replace("&", "").replace("|", "")
