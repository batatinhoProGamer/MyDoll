from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.label import Label
from kivy.uix.button import Button


class Feiras_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()

    def excluir(self, numero):
        del self.feiras[numero]
        saving = carregar()
        saving["feiras"] = self.feiras
        salvar(saving)
        self.atualizar()

    def editar(self, dia, mes, ano, local, horario_inicio, horario_final, descricao, nome_feira, numero):
        self.feiras[numero]["data"] = dia + "/" + mes + "/" + ano
        self.feiras[numero]["local"] = local
        self.feiras[numero]["horario_inicio"] = horario_inicio
        self.feiras[numero]["horario_final"] = horario_final
        self.feiras[numero]["descricao"] = descricao
        self.feiras[numero]["nome_feira"] = nome_feira
        conteudo = self.feiras[numero]
        del self.feiras[numero]
        if len(self.feiras) == 0:
            self.feiras.append(conteudo)
        else:
            pronto = False
            for num, feira in enumerate(self.feiras):
                if checar_data(conteudo["data"], feira["data"]):
                    self.feiras.insert(num, conteudo)
                    pronto = True
                    break
            if pronto == False:
                self.feiras.append(conteudo)
        saving = carregar()
        saving["feiras"] = self.feiras
        salvar(saving)
        self.atualizar()

    def excluir_produto(self, numero, numero_feira):
        del self.feiras[numero_feira]["produtos"][numero]
        saving = carregar()
        saving["feiras"][numero_feira]["produtos"] = self.feiras[numero_feira]["produtos"]
        salvar(saving)
        self.atualizar()

    def adicionar(self, dia, mes, ano, local, horario_inicio, horario_final, descricao, nome_feira):
        data = dia + "/" + mes + "/" + ano
        conteudo = {
            "imagem": "imagens/feiras.png",
            "nome_feira": nome_feira,
            "data": data,
            "horario_inicio": horario_inicio,
            "horario_final": horario_final,
            "local": local,
            "descricao": descricao,
            "produtos": []
        }
        
        if len(self.feiras) == 0:
            self.feiras.append(conteudo)
        else:
            pronto = False
            for num, feira in enumerate(self.feiras):
                if checar_data(conteudo["data"], feira["data"]):
                    self.feiras.insert(num, conteudo)
                    pronto = True
                    break
            if pronto == False:
                self.feiras.append(conteudo)

        saving = carregar()
        saving["feiras"] = self.feiras
        salvar(saving)
        self.atualizar()
    
    def atualizar(self):
        self.clear_widgets()
        self.add_widget(Button(background_color=(0, 0, 0, 0), height=5))
        self.feiras = carregar()["feiras"]
        for numerofeira, caixa in enumerate(self.feiras):
            self.add_widget(Caixa_feiras(caixa, numerofeira))
            for num, produto in enumerate(caixa["produtos"]):
                self.add_widget(Produto_feiras(produto, num, numerofeira))
            self.add_widget(Botao_adicionar_produto_feira(numerofeira))
            self.add_widget(BoxLayout(size_hint_y=None, height=30))
        self.add_widget(Botao_adicionar_feira())
    
    def adicionar_produto(self, produto, numero_feira):
        loading = carregar()
        dic = {
            "nome": produto[0],
            "quantidade": produto[1],
            "descricao": produto[2],
            "preco": "",
            "imagem": ""
        }
        for estoque in loading["estoque"]:
            if estoque["nome_produto"] == dic["nome"]:
                dic["preco"] = estoque["preco"]
                dic["imagem"] = estoque["imagem"]

        self.feiras[numero_feira]["produtos"].append(dic)
        loading["feiras"] = self.feiras
        salvar(loading)
        self.atualizar()
    

class Produto_feiras(BoxLayout):
    def __init__(self, conteudo, numero_proprio, numero_feira, **kwargs):
        super().__init__(**kwargs)
        self.numero = numero_proprio
        self.numero_feira = numero_feira
        self.ids.imagem_feiras_produto.source = conteudo["imagem"]
        self.ids.feiras_nome_produto.text = conteudo["nome"]
        self.ids.feiras_quantidade_produto.text = conteudo["quantidade"]
        self.ids.preco_total_agenda_caixa.text = str(int(conteudo["preco"]) * int(conteudo["quantidade"]))
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.ids.caixinha_descricao.add_widget(Label(text=conteudo["descricao"]))


