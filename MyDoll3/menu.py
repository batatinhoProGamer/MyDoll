from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.label import Label
from datetime import date
from agenda import checar_data


class Compromissos_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()
    
    def atualizar(self):
        self.clear_widgets()
        self.compromissos_menu = carregar()["compromissos"]
        for num, compromisso in enumerate(self.compromissos_menu):
            self.add_widget(Caixa_compromissos_menu(compromisso, num))


class Caixa_compromissos_menu(BoxLayout):
    def __init__(self, conteudo, num, **kwargs):
        super().__init__(**kwargs)
        self.numero = num
        self.ids.imagem_compromisso_menu.source = conteudo["imagem"]
        self.ids.nome_e_quantidade_produto_compromisso_menu.text = conteudo["nome"] + ": " + conteudo["quantidade"] + " unidades"
        self.ids.data_compromisso_menu.text = conteudo["data"]
        self.ids.preco_produto_compromisso_menu.text = "R$" + conteudo["preco"] + ",00"
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.add_widget(Label(text=conteudo["descricao"], size_hint_y=0.3))


class Menu_feiras_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()
    
    def atualizar(self):
        self.clear_widgets()
        self.feiras = carregar()["feiras"]
        for conteudo in self.feiras:
            self.add_widget(Caixa_feiras_menu(conteudo))

class Caixa_feiras_menu(BoxLayout):
    def __init__(self, conteudo, **kwargs):
        super().__init__(**kwargs)
        self.ids.data_feira_menu.text = conteudo["data"]
        self.ids.nome_feira_menu.text = conteudo["nome_feira"]
        self.ids.local_feira_menu.text = conteudo["local"]
        self.ids.horarios_feira_menu.text = conteudo["horario_inicio"] + " - " + conteudo["horario_final"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.add_widget(Label(text=conteudo["descricao"], size_hint_y=0.3))