# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from tkinter import *
from tkinter import ttk


class Criacao:
	__controller = None

	__root = None

	__frame_menu_principal = None

	__entry_nome = None

	__notebook_abas_de_elementos = None

	__text_area = None

	__parent = None

	def __init__(self, parent, controller):
		self.__controller = controller
		self.__parent = parent

	def __inicializar_root(self, adicao):
		self.__root = Toplevel(self.__parent)
		self.__root.transient(self.__parent)
		if adicao:
			self.__root.title("Criação de GLC")
		else:
			self.__root.title("Edição de GLC")
		self.__root.resizable(width=True, height=True)

	def __inicializar_menus(self, nome, sentenca, adicao):
		padding = 10
		self.__frame_menu_principal = Frame(self.__root, padx=padding, pady=padding)
		self.__frame_menu_principal.pack()

		frame_nome = Frame(self.__frame_menu_principal, pady=padding)
		frame_nome.pack(fill=X)

		Label(frame_nome, text="Nome:").pack(side=LEFT)
		self.__entry_nome = Entry(frame_nome)
		self.__entry_nome.insert(0, nome)
		self.__entry_nome.pack(fill=X)
		self.__entry_nome.focus()

		f = Frame(self.__frame_menu_principal)
		f.pack(fill=X)
		Label(f, text="Entrada:").pack(side=LEFT)
		frame_elemento = Frame(self.__frame_menu_principal, padx=padding, pady=padding)
		frame_elemento.pack(expand=True, fill=BOTH)
		frame_text_area = Frame(frame_elemento, padx=padding)
		frame_text_area.pack(expand=True, fill=BOTH)

		self.__text_area = Text(frame_text_area, width=0, height=0)

		self.__text_area.insert(END, sentenca)
		self.__text_area.pack(expand=True, fill=BOTH, side=LEFT)

		scrollbar_elemento = Scrollbar(frame_text_area, command=self.__text_area.yview)
		self.__text_area['yscrollcommand'] = scrollbar_elemento.set
		scrollbar_elemento.pack(fill=Y, side=LEFT)
		if adicao:
			Button(frame_elemento, text="Adicionar Nova GLC", command=self.cria_elemento).pack()
		else:
			Button(frame_elemento, text="Confirmar Edição", command=self.cria_elemento).pack()

	def __mostrar_menu(self, mostrar):
		if mostrar:
			self.__frame_menu_principal.pack(expand=True, fill=BOTH)
		else:
			self.__frame_menu_principal.pack_forget()

	def get_root(self):
		return self.__root

	def is_showing(self):
		return self.__root is not None

	def show(self, nome="", sentenca="", adicao=True):
		self.__inicializar_root(adicao)
		self.__inicializar_menus(nome, sentenca, adicao)
		self.__mostrar_menu(True)
		self.__root.minsize(width=400, height=300)
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.centralizar(self.__root)
		self.__root.grab_set()

	def pass_set(self):
		self.__root.grab_set()

	def close(self):
		self.__root.destroy()
		self.__root = None

	def cria_elemento(self):
		nome = self.__entry_nome.get()
		text = self.__text_area.get("1.0", 'end-1c')
		success = self.__controller.cb_nova_gramatica(nome, text)
		if success:
			self.close()

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