class Botao_adicionar_produto_feira(BoxLayout):
    def __init__(self, numero, **kwargs):
        super().__init__(**kwargs)
        self.numero = numero


class Botao_adicionar_feira(BoxLayout):
    pass


class Concluir_feira_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def concluir_feira(self):
        dic = {
            "nome_feira": self.feira["nome_feira"],
            "data": self.feira["data"],
            "imagem": self.feira["imagem"],
            "horario_inicial": self.feira["horario_inicio"],
            "horario_final": self.feira["horario_final"],
            "vendas": self.vendas,
            "local": self.feira["local"],
            "descricao": self.feira["descricao"]
        }
        conteudo = carregar()
        del conteudo["feiras"][self.numero_da_feira]

        for produto in dic["vendas"]:
            for estoque in conteudo["estoque"]:
                if estoque["nome_produto"] == produto["nome"]:
                    estoque["quantidade"] = str(int(estoque["quantidade"]) - int(produto["quantidade"]))
                    break

        if len(conteudo["feiras_historico"]) == 0:
            conteudo["feiras_historico"].append(dic)
        else:
            for num, feira in enumerate(conteudo["feiras_historico"]):
                if checar_data(feira["data"], dic["data"]):
                    conteudo["feiras_historico"].insert(num, dic)
                    break

                if num == len(conteudo["feiras_historico"]) - 1:
                    conteudo["feiras_historico"].append(dic)
        salvar(conteudo)

    def iniciar(self, numero):
        self.numero_da_feira = numero
        self.feira =carregar()["feiras"][numero]
        self.vendas = []
        self.atualizar()
    
    def adicionar(self, conteudo):
        nome = conteudo[0]
        quantidade = conteudo[1]
        descricao = conteudo[2]
        preco = conteudo[3]
        pagamento = conteudo[4]
        imagem = ""
        estoque = carregar()["estoque"]
        for nome_produto in estoque:
            if nome_produto["nome_produto"] == nome:
                imagem = nome_produto["imagem"]
                break
        dic = {
            "nome": nome,
            "quantidade": quantidade,
            "descricao": descricao,
            "preco": preco,
            "imagem": imagem,
            "pagamento": pagamento
        }
        self.vendas.append(dic)
        self.atualizar()
    
    def atualizar(self):
        self.clear_widgets()
        for num, venda in enumerate(self.vendas):
            self.add_widget(Caixa_concluir_feira(venda, num))
        self.add_widget(Botao_adicionar_produto_concluir_feira())
    
    def excluir_produto(self, numero):
        del self.vendas[numero]
        self.atualizar()


class Caixa_concluir_feira(BoxLayout):
    def __init__(self, conteudo, num, **kwargs):
        super().__init__(**kwargs)
        self.numero = num
        self.ids.imagem_feiras_produto_concluir.source = conteudo["imagem"]
        self.ids.feiras_nome_produto_concluir.text = conteudo["nome"]
        self.ids.feiras_quantidade_produto_concluir.text = conteudo["quantidade"]
        self.ids.preco_total_agenda_caixa_concluir.text = conteudo["preco"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.height += 50
            self.ids.caixinha_descricao_concluir.add_widget(Label(text=conteudo["descricao"]))


class Botao_adicionar_produto_concluir_feira(BoxLayout):
    pass


class Caixa_feiras(BoxLayout):
    def __init__(self, conteudo, numero, **kwargs):
        super().__init__(**kwargs)
        self.numero = numero
        preco = 0
        for produto in conteudo["produtos"]:
            preco += int(produto["preco"]) * int(produto["quantidade"])
        self.ids.preco_feiras_total.text = str(preco)
        self.ids.nome_feira.text = conteudo["nome_feira"]
        self.ids.local_feira.text = conteudo["local"]
        self.ids.data_feira.text = conteudo["data"]
        self.ids.horarios_feira.text = conteudo["horario_inicio"] + " - " + conteudo["horario_final"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.height += 50
            self.add_widget(Label(text=conteudo["descricao"]))
        
        
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