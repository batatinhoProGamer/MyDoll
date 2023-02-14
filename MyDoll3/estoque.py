from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.button import Button


class Tela_estoque(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
        self.estoque = carregar()["estoque"]
        for num, item in enumerate(self.estoque):
            self.add_widget(Caixa_item_estoque(item, num, width = self.width))
        self.add_widget(Botao_adicionar_estoque())

    def tela_atualizar(self):
        self.clear_widgets()
        self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
        for num, item in enumerate(self.estoque):
            self.add_widget(Caixa_item_estoque(item, num, width = self.width))
        self.add_widget(Botao_adicionar_estoque())

    def atualizar_estoque_com_agenda(self, nome_quantidade):
        nome = ""
        quantidade = ""
        for c in range(0, len(nome_quantidade)):
            if nome_quantidade[c] == ":":
                quantidade = nome_quantidade[c+2:-11]
                nome = nome_quantidade[:c]
                break
            
        for num, estoque in enumerate(self.estoque):
            if estoque["nome_produto"] == nome:
                self.estoque[num]["quantidade"] = str(int(self.estoque[num]["quantidade"]) - int(quantidade))
                break
        conteudo = carregar()
        conteudo["estoque"] = self.estoque
        salvar(conteudo)
        self.tela_atualizar()

    def atualizar(self, item, numero):
        if item["quantidade"].isnumeric() and item["preco"].isnumeric():
            self.estoque[numero] = item
            conteudo = carregar()
            conteudo["estoque"] = self.estoque
            salvar(conteudo)
            self.clear_widgets()
            self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
            for num, item in enumerate(self.estoque):
                self.add_widget(Caixa_item_estoque(item, num, width = self.width))
            self.add_widget(Botao_adicionar_estoque())

    def adicionar(self, item):
        if item["quantidade"].isnumeric() and item["preco"].isnumeric():
            self.estoque.append(item)
            conteudo = carregar()
            conteudo["estoque"] = self.estoque
            salvar(conteudo)

    def excluir(self, numero):
        del self.estoque[numero]
        conteudo = carregar()
        conteudo["estoque"] = self.estoque
        salvar(conteudo)


class Caixa_item_estoque(BoxLayout):
    def __init__(self, conteudo, num, **kwargs):
        super().__init__(**kwargs)
        self.numero = num
        self.ids.imagem.source = conteudo["imagem"]
        self.ids.nome_produto.text = conteudo["nome_produto"]
        self.ids.quantidade_produto.text = conteudo["quantidade"] + " unidades"
        self.ids.preco_produto.text = "R$" + "{:,.2f}".format(int(conteudo["preco"]))


class Botao_adicionar_estoque(BoxLayout):
    pass