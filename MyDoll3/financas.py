from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import datetime, timezone

class Label_minha(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.bold: True

class Botao_adicionar_financas(BoxLayout):
    pass

class Scroll_financas_atual(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()

    def atualizar(self):
        self.clear_widgets()
        self.conteudo = carregar("financas")
        for numero, compras in enumerate(self.conteudo["atual"]):
            self.add_widget(Caixa_financas_atual(numero, compras))
        self.add_widget(Botao_adicionar_financas())
        self.add_widget(Botao_concluir_mes_financas())

    def adicionar(self, produto, local, preco, forma_pagamento, dia, mes, ano, descricao):
        dic = {
            "nome produto": produto,
            "local": local,
            "preco": preco,
            "forma pagamento": forma_pagamento,
            "data": {
                "dia": dia,
                "mes": mes,
                "ano": ano
            },
            "descricao": descricao
        }
        if len(self.conteudo["atual"]) == 0:
            self.conteudo["atual"].append(dic)
        
        else:
            feito = False
            for num, produto in enumerate(self.conteudo["atual"]):
                if produto["data"]["dia"] <= dia:
                    feito = True
                    self.conteudo["atual"].insert(num, dic)
                    break
            if not feito:
                self.conteudo["atual"].append(dic)

        salvar(self.conteudo, "financas")
        self.atualizar()

    def editar(self, numero, produto, local, preco, forma_pagamento, dia, mes, ano, descricao):
        dic = {
            "nome produto": produto,
            "local": local,
            "preco": preco,
            "forma pagamento": forma_pagamento,
            "data": {
                "dia": dia,
                "mes": mes,
                "ano": ano
            },
            "descricao": descricao
        }
        self.conteudo["atual"][numero] = dic
        salvar(self.conteudo, "financas")
        self.atualizar()

    def excluir(self, numero):
        del self.conteudo["atual"][numero]
        salvar(self.conteudo, "financas")
        self.atualizar()

    def concluir_mes(self):
        mes = self.conteudo["atual"][0]["data"]["mes"]
        ano = self.conteudo["atual"][0]["data"]["ano"]
        self.conteudo["historico"][mes + "/" + ano] = self.conteudo["atual"].copy()
        self.conteudo["atual"] = []
        salvar(self.conteudo, "financas")
        self.conteudo = carregar("financas")
        self.atualizar()


class Caixa_financas_atual(BoxLayout):
    def __init__(self, numero, conteudo, **kwargs):
        super().__init__(**kwargs)
        self.numero = numero
        self.conteudo = conteudo
        self.ids.nome_produto.text = str(conteudo["nome produto"])
        self.ids.local.text = str(conteudo["local"])
        self.ids.preco.text = str(conteudo["preco"]) + " pago em " + str(conteudo["forma pagamento"])
        self.ids.data.text = str(conteudo["data"]["dia"]) + "/" + str(conteudo["data"]["mes"]) + "/" + str(conteudo["data"]["ano"])
        if str(conteudo["descricao"]) != "" and str(conteudo["descricao"]) != "Descrição":
            self.height += 50
            self.add_widget(Label_minha(text=str(conteudo["descricao"])))




class Scroll_financas_historico(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()

    def atualizar(self):
        self.clear_widgets()
        self.conteudo = carregar("financas")
        for data, lista in self.conteudo["historico"].items():
            self.add_widget(Label_minha(text=data, color=(0, 0, 0, 1)))
            for numero, compras in enumerate(lista):
                self.add_widget(Caixa_financas_historico(compras))

    def filtro_mes_atualizar(self, mes, ano):
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for data, produtos in self.conteudo["historico"].items():
                    if data[3:] == ano:
                        self.add_widget(Label_minha(text=data, color=(0, 0, 0, 1)))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(produto))
        else:
            if ano == "Todos":
                for data, produtos in self.conteudo["historico"].items():
                    if data[0:2] == mes:
                        self.add_widget(Label_minha(text=data, color=(0, 0, 0, 1)))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(produto))
            else:
                for data, produtos in self.conteudo["historico"].items():
                    if data[0:2] == mes and data[3:] == ano:
                        self.add_widget(Label_minha(text=data, color=(0, 0, 0, 1)))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(produto))
    
    def filtro_ano_atualizar(self, mes, ano):
        self.filtro_mes_atualizar(mes, ano)

    def anos_filtro(self):
        individuais = carregar("financas")["historico"]
        anos = []
        for ano, venda in individuais.items():
            if ano[3:] not in anos:
                anos.append(ano[3:])

        anos.sort()

        for num, ano in enumerate(anos):
            anos[num] = "Ano: " + ano
        
        anos.insert(0, "Ano: Todos")
        return anos

    def meses_filtro(self):
        individuais = carregar("financas")["historico"]
        meses = []
        for mes, venda in individuais.items():
            if mes[0:2] not in meses:
                meses.append(mes[0:2])

        meses.sort()

        for num, mes in enumerate(meses):
            meses[num] = "Mês: " + mes
        
        meses.insert(0, "Mês: Todos")
        return meses


class Caixa_financas_historico(BoxLayout):
    def __init__(self, conteudo, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = conteudo
        self.ids.nome_produto.text = str(conteudo["nome produto"])
        self.ids.local.text = str(conteudo["local"])
        self.ids.preco.text = str(conteudo["preco"]) + " pago em " + str(conteudo["forma pagamento"])
        self.ids.data.text = str(conteudo["data"]["dia"]) + "/" + str(conteudo["data"]["mes"]) + "/" + str(conteudo["data"]["ano"])
        if str(conteudo["descricao"]) != "" and str(conteudo["descricao"]) != "Descrição":
            self.height += 50
            self.add_widget(Label_minha(text=str(conteudo["descricao"])))


class Botao_concluir_mes_financas(Button):
    pass