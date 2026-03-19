import requests
import json
import os
import time

def descobrir_id_eleicao(ano="2024"):
    url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/listar/municipais/{ano}"
    try:
        response = requests.get(url)
        dados = response.json()
        for eleicao in dados['eleicoes']:
            if "ORDINÁRIA" in eleicao['nome'].upper():
                return eleicao['codigo']
    except:
        return "20452"

def coletar_candidatos(id_eleicao, cod_municipio):
    # Puxa Prefeito (11) e Vereador (13) e junta num arquivo só da cidade
    candidatos_cidade = []
    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_municipio}/{id_eleicao}/{cargo}/candidatos"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                dados = res.json()
                if 'candidatos' in dados:
                    candidatos_cidade.extend(dados['candidatos'])
            time.sleep(0.5) # Pausa leve para o TSE não bloquear por excesso de acessos
        except:
            continue
    return candidatos_cidade

# 1. Carrega sua lista de cidades que deve estar na raiz
with open("municipios_pe.json", "r", encoding='utf-8') as f:
    cidades = json.load(f)

id_atual = descobrir_id_eleicao()
os.makedirs("dados", exist_ok=True) # Cria uma pasta para não bagunçar a raiz

# 2. Loop para processar cada cidade da sua lista
for cidade in cidades:
    print(f"Coletando: {cidade['nome']}...")
    dados_finais = coletar_candidatos(id_atual, cidade['codigo'])
    
    filename = f"dados/{cidade['codigo']}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False)

print("Processo concluído com sucesso!")