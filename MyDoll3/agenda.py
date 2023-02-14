from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button


class Agenda_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
        self.compromissos_agenda = carregar()["compromissos"]
        self.estoque = carregar()["estoque"]
        for num, compromisso in enumerate(self.compromissos_agenda):
            if num == 0:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            self.add_widget(Caixa_agenda_compromissos(compromisso, num))
        self.add_widget(Botao_adicionar_agenda())

    def editar(self, conteudo, numero):
        nome = conteudo[0]
        quantidade = conteudo[1]
        descricao = conteudo[2]
        dia = conteudo[3]
        mes = conteudo[4]
        ano = conteudo[5]
        preco = ""
        imagem = ""

        for c in self.estoque:
            if c["nome_produto"] == nome:
                preco = str(int(quantidade) * int(c["preco"]))
                imagem = c["imagem"]
        
        dic = {"nome": nome, 
            "quantidade": quantidade, 
            "data": dia + "/" + mes + "/" + ano, 
            "descricao": descricao, 
            "preco": preco, 
            "imagem": imagem}

        self.clear_widgets()
        self.compromissos_agenda[numero] = dic
        for num, compromisso in enumerate(self.compromissos_agenda):
            if num == 0:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            self.add_widget(Caixa_agenda_compromissos(compromisso, num))
        self.add_widget(Botao_adicionar_agenda())
        saving = carregar()
        saving["compromissos"] = self.compromissos_agenda
        salvar(saving)

    def atualizar(self):
        self.compromissos_agenda = carregar()["compromissos"]
        self.estoque = carregar()["estoque"]
        self.clear_widgets()
        self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
        for num, compromisso in enumerate(self.compromissos_agenda):
            if num == 0:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            self.add_widget(Caixa_agenda_compromissos(compromisso, num))
        self.add_widget(Botao_adicionar_agenda())

    def excluir(self, numero):
        del self.compromissos_agenda[numero]
        self.clear_widgets()
        for num, compromisso in enumerate(self.compromissos_agenda):
            if num == 0:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
            self.add_widget(Caixa_agenda_compromissos(compromisso, num))
        self.add_widget(Botao_adicionar_agenda())
        saving = carregar()
        saving["compromissos"] = self.compromissos_agenda
        salvar(saving)

    def adicionar(self, conteudo):
        nome = conteudo[0]
        quantidade = conteudo[1]
        descricao = conteudo[2]
        dia = conteudo[3]
        mes = conteudo[4]
        ano = conteudo[5]
        preco = ""
        imagem = ""

        if dia.isnumeric() and mes.isnumeric() and ano.isnumeric() and quantidade.isnumeric() and nome != "Escolha um produto":
            self.clear_widgets()
            for c in self.estoque:
                if c["nome_produto"] == nome:
                    preco = str(int(quantidade) * int(c["preco"]))
                    imagem = c["imagem"]

            dic = {"nome": nome, 
                "quantidade": quantidade, 
                "data": dia + "/" + mes + "/" + ano, 
                "descricao": descricao, 
                "preco": preco, 
                "imagem": imagem}
            
            concluido = False
            for c in range(0, len(self.compromissos_agenda)):
                if checar_data(dic["data"], self.compromissos_agenda[c]["data"]):
                    self.compromissos_agenda.insert(c, dic)
                    for num, compromisso in enumerate(self.compromissos_agenda):
                        if num == 0:
                            self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
                        elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                            self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
                        self.add_widget(Caixa_agenda_compromissos(compromisso, num))
                    self.add_widget(Botao_adicionar_agenda())
                    concluido = True
                    break
            if not concluido:
                self.compromissos_agenda.append(dic)
                for num, compromisso in enumerate(self.compromissos_agenda):
                    if num == 0:
                        self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
                    elif compromisso["data"] != self.compromissos_agenda[num - 1]["data"]:
                        self.add_widget(Label(height=50, size_hint_y=None, text=compromisso["data"], color=(0.2, 0.2, 0.2, 1), bold=True))
                    self.add_widget(Caixa_agenda_compromissos(compromisso, num))
                self.add_widget(Botao_adicionar_agenda())
            saving = carregar()
            saving["compromissos"] = self.compromissos_agenda
            salvar(saving)


class Caixa_agenda_compromissos(BoxLayout):
    def __init__(self, conteudo, numero, **kwargs):
        super().__init__(**kwargs)
        self.numero = numero
        self.ids.data_agenda_caixa.text = conteudo["data"]
        self.ids.nome_e_quantidade_produto_agenda_caixa.text = conteudo["nome"] + ": " + conteudo["quantidade"] + " unidade(s)"
        self.ids.preco_total_agenda_caixa.text = "R$" + "{:,.2f}".format(int(conteudo["preco"]))
        self.ids.imagem_agenda_caixa.source = conteudo["imagem"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.height += 50
            self.add_widget(Label(text=conteudo["descricao"], size_hint_y=0.4))


class Botao_adicionar_agenda(BoxLayout):
    pass


class Adicionar_agenda_tela(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()
    
    def atualizar(self):
        estoque = carregar()["estoque"]
        self.nome_todos_os_produtos = []
        for nome_produto in estoque:
            self.nome_todos_os_produtos.append(nome_produto["nome_produto"])


class Janela_informacoes_agenda(Screen):
    def definir_descricao(self, numero):
        self.descricao = carregar()["compromissos"][numero]["descricao"]


def checar_data(adicionando, data_salva):
    # Retorna True se a primeira data vir primeiro
    if int(adicionando[6:]) == int(data_salva[6:]):
        if int(adicionando[3:5]) == int(data_salva[3:5]):
            if int(adicionando[0:2]) <= int(data_salva[0:2]):
                return True
            else:
                return False
        elif int(adicionando[3:5]) < int(data_salva[3:5]):
            return True
        else:
            return False
    elif int(adicionando[6:]) < int(data_salva[6:]):
        return True
    else:
        return False