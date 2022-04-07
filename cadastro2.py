from email.utils import collapse_rfc2231_value
from multiprocessing.sharedctypes import Value
from optparse import Values
from tkinter import *
from tkinter import ttk
import sqlite3

from pyparsing import col

root = Tk()

class funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.continente_entry.delete(0, END)
        self.numero_entry.delete(0, END)
        self.tecnico_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("times.bd")
        self.cursor = self.conn.cursor(); print('conetando no banco de dados')
    def desconeta_bd(self):
        self.conn.close(); print('deconectado do banco de dados')
    def montaTabelas(self):
        self.conecta_bd()
     ### criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS times (
               cod INTEGER PRIMARY KEY,
               nome_time CHAR(50) NOT NULL,
               continente CHAR(50)  NOT NULL,
               numero INTEGER(50), 
               tecnico CHAR(30) NOT NULL
            ); 
        """)
        self.conn.commit(); print('O banco de dados foi criado')
        self.desconeta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.continente = self.continente_entry.get()
        self.numero = self.numero_entry.get()
        self.tecnico = self.tecnico_entry.get()
    def add_time(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO times (nome_time, continente, numero, tecnico)
        VALUES(?, ?, ?, ?)""", (self.nome, self.continente, self.numero, self.tecnico))
        self.conn.commit()
        self.desconeta_bd()
        self.select_lista()
        self.limpa_tela()   
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_time, continente, numero, tecnico FROM times
        ORDER BY nome_time ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconeta_bd()
    def duploclick(self, event):
        self.limpa_tela
        self.listaCli.selection()
        for n in self.listaCli.selection():
         col1, col2, col3, col4, col5 = self.listaCli.item(n, 'values')
        self.codigo_entry.insert(END, col1)
        self.nome_entry.insert(END, col2)
        self.continente_entry.insert(END, col3)
        self.numero_entry.insert(END, col4)
        self.tecnico_entry.insert(END, col5)
    def deleta_time(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM times WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconeta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_time(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE times SET nome_time = ?, continente = ?, numero = ?, tecnico = ? 
             WHERE cod = ? """, (self.nome, self.continente, self.numero, self.tecnico, self.codigo))
        self.conn.commit()
        self.desconeta_bd()
        self.select_lista()
        self.limpa_tela()   

        





class application(funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de times")
        self.root.configure(background='#00FF7F')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#EEDD82', highlightbackground='#000000', highlightthickness='6')
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96 , relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#00BFFF', highlightbackground='#000000', highlightthickness='6')
        self.frame_2.place(relx= 0.02, rely=0.5, relwidth= 0.96 , relheight= 0.46)
    def widgets_frame1(self):
    ### botao limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=3, bg='#778899', command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2 , rely=0.1, relwidth=0.1, relheight=0.15)
    ### botao buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=3, bg='#87CEEB')
        self.bt_buscar.place(relx=0.3 , rely=0.1, relwidth=0.1, relheight=0.15)
    ### botao alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=3, bg='#6B8E23', command=self.altera_time)
        self.bt_alterar.place(relx=0.6 , rely=0.1, relwidth=0.1, relheight=0.15)
    ### botao apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=3, bg='#FF4500', command=self.deleta_time)
        self.bt_apagar.place(relx=0.7 , rely=0.1, relwidth=0.1, relheight=0.15)
    ### botao novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=3, bg='#00CED1', command=self.add_time)
        self.bt_novo.place(relx=0.8 , rely=0.1, relwidth=0.1, relheight=0.15)
        
    ### criaçao label e codigo
        self.lb_codigo = Label(self.frame_1, text='Codigo', bg='#FFFACD')
        self.lb_codigo.place(relx=0.05, rely=0.05)
        
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.07)

    ### criaçao label e Nome
        self.lb_nome = Label(self.frame_1, text='Nome Do time', bg='#FFFACD')
        self.lb_nome.place(relx=0.05, rely=0.35)
        
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.5)
        
    ### criaçao label e Continente
        self.lb_continente = Label(self.frame_1, text='Qual o continente ?', bg='#FFFACD')
        self.lb_continente.place(relx=0.05, rely=0.55)
        
        self.continente_entry = Entry(self.frame_1)
        self.continente_entry.place(relx=0.05, rely=0.65, relwidth=0.5)

    ### criaçao label e Numero de jogadores 
        self.lb_numero = Label(self.frame_1, text='Quantos jogadores ?', bg='#FFFACD')
        self.lb_numero.place(relx=0.05, rely=0.75)
        
        self.numero_entry = Entry(self.frame_1)
        self.numero_entry.place(relx=0.05, rely=0.85, relwidth=0.5)
        
    ### criaçao label e Nome do tecnico 
        self.lb_tecnico = Label(self.frame_1, text='Nome do técnico ?', bg='#FFFACD')
        self.lb_tecnico.place(relx=0.65, rely=0.35)
        
        self.tecnico_entry = Entry(self.frame_1)
        self.tecnico_entry.place(relx=0.65, rely=0.45, relwidth=0.15)
    
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2','col3','col4','col5'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Codigo')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Continente')
        self.listaCli.heading('#4', text='Jogadores')
        self.listaCli.heading('#5', text='Técnico')

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=150)
        self.listaCli.column('#4', width=50)
        self.listaCli.column('#5', width=80)
        
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroollista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroollista.set)
        self.scroollista.place(relx=96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.duploclick)
application()