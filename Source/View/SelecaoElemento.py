# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from tkinter import *


class SelecionaElemento:
    __controller = None

    __root = None

    __frame_menu_principal = None

    __listbox_lista_de_elementos = None

    __parent = None

    __int_elemento_selecionado = None
    __indice_original = None

    def __init__(self, parent):
        self.__parent = parent

    def __inicializar_root(self):
        self.__root = Toplevel(self.__parent)
        self.__root.transient(self.__parent)
        self.__root.title("Seleção de Elemento")
        self.__root.resizable(width=True, height=True)

    def __inicializar_variaveis(self):
        self.__int_elemento_selecionado = None

    def __inicializar_menus(self, lista_de_opcoes, tipo_especifico):
        padding = 10
        self.__frame_menu_principal = Frame(self.__root, padx=padding, pady=padding)
        self.__frame_menu_principal.pack()

        l = Label(self.__frame_menu_principal, text="Com qual outro elemento você deseja aplicar a operação escolhida?")
        l.pack()

        f = Frame(self.__frame_menu_principal)
        f.pack(expand=True, fill=Y)

        self.__listbox_lista_de_elementos = Listbox(f, selectmode=SINGLE, exportselection=False)
        i_original = 0
        i_novo = 0
        self.__indice_original = {}
        for elemento in lista_de_opcoes:
            if tipo_especifico in elemento[1:3]:
                self.__listbox_lista_de_elementos.insert(END, elemento)
                self.__indice_original[i_novo] = i_original
                i_novo += 1
            i_original += 1
        self.__listbox_lista_de_elementos.pack(expand=True, fill=Y, side=LEFT)

        scrollbar_lista = Scrollbar(f, command=self.__listbox_lista_de_elementos.yview)
        self.__listbox_lista_de_elementos['yscrollcommand'] = scrollbar_lista.set
        scrollbar_lista.pack(fill=Y, side=LEFT)

        b = Button(self.__frame_menu_principal, text="Realizar Operação", command=self.__cb_confirma_operacao)
        b.pack()

    def __mostrar_menu(self, mostrar):
        if mostrar:
            self.__frame_menu_principal.pack(expand=True, fill=BOTH)
        else:
            self.__frame_menu_principal.pack_forget()

    def __cb_confirma_operacao(self):
        selecionado = self.__listbox_lista_de_elementos.curselection()
        if selecionado:
            self.__int_elemento_selecionado = selecionado[0]
        self.close()

    def get_selecionado_oritinal(self):
        if self.__int_elemento_selecionado is not None:
            return self.__indice_original[self.__int_elemento_selecionado]
        else:
            return None

    def get_root(self):
        return self.__root

    def is_showing(self):
        return self.__root is not None

    def show(self, lista_de_opcoes, tipo_especifico):
        self.__inicializar_root()
        self.__inicializar_variaveis()
        self.__inicializar_menus(lista_de_opcoes, tipo_especifico)
        self.__mostrar_menu(True)
        self.__root.minsize(width=400, height=300)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.centralizar(self.__root)
        self.__root.grab_set()
        self.__parent.wait_window(self.__root)
        return self.get_selecionado_oritinal()

    def pass_set(self):
        self.__root.grab_set()

    def close(self):
        self.__root.destroy()
        self.__root = None

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
