from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from datetime import datetime, timezone
            

class Label_minha(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.bold: True


class Historico_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtro_mes = "Mês: Todos"
        self.filtro_ano = "Ano: Todos"
        self.atualizar()

    def anos_filtro(self):
        individuais = carregar()["historico"]
        feiras = carregar()["feiras_historico"]
        anos = []
        for venda in individuais:
            if venda["data"][6:] not in anos:
                anos.append(venda["data"][6:])

        for venda in feiras:
            if venda["data"][6:] not in anos:
                for num, ano in enumerate(anos):
                    if int(venda["data"][6:]) < int(ano):
                        anos.insert(num, venda["data"][6:])
                        break

                    if num == len(anos) - 1:
                        anos.append(venda["data"][3:5])

                if len(anos) == 0:
                    anos.append(venda["data"][6:])

        anos.sort()

        for num, ano in enumerate(anos):
            anos[num] = "Ano: " + ano
        
        anos.insert(0, "Ano: Todos")
        return anos

    def meses_filtro(self):
        individuais = carregar()["historico"]
        feiras = carregar()["feiras_historico"]
        meses = []
        for venda in individuais:
            if venda["data"][3:5] not in meses:
                meses.append(venda["data"][3:5])

        for venda in feiras:
            if venda["data"][3:5] not in meses:
                for num, mes in enumerate(meses):
                    if int(venda["data"][3:5]) < int(mes):
                        meses.insert(num, venda["data"][3:5])
                        break

                    if num == len(meses) - 1:
                        meses.append(venda["data"][3:5])
                
                if len(meses) == 0:
                    meses.append(venda["data"][3:5])

        meses.sort()

        for num, mes in enumerate(meses):
            meses[num] = "Mês: " + mes
        
        meses.insert(0, "Mês: Todos")
        return meses

    def adicionar(self, imagem, data, nome_e_quantidade, preco, metodo, descricao):
        conteudo = {
            "imagem": imagem,
            "data": data,
            "nome_e_quantidade": nome_e_quantidade,
            "preco": preco,
            "metodo": metodo,
            "descricao": descricao
        }
        
        if len(self.historico) == 0:
            self.historico.append(conteudo)
        else:
            for num, vendas in enumerate(self.historico):
                if checar_data(vendas["data"], conteudo["data"]):
                    self.historico.insert(num, conteudo)
                    break

                if num == len(self.historico) - 1:
                    self.historico.append(conteudo)
        saving = carregar()
        saving["historico"] = self.historico
        salvar(saving)
    
    def atualizar(self):
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        conteudo = carregar()
        self.historico = conteudo["historico"]
        for produto in self.historico:
            self.add_widget(Caixa_historico(produto))

    def filtro_mes_atualizar(self, mes, ano):
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        conteudo = carregar()
        self.feiras_historico = conteudo["historico"]
        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for produto in self.historico:
                    if produto["data"][6:] == ano:
                        self.add_widget(Caixa_historico(produto))
        else:
            if ano == "Todos":
                for produto in self.historico:
                    if produto["data"][3:5] == mes:
                        self.add_widget(Caixa_historico(produto))
            else:
                for produto in self.historico:
                    if produto["data"][3:5] == mes and produto["data"][6:] == ano:
                        self.add_widget(Caixa_historico(produto))
    
    def filtro_ano_atualizar(self, mes, ano):
        self.filtro_mes_atualizar(mes, ano)


class Historico_scroll_feiras(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtro_mes = "Mês: Todos"
        self.filtro_ano = "Ano: Todos"
        self.atualizar()
    
    def atualizar(self):
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        conteudo = carregar()
        self.feiras_historico = conteudo["feiras_historico"]
        for caixa in self.feiras_historico:
            self.add_widget(Caixa_historico_feira(caixa))
            for produto in caixa["vendas"]:
                self.add_widget(Produto_feiras_historico(produto))
            self.add_widget(BoxLayout(size_hint_y=None, height=30))

    def filtro_mes_atualizar(self, mes, ano):
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        conteudo = carregar()
        self.feiras_historico = conteudo["feiras_historico"]
        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for caixa in self.feiras_historico:
                    if ano == caixa["data"][6:]:
                        self.add_widget(Caixa_historico_feira(caixa))
                        for produto in caixa["vendas"]:
                            self.add_widget(Produto_feiras_historico(produto))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
        else:
            if ano == "Todos":
                for caixa in self.feiras_historico:
                    if caixa["data"][3:5] == mes:
                        self.add_widget(Caixa_historico_feira(caixa))
                        for produto in caixa["vendas"]:
                            self.add_widget(Produto_feiras_historico(produto))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
            else:
                for caixa in self.feiras_historico:
                    if caixa["data"][3:5] == mes and caixa["data"][6:] == ano:
                        self.add_widget(Caixa_historico_feira(caixa))
                        for produto in caixa["vendas"]:
                            self.add_widget(Produto_feiras_historico(produto))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
    
    def filtro_ano_atualizar(self, mes, ano):
        self.filtro_mes_atualizar(mes, ano)


class Caixa_historico(BoxLayout):
    def __init__(self, conteudo, **kwargs):
        super().__init__(**kwargs)
        self.ids.data_historico_caixa.text = conteudo["data"]
        self.ids.nome_e_quantidade_produto_historico_caixa.text = conteudo["nome_e_quantidade"]
        self.ids.preco_total_historico_caixa.text = "R$" + "{:,.2f}".format(int(conteudo["preco"]))
        self.ids.imagem_historico_caixa.source = conteudo["imagem"]
        self.ids.metodo_de_pagamento.text = conteudo["metodo"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.height += 50
            self.add_widget(Label_minha(text=conteudo["descricao"]))


class Caixa_historico_feira(BoxLayout):
    def __init__(self, conteudo, **kwargs):
        super().__init__(**kwargs)
        preco = 0
        for produto in conteudo["vendas"]:
            preco += int(produto["preco"])
        self.ids.preco_feiras_total_historico.text = str(preco)
        self.ids.nome_feira_historico.text = conteudo["nome_feira"]
        self.ids.local_feira_historico.text = conteudo["local"]
        self.ids.data_feira_historico.text = conteudo["data"]
        self.ids.horarios_feira_historico.text = conteudo["horario_inicial"] + " - " + conteudo["horario_final"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.height += 50
            self.add_widget(Label_minha(text=conteudo["descricao"]))


class Produto_feiras_historico(BoxLayout):
    def __init__(self, conteudo, **kwargs):
        super().__init__(**kwargs)
        self.ids.imagem_feiras_produto_historico.source = conteudo["imagem"]
        self.ids.feiras_nome_produto_historico.text = conteudo["nome"]
        self.ids.feiras_quantidade_produto_historico.text = conteudo["quantidade"] + " unidades"
        self.ids.preco_total_feira_historico.text = "R$" + conteudo["preco"]
        self.ids.metodo_de_pagamento_historico_feira_produto.text = conteudo["pagamento"]
        if conteudo["descricao"] != "" and conteudo["descricao"] != "Descrição":
            self.ids.caixinha_descricao.add_widget(Label_minha(text=conteudo["descricao"]))


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