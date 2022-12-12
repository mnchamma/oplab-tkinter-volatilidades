import requests
import pandas as pd
from tkinter import *
from tkinter import ttk


### FUNÇÃO PARA PEGAR TOKEN DE AUTENTICAÇÃO NA API
def get_token(email,senha):
    ## BODY PARA REQUISIÇÃO NA API
    body = {"email": email,"password": senha}
    
    ## CHAMADA NA API
    r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate',json=body).json()['access-token']
    return r

### FUNÇÃO PARA BUSCAR INFORMAÇÕES NA API
def ofertas(login,senha,symbol):
    token = get_token(login,senha)
    r = requests.get('https://api.oplab.com.br/v3/market/instruments/{}'.format(symbol), headers={"Access-Token": token}).json()
    ewma = r['ewma_current']
    stdv = round(r['stdv_1y']*(252**0.5),4)*100
    garch = r['garch11_1y']
    vi = r['iv_current']
    score = r['oplab_score']['value']
    lista = [ewma,stdv,garch,vi,score]
    # df = pd.DataFrame({1:[ewma],2:[stdv],3:[garch],4:[vi],5:[score]})
    # print(df)
    return lista

    
### DEFINIÇÃO DE CASSE DE FUNÇÕES PARA UTILIZAR O TKINTER
root = Tk()

class Funcs():
    def buscar(self):
        self.login = self.login_entry.get()
        self.senha = self.senha_entry.get()  
        self.mes = self.mes_entry.get() 
        lista = ofertas(self.login,self.senha,self.mes)
        self.lista_ofertas.delete(*self.lista_ofertas.get_children())
        self.lista_ofertas.insert('',END,values=lista)         
        

    def select_lista(self):
        self.lista_ofertas.delete(*self.lista_ofertas.get_children())
        

class Aplication(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_lista()
        root.mainloop()
    def tela(self):
        self.root.title('Stock Screener')
        self.root.configure(background='#F5F5F5')
        self.root.geometry('900x500')
        self.root.resizable(False,True)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root,bd = 4,bg='#005b8f')
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.95,relheight=0.46)

        self.frame_2 = Frame(self.root,bd = 4,bg='#005b8f')
        self.frame_2.place(relx=0.02,rely=0.5,relwidth=0.95,relheight=0.46)

    def widgets_frame1(self):
        ### BOTÃO ENVIAR
        self.botao_enviar = Button(self.frame_1,text = 'Buscar Ativo',command=self.buscar)
        self.botao_enviar.place(relx=0.45,rely=0.05,relheight=0.15)
        
        ### EMAIL
        self.lb_login = Label(self.frame_1,text='Email OpLab')
        self.lb_login.place(relx=0.05,rely=0.05)
        self.login_entry = Entry(self.frame_1)
        self.login_entry.place(relx=0.15,rely=0.05)

        ### SENHA
        self.lb_senha = Label(self.frame_1,text='Senha OpLab')
        self.lb_senha.place(relx=0.05,rely=0.20)
        self.senha_entry = Entry(self.frame_1)
        self.senha_entry.place(relx=0.15,rely=0.20)

        ### ATIVO
        self.lb_mes = Label(self.frame_1,text='Ativo')
        self.lb_mes.place(relx=0.05,rely=0.35)
        self.mes_entry = Entry(self.frame_1)
        self.mes_entry.place(relx=0.15,rely=0.35)

    def lista_frame2(self):
        self.lista_ofertas = ttk.Treeview(self.frame_2,height=3,column=('col1','col2','col3','col4','col5'))
        self.lista_ofertas.heading('#0',text='')
        self.lista_ofertas.heading('#1',text='EWMA')
        self.lista_ofertas.heading('#2',text='STDV')
        self.lista_ofertas.heading('#3',text='GARCH')
        self.lista_ofertas.heading('#4',text='VOL IMP')
        self.lista_ofertas.heading('#5',text='OPLAB SCORE')

        self.lista_ofertas.column('#0',width=1)
        self.lista_ofertas.column('#1',width=75)
        self.lista_ofertas.column('#2',width=75)
        self.lista_ofertas.column('#3',width=75)
        self.lista_ofertas.column('#4',width=75)
        self.lista_ofertas.column('#5',width=100)

        self.lista_ofertas.place(relx=0.01,rely=0.01,relwidth=0.95,relheight=0.85)
        self.scroll_lista = Scrollbar(self.frame_2,orient='vertical')
        self.lista_ofertas.configure(yscroll=self.scroll_lista.set)
        self.scroll_lista.place(relx=0.96,rely=0.01,relwidth=0.04,relheight=0.85)


Aplication()



