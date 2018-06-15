# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Source.Model.Elemento import *
from Source.View.Criacao import Criacao
from Source.View.SelecaoElemento import SelecionaElemento


class View:

	__controller = None

	__root = None
	__frame_menu_principal = None

	__listbox_lista_de_linguagens = None

	__button_nova_linguagem = None
	__button_deletar_linguagem = None
	__button_clonar_linguagem = None

	__frame_manipulacao_elemento = None
	__frame_elemento_nulo = None
	__notebook_abas_de_representacao = None

	__frame_info = None
	__label_nome_display = None
	__label_tipo_display = None
	__text_visualizacao = None
	__frame_conversoes = None
	__frame_operacoes = None
	__int_operacao_selecionada = None
	__frame_operacoes_gr = None
	__int_operacao_gr_selecionada = None
	__frame_operacoes_af = None

	__button_alterar_elemento = None

	__button_converter_para_gr = None
	__button_converter_para_af = None

	__popup_novo_elemento = None
	__popup_seleciona_elemento = None

	def __init__(self, controller):
		self.__controller = controller
		self.__inicializar_root()
		self.__inicializar_variaveis()
		self.__inicializar_menubar()
		self.__inicializar_menus()
		self.centralizar(self.__root)
		self.__atualiza_operacao(None)
		self.mostrar_menu(True)

	def __inicializar_variaveis(self):
		self.__popup_novo_elemento = Criacao(self.__root, self.__controller)
		self.__popup_seleciona_elemento = SelecionaElemento(self.__root)
		self.__int_operacao_selecionada = IntVar()
		self.__int_operacao_gr_selecionada = IntVar()
		self.__string_sentenca_a_reconhecer = StringVar()
		self.__string_tamanho_enumerados = StringVar()

	def __inicializar_root(self):
		self.__root = Tk()
		self.__root.title("T2 INE5421 - Dúnia Marchiori, Vinicius Steffani Schweitzer")
		self.__root.resizable(width=True, height=True)
		self.__root.minsize(width=800, height=600)
		self.__root.grid_rowconfigure(0, weight=1)
		self.__root.grid_columnconfigure(0, weight=1)
		self.__root.protocol("WM_DELETE_WINDOW", sys.exit)

	def __inicializar_menubar(self):
		menu_main = Menu(self.__root)

		menu_abrir = Menu(menu_main, tearoff=0)
		menu_abrir.add_command(label="Expressão Regular", command=self.cb_carregar_er)
		menu_abrir.add_command(label="Gramática Regular", command=self.cb_carregar_gr)

		menu_arquivo = Menu(menu_main, tearoff=0)
		menu_arquivo.add_cascade(label="Abrir", menu=menu_abrir)
		menu_arquivo.add_command(label="Salvar", command=self.cb_salvar)

		menu_main.add_cascade(label="Arquivo", menu=menu_arquivo)
		menu_main.add_command(label="Sobre", command=lambda: self.mostrar_aviso("Trabalho 2 de INE5421\n\nPor:\nDúnia Marchiori\nVinicius Steffani Schweitzer"))

		self.__root.configure(menu=menu_main)

	def __configura_elemento(self, elemento, row=0, column=0, rowspan=1, columnspan=1, rowweight=1, columnweight=1, sticky=N+S+E+W):
		elemento.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
		elemento.master.grid_rowconfigure(row, weight=rowweight)
		elemento.master.grid_columnconfigure(column, weight=columnweight)

	def __inicializar_menus(self):
		self.__frame_menu_principal = Frame(self.__root)
		self.__configura_elemento(self.__frame_menu_principal)

		self.__inicializa_lista_de_linguagens()
		self.__inicializa_opcoes_de_manipulacao()

	def __inicializa_lista_de_linguagens(self):
		frame_lista_de_linguagens = LabelFrame(self.__frame_menu_principal, bd=2, relief=GROOVE, text="Elementos")
		self.__configura_elemento(frame_lista_de_linguagens, row=0, column=0)

		frame_listbox = Frame(frame_lista_de_linguagens)
		self.__configura_elemento(frame_listbox, row=1, column=0, rowspan=1, columnspan=3)

		self.__listbox_lista_de_linguagens = Listbox(frame_listbox, selectmode=SINGLE, bd=5, relief=SUNKEN, exportselection=False)
		self.__configura_elemento(self.__listbox_lista_de_linguagens, row=0, column=0)
		self.__listbox_lista_de_linguagens.bind('<<ListboxSelect>>', self.cb_seleciona_lista)

		scrollbar_lista = Scrollbar(frame_listbox, command=self.__listbox_lista_de_linguagens.yview)
		self.__listbox_lista_de_linguagens['yscrollcommand'] = scrollbar_lista.set
		self.__configura_elemento(scrollbar_lista, row=0, column=1, rowweight=1, columnweight=0)

		self.__button_nova_linguagem = Button(frame_lista_de_linguagens, text="Novo", command=self.abrir_janela_novo_elemento)
		self.__configura_elemento(self.__button_nova_linguagem, row=0, column=0, rowweight=0, columnweight=1)
		self.__button_deletar_linguagem = Button(frame_lista_de_linguagens, text="Remover",command=lambda: self.__controller.cb_remover_elemento(self.__get_indice_selecionado()))
		self.__configura_elemento(self.__button_deletar_linguagem, row=0, column=1, rowweight=0, columnweight=1)
		self.__button_clonar_linguagem = Button(frame_lista_de_linguagens, text="Duplicar", command=lambda:self.__controller.cb_duplica_elemento(self.__get_indice_selecionado()))
		self.__configura_elemento(self.__button_clonar_linguagem, row=0, column=2, rowweight=0, columnweight=1)

	def __inicializa_opcoes_de_manipulacao(self):
		frame_opcoes_de_manipulacao = LabelFrame(self.__frame_menu_principal, bd=2, relief=GROOVE, text="Manipulações")
		self.__configura_elemento(frame_opcoes_de_manipulacao, row=0, column=1, columnweight=5)

		# region Frame sem elemento selecionado
		self.__frame_elemento_nulo = Frame(frame_opcoes_de_manipulacao)
		self.__configura_elemento(self.__frame_elemento_nulo)
		self.__inicializa_tela_sem_selecionado()
		self.__frame_elemento_nulo.grid_remove()
		# endregion

		# region Notebook com as abas
		self.__frame_manipulacao_elemento = LabelFrame(frame_opcoes_de_manipulacao, text="ER", bd=2, relief=GROOVE,)
		self.__configura_elemento(self.__frame_manipulacao_elemento)
		self.__frame_manipulacao_elemento.grid_remove()

		self.__notebook_abas_de_representacao = ttk.Notebook(self.__frame_manipulacao_elemento)
		self.__notebook_abas_de_representacao.pack(expand=True, fill=BOTH)

		aba_info = ttk.Frame(self.__notebook_abas_de_representacao)
		self.__notebook_abas_de_representacao.add(aba_info, text='Informações')

		aba_conversoes = ttk.Frame(self.__notebook_abas_de_representacao)
		self.__notebook_abas_de_representacao.add(aba_conversoes, text='Conversões')

		aba_operacoes_linguagem = ttk.Frame(self.__notebook_abas_de_representacao)
		self.__notebook_abas_de_representacao.add(aba_operacoes_linguagem, text='Operações')

		aba_operacoes_especificas = ttk.Frame(self.__notebook_abas_de_representacao)
		self.__notebook_abas_de_representacao.add(aba_operacoes_especificas, text='Operações Específicas')
		# endregion

		# region Frames das abas
		padding = 10

		self.__frame_info = Frame(aba_info, padx=padding, pady=padding)
		self.__configura_elemento(self.__frame_info)
		self.__inicializa_frame_informacoes()

		self.__frame_conversoes = Frame(aba_conversoes, padx=padding, pady=padding)
		self.__configura_elemento(self.__frame_conversoes)
		self.__inicializa_frame_conversoes()

		self.__frame_operacoes = Frame(aba_operacoes_linguagem, padx=padding, pady=padding)
		self.__configura_elemento(self.__frame_operacoes)
		self.__inicializa_frame_operacoes()

		self.__frame_operacoes_gr = Frame(aba_operacoes_especificas, padx=padding, pady=padding)
		self.__configura_elemento(self.__frame_operacoes_gr)
		self.__inicializa_frame_operacoes_gr()
		self.__frame_operacoes_gr.grid_remove()

		self.__frame_operacoes_af = Frame(aba_operacoes_especificas, padx=padding, pady=padding)
		self.__inicializa_frame_operacoes_af()
		self.__configura_elemento(self.__frame_operacoes_af)
		# endregion

	def __inicializa_frame_informacoes(self):
		padding = 10
		frame_dados = Frame(self.__frame_info)
		self.__configura_elemento(frame_dados, row=0, column=0, rowweight=0, sticky=NW)

		label_nome = Label(frame_dados, text="Nome:")
		self.__configura_elemento(label_nome, row=0, column=0, rowweight=0, columnweight=0, sticky=W)
		self.__label_nome_display = Label(frame_dados, text="NOME", wraplength=500, justify=LEFT)
		self.__configura_elemento(self.__label_nome_display, row=0, column=1, rowweight=0, columnweight=1, sticky=W)
		label_tipo = Label(frame_dados, text="Tipo:")
		self.__configura_elemento(label_tipo, row=1, column=0, rowweight=0, columnweight=0, sticky=W)
		self.__label_tipo_display = Label(frame_dados, text="TIPO")
		self.__configura_elemento(self.__label_tipo_display, row=1, column=1, rowweight=0, columnweight=1, sticky=W)

		frame_visualizacao = Frame(self.__frame_info, pady=10)
		self.__configura_elemento(frame_visualizacao, row=1, column=0)

		label_visualizacao = Label(frame_visualizacao, text="Visualização:")
		self.__configura_elemento(label_visualizacao, row=0, column=0, columnspan=2, rowweight=0, columnweight=0, sticky=W)

		self.__text_visualizacao = Text(frame_visualizacao, wrap=NONE, width=0, height=0)
		self.__configura_elemento(self.__text_visualizacao, row=1, column=0)
		self.__text_visualizacao.config(state=DISABLED)

		scrollbar_visualizacao_y = Scrollbar(frame_visualizacao, command=self.__text_visualizacao.yview)
		self.__text_visualizacao['yscrollcommand'] = scrollbar_visualizacao_y.set
		self.__configura_elemento(scrollbar_visualizacao_y, row=1, column=1, columnweight=0)

		scrollbar_visualizacao_x = Scrollbar(frame_visualizacao, orient=HORIZONTAL, command=self.__text_visualizacao.xview)
		self.__text_visualizacao['xscrollcommand'] = scrollbar_visualizacao_x.set
		self.__configura_elemento(scrollbar_visualizacao_x, row=2, column=0, rowweight=0, columnweight=1)

		frame_alteracao = Frame(self.__frame_info)
		self.__configura_elemento(frame_alteracao, row=2, column=0, rowweight=0, columnweight=1, sticky=E+W)

		self.__button_alterar_elemento = Button(frame_alteracao, text="Alterar Elemento", command=self.alterar_elemento)
		self.__configura_elemento(self.__button_alterar_elemento, sticky="")

	def __inicializa_frame_conversoes(self):
		padding = 10
		label_gr = Label(self.__frame_conversoes, text="Converter para Gramática Regular:", pady=padding)
		self.__configura_elemento(label_gr, row=0, column=0, rowweight=0, columnweight=0, sticky=W)

		self.__button_converter_para_gr = Button(self.__frame_conversoes, text="Converter", command=lambda: self.__controller.cb_converter_para_gr(self.__get_indice_selecionado()))
		self.__configura_elemento(self.__button_converter_para_gr, row=0, column=1, rowweight=0, columnweight=0, sticky=W)

		label_af = Label(self.__frame_conversoes, text="Converter para Autômato Finito:", pady=padding)
		self.__configura_elemento(label_af, row=1, column=0, rowweight=0, columnweight=0, sticky=W)

		self.__button_converter_para_af = Button(self.__frame_conversoes, text="Converter", command=lambda: self.__controller.cb_converter_para_af(self.__get_indice_selecionado()))
		self.__configura_elemento(self.__button_converter_para_af, row=1, column=1, rowweight=0, columnweight=0, sticky=W)

	def __inicializa_frame_operacoes(self):
		padding = 10

		label__operacao = Label(self.__frame_operacoes, text="Obter autômato finito do(a):")
		self.__configura_elemento(label__operacao, row=0, column=0, rowweight=0, columnweight=0, sticky=NW)

		frame_seleciona_operacao = LabelFrame(self.__frame_operacoes, text="Operação")
		self.__configura_elemento(frame_seleciona_operacao, row=1, column=0, rowweight=0, columnweight=0, sticky=NW)

		operacoes = [
			("União deste elemento com outro", 0),
			("Intersecção deste elemento com outro", 1),
			("Diferença deste elemento com outro", 2),
			("Reverso deste elemento", 3),
			("Complemento deste elemento", 4)
		]
		self.__int_operacao_selecionada.set(0)
		for texto, valor in operacoes:
			b = Radiobutton(frame_seleciona_operacao, text=texto,
							variable=self.__int_operacao_selecionada, value=valor)
			self.__configura_elemento(b, row=valor, sticky=NW)

		f = Frame(self.__frame_operacoes, pady=padding)
		self.__configura_elemento(f, row=3, column=0, rowweight=0, columnweight=0, sticky=NW)

		button_aplicar_operacao = Button(f, text="Aplicar Operação", command=self.cb_operacao_sobre_linguagem)
		self.__configura_elemento(button_aplicar_operacao)

	def __inicializa_frame_operacoes_gr(self):
		padding = 10
		label__operacao = Label(self.__frame_operacoes_gr, text="Obter gramática resultante do(a):")
		self.__configura_elemento(label__operacao, row=0, column=0, rowweight=0, columnweight=0, sticky=NW)

		frame_seleciona_operacao = LabelFrame(self.__frame_operacoes_gr, text="Operação")
		self.__configura_elemento(frame_seleciona_operacao, row=1, column=0, rowweight=0, columnweight=0, sticky=NW)

		operacoes = [
			("União desta gramática com outra", 0),
			("Concatenação desta gramática com outra", 1),
			("Fecho desta gramática", 2)
		]
		self.__int_operacao_gr_selecionada.set(0)
		for texto, valor in operacoes:
			b = Radiobutton(frame_seleciona_operacao, text=texto,
							variable=self.__int_operacao_gr_selecionada, value=valor)
			self.__configura_elemento(b, row=valor, sticky=NW)

		f = Frame(self.__frame_operacoes_gr, pady=padding)
		self.__configura_elemento(f, row=3, column=0, rowweight=0, columnweight=0, sticky=NW)

		button_aplicar_operacao = Button(f, text="Aplicar Operação", command=self.cb_operacao_sobre_gr)
		self.__configura_elemento(button_aplicar_operacao)

	def __inicializa_frame_operacoes_af(self):
		padding = 10
		label_det = Label(self.__frame_operacoes_af, text="Obter autômato determinístico equivalente:", pady=padding)
		self.__configura_elemento(label_det, row=0, column=0, columnspan=2, rowweight=0, columnweight=0, sticky=W)

		button_determinizar = Button(self.__frame_operacoes_af, text="Determinizar", command=self.cb_determiniza_af)
		self.__configura_elemento(button_determinizar, row=0, column=2, rowweight=0, columnweight=0, sticky=W)

		label_af = Label(self.__frame_operacoes_af, text="Obter autômato mínimo equivalente:", pady=padding)
		self.__configura_elemento(label_af, row=1, column=0, columnspan=2, rowweight=0, columnweight=0, sticky=W)

		button_converter_para_af = Button(self.__frame_operacoes_af, text="Minimizar", command=self.cb_minimiza_af)
		self.__configura_elemento(button_converter_para_af, row=1, column=2, rowweight=0, columnweight=0, sticky=W+E)

		label_reconhecer = Label(self.__frame_operacoes_af, text="Reconhecer sentença:", pady=padding)
		self.__configura_elemento(label_reconhecer, row=2, column=0, rowweight=1, columnweight=0, sticky=W)

		f = Frame(self.__frame_operacoes_af, padx=padding)
		self.__configura_elemento(f, row=2, column=1, rowweight=0, columnweight=0, sticky=W+E)
		entry_sentenca = Entry(f, textvariable=self.__string_sentenca_a_reconhecer)
		self.__configura_elemento(entry_sentenca)

		button_reconhecer = Button(self.__frame_operacoes_af, text="Reconhecer", command=self.cb_reconhece_sentenca)
		self.__configura_elemento(button_reconhecer, row=2, column=2, rowweight=0, columnweight=0, sticky=W+E)

		label_gerar = Label(self.__frame_operacoes_af, text="Gerar sentenças de tamanho: ", pady=padding)
		self.__configura_elemento(label_gerar, row=3, column=0, rowweight=1, columnweight=0, sticky=W)

		f = Frame(self.__frame_operacoes_af, padx=padding)
		self.__configura_elemento(f, row=3, column=1, rowweight=0, columnweight=0, sticky=W+E)
		entry_tamanho = Entry(f, textvariable=self.__string_tamanho_enumerados)
		self.__configura_elemento(entry_tamanho)

		button_reconhecer = Button(self.__frame_operacoes_af, text="Gerar", command=self.cb_enumera_sentencas)
		self.__configura_elemento(button_reconhecer, row=3, column=2, rowweight=0, columnweight=0, sticky=W+E)

		self.__frame_operacoes_af.grid_columnconfigure(1, minsize=200)

	def __inicializa_tela_sem_selecionado(self):
		f = Frame(self.__frame_elemento_nulo)
		f.pack(expand=True)
		label = Label(f, text="Você não possui nenhum elemento selecionado\n"
							  "Crie um novo no painel à esquerda ou selecione um já criado")
		label.pack()

	def __estado_botoes_da_lista(self, estado=True):
		state = NORMAL
		if not estado:
			state = DISABLED
		self.__button_deletar_linguagem['state'] = state
		self.__button_clonar_linguagem['state'] = state

	def __altera_tela_operacao(self, num_tela):
		if num_tela == 0:
			self.__frame_manipulacao_elemento.grid_remove()
			self.__frame_elemento_nulo.grid()
		else:
			self.__frame_elemento_nulo.grid_remove()
			self.__frame_manipulacao_elemento.grid()

			if num_tela == 1:  # GR
				self.__notebook_abas_de_representacao.tab(3, state=NORMAL)
				self.__frame_operacoes_af.grid_remove()
				self.__frame_operacoes_gr.grid()
			elif num_tela == 2:  # ER
				self.__notebook_abas_de_representacao.tab(3, state=DISABLED)
				self.__frame_operacoes_gr.grid_remove()
				self.__frame_operacoes_af.grid_remove()
			elif num_tela == 3:  # AF
				self.__notebook_abas_de_representacao.tab(3, state=NORMAL)
				self.__frame_operacoes_gr.grid_remove()
				self.__frame_operacoes_af.grid()

	def __atualiza_operacao(self, elemento_selecionado):
		if elemento_selecionado is not None:
			self.__estado_botoes_da_lista(estado=True)
			nome = elemento_selecionado.get_nome()
			tipo = None
			representacao = elemento_selecionado.to_string()
			if elemento_selecionado.get_tipo() is TipoElemento.GLC:
				self.__altera_tela_operacao(1)
				tipo = "Gramática Livre de Contexto"
				self.__frame_manipulacao_elemento.configure(text=tipo)
				self.__button_converter_para_gr['state'] = DISABLED
				self.__button_converter_para_af['state'] = NORMAL
				self.__button_alterar_elemento['state'] = NORMAL
				self.__button_alterar_elemento.grid()
			self.__atualiza_visualizacao_do_elemento(nome, tipo, representacao)
		else:
			self.__altera_tela_operacao(0)
			self.__estado_botoes_da_lista(estado=False)

	def atualiza_elemento_selecionado(self, indice, elemento_selecionado):
		if indice is not None:
			self.__listbox_lista_de_linguagens.selection_set(indice)
			self.__listbox_lista_de_linguagens.see(indice)
			self.__notebook_abas_de_representacao.select(0)
		self.__atualiza_operacao(elemento_selecionado)

	def __atualiza_visualizacao_do_elemento(self, nome, tipo, representacao):
		self.__label_nome_display['text'] = nome
		self.__label_tipo_display['text'] = tipo
		self.__text_visualizacao.configure(state='normal')
		self.__text_visualizacao.delete("1.0", END)
		self.__text_visualizacao.insert(END, representacao)
		self.__text_visualizacao.configure(state='disabled')

	def adicionar_elemento_na_lista(self, nome_do_elemento, tipo_do_elemento, select=True):
		display_name = "(" + tipo_do_elemento.name + ") " + nome_do_elemento
		self.__listbox_lista_de_linguagens.insert(END, display_name)
		if select:
			self.__listbox_lista_de_linguagens.selection_clear(0, END)
			self.__listbox_lista_de_linguagens.select_set(END)
			self.cb_seleciona_lista()

	def remover_elemento_da_lista(self, indice):
		self.__listbox_lista_de_linguagens.delete(indice)
		self.cb_seleciona_lista(None)

	def abrir_janela_novo_elemento(self):
		if not self.__popup_novo_elemento.is_showing():
			self.__popup_novo_elemento.show()

	def abrir_janela_edicao_de_elemento(self, nome, sentenca, tipo):
		current_size = self.__listbox_lista_de_linguagens.size()
		if not self.__popup_novo_elemento.is_showing():
			self.__popup_novo_elemento.show(nome, sentenca, tipo, False)
		self.__root.wait_window(self.__popup_novo_elemento.get_root())
		return current_size != self.__listbox_lista_de_linguagens.size()

	def reposiciona_elemento_editado(self, indice):
		novo = self.__listbox_lista_de_linguagens.get(END)
		self.__listbox_lista_de_linguagens.delete(indice)
		self.__listbox_lista_de_linguagens.insert(indice, novo)
		self.__listbox_lista_de_linguagens.delete(END)

	def abrir_janela_seleciona_elemento(self, tipo=""):
		if not self.__popup_seleciona_elemento.is_showing():
			lista_elementos = self.__listbox_lista_de_linguagens.get(0, END)
			return self.__popup_seleciona_elemento.show(lista_elementos, tipo)

	def __get_current_top(self):
		if self.__popup_novo_elemento.is_showing():
			current_top = self.__popup_novo_elemento.get_root()
		elif self.__popup_seleciona_elemento.is_showing():
			current_top = self.__popup_seleciona_elemento.get_root()
		else:
			current_top = self.__root
		return current_top

	def __get_indice_selecionado(self):
		indice = self.__listbox_lista_de_linguagens.curselection()
		if indice:
			indice = indice[0]
		else:
			indice = None
		return indice

	def mostrar_aviso(self, aviso, titulo="Erro"):
		current_top = self.__get_current_top()
		popup = Toplevel(current_top)
		popup.transient(current_top)
		popup.title(titulo)
		popup.resizable(width=False, height=False)
		popup.minsize(width=300, height=100)
		label = Label(popup, text=aviso, wraplength=280, justify=LEFT)
		label.pack(expand=True)
		frame_btn = Frame(popup, pady=10)
		frame_btn.pack()
		btn = Button(frame_btn, text="OK", width=10, command=lambda:popup.destroy())
		btn.pack()
		btn.focus()
		self.centralizar(popup)
		popup.grab_set()
		current_top.wait_window(popup)
		if self.__popup_novo_elemento.is_showing():
			self.__popup_novo_elemento.pass_set()
		elif self.__popup_seleciona_elemento.is_showing():
			self.__popup_seleciona_elemento.pass_set()

	def mostrar_lista(self, lista_de_sentencas, tamanho):
		current_top = self.__get_current_top()
		popup = Toplevel(current_top)
		popup.transient(current_top)
		popup.title("Lista de Sentenças Geradas")
		popup.resizable(width=False, height=True)
		popup.minsize(width=400, height=231)
		label = Label(popup, text="Sentenças de tamanho: " + str(tamanho) + ":")
		label.pack()
		f = Frame(popup)
		f.pack(expand=True, fill=Y)
		listbox_de_sentencas = Listbox(f)
		for sentenca in lista_de_sentencas:
			listbox_de_sentencas.insert(END, sentenca)
		listbox_de_sentencas.pack(side=LEFT, fill=Y)

		scrollbar_lista = Scrollbar(f, command=listbox_de_sentencas.yview)
		listbox_de_sentencas['yscrollcommand'] = scrollbar_lista.set
		scrollbar_lista.pack(fill=Y, side=LEFT)

		frame_btn = Frame(popup, pady=10)
		frame_btn.pack()
		btn = Button(frame_btn, text="OK", width=10, command=lambda:popup.destroy())
		btn.pack()
		btn.focus()

		self.centralizar(popup)
		popup.grab_set()
		current_top.wait_window(popup)
		if self.__popup_novo_elemento.is_showing():
			self.__popup_novo_elemento.pass_set()
		elif self.__popup_seleciona_elemento.is_showing():
			self.__popup_seleciona_elemento.pass_set()

	def mostrar_menu(self, mostrar):
		if mostrar:
			self.__frame_menu_principal.pack(expand=True, fill=BOTH)
		else:
			self.__frame_menu_principal.pack_forget()

	def start(self):
		self.__root.mainloop()

	def alterar_elemento(self):
		indice = self.__get_indice_selecionado()
		self.__controller.cb_alterar_elemento(indice)

	def salvar_arquivo(self, nome):
		nome = nome + ".txt"
		arquivo = filedialog.asksaveasfilename(initialdir="./", title="Onde você deseja salvar?", initialfile=nome, filetypes=(("txt","*.txt"),("all files","*.*")))
		return arquivo

	def carregar_arquivo(self):
		arquivo = filedialog.askopenfilename(initialdir="./", title="Qual arquivo você quer carregar?")
		return arquivo

	def centralizar(self, janela):
		janela.update_idletasks()
		width = janela.winfo_width()
		frm_width = janela.winfo_rootx() - janela.winfo_x()
		win_width = width + 2 * frm_width
		height = janela.winfo_height()
		titlebar_height = janela.winfo_rooty() - janela.winfo_y()
		win_height = height + titlebar_height + frm_width
		x = janela.winfo_screenwidth() // 2 - win_width // 2
		y = janela.winfo_screenheight() // 2 - win_height // 2
		janela.geometry('{}x{}+{}+{}'.format(width, height, x, y))
		janela.deiconify()

	def cb_seleciona_lista(self, event=None):
		indice = self.__get_indice_selecionado()
		self.__controller.cb_alterar_elemento_selecionado(indice)

	def cb_operacao_sobre_linguagem(self):
		indice_primeiro = self.__get_indice_selecionado()
		operacao = self.__int_operacao_selecionada.get()
		if operacao < 3:
			indice_segundo = self.abrir_janela_seleciona_elemento()
		else:
			indice_segundo = None
		self.__controller.cb_aplica_operacao(indice_primeiro, indice_segundo, operacao)

	def cb_operacao_sobre_gr(self):
		indice_primeiro = self.__get_indice_selecionado()
		operacao = self.__int_operacao_gr_selecionada.get()
		if operacao != 2:
			indice_segundo = self.abrir_janela_seleciona_elemento("GR")
		else:
			indice_segundo = None
		self.__controller.cb_aplica_operacao_gr(indice_primeiro, indice_segundo, operacao)

	def cb_determiniza_af(self):
		indice_selecionado = self.__get_indice_selecionado()
		self.__controller.cb_determiniza_af(indice_selecionado)

	def cb_minimiza_af(self):
		indice_selecionado = self.__get_indice_selecionado()
		self.__controller.cb_minimiza_af(indice_selecionado)

	def cb_reconhece_sentenca(self):
		indice_selecionado = self.__get_indice_selecionado()
		sentenca = self.__string_sentenca_a_reconhecer.get()
		self.__controller.cb_reconhecimento(indice_selecionado, sentenca)

	def cb_enumera_sentencas(self):
		indice_selecionado = self.__get_indice_selecionado()
		tamanho = self.__string_tamanho_enumerados.get()
		self.__controller.cb_enumeracao(indice_selecionado, tamanho)

	def cb_salvar(self):
		if self.__get_indice_selecionado() is not None:
			self.__controller.cb_salvar_elemento(self.__get_indice_selecionado())
		else:
			self.mostrar_aviso("Você precisa selecionar um elemento para salvá-lo.")

	def cb_carregar_gr(self):
		caminho = self.carregar_arquivo()
		self.__controller.cb_carregar_gr(caminho)

	def cb_carregar_er(self):
		caminho = self.carregar_arquivo()
		self.__controller.cb_carregar_er(caminho)
