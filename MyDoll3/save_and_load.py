import json

def salvar(conteudo, arquivo="saving"):
    with open(arquivo + ".json", "w", encoding='UTF-8') as saving:
        json.dump(conteudo, saving)

def carregar(arquivo="saving"):
    with open(arquivo + ".json", encoding='UTF-8') as loading:
        data = json.load(loading)
        return data
