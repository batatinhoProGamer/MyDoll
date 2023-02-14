from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from save_and_load import *
from menu import *
from agenda import *
from estoque import *
from historico import *
from feiras import *
from financas import *
from kivy.uix.label import Label
from datetime import datetime, timezone
from kivy.lang import Builder

Builder.load_file("MyApp.kv")


class Label_minha(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.bold: True

              
class Geral(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atual_editando_financas = 0
    
    def editando_financas(self, numero):
        self.atual_editando_financas = numero


class Gerenciador_principal(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atual_editando_estoque = 0
        self.atual_editando_agenda = 0
        self.mais_informacoes_agenda = 0
        self.carregado = carregar()
        self.valor_total = self.carregado["valor_total"]
        self.adicionando_produto_feira = 0
        self.feira_editando = 0

    def data_atual(self, data):
        dic = {
            "dia": '%02d' % datetime.now(timezone.utc).day,
            "mes": '%02d' % datetime.now(timezone.utc).month,
            "ano": str(datetime.now(timezone.utc).year)
            }
        return dic[data]

    def ano_atual_e_proximos(self):
        anos = ["Ano: Todos"]
        for c in range(0, 3):
            anos.append("Ano: " + str(datetime.now(timezone.utc).year + c))
        return anos

    def ano_atual_e_anteriores(self):
        anos = ["Ano: Todos"]
        for c in range(0, 3):
            anos.append("Ano: " + str(datetime.now(timezone.utc).year - c))
        return anos

    def pegar_financias(self):
        self.financas =  carregar()["financas"]

    def procurar_imagem(self, nome):
        conteudo = carregar()
        for produto in conteudo["estoque"]:
            if produto["nome_produto"] == nome:
                return produto["imagem"]

    def imagem_adicionar(self, lista, imagem_atual):
        if len(lista) > 0:
            return lista[0]
        else:
            return imagem_atual
    
    def total_contabilizar(self):
        conteudo = carregar()
        estoque = conteudo["estoque"]
        self.valor_total = 0
        for preco in estoque:
            self.valor_total += int(preco["preco"]) * int(preco["quantidade"])
        conteudo["valor_total"] = self.valor_total
        salvar(conteudo)
        return self.valor_total

    def editando_estoque(self, numero):
        self.atual_editando_estoque = numero

    def editando_agenda(self, numero):
        self.atual_editando_agenda = numero
    
    def mais_informacoes_agenda_atualizar(self, numero):
        self.mais_informacoes_agenda = numero
    
    def pegar_algo(self, algo):
        conteudo = carregar()["compromissos"]
        return conteudo[self.mais_informacoes_agenda][algo]
    
    def produto_feira_adiconar(self, numero):
        self.adicionando_produto_feira = numero
    
    def feira_editar(self, numero):
        self.feira_editando = numero
        

class MyDoll(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def build(self):
        return Geral()


MyDoll().run()