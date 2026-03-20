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
    candidatos_cidade = []
    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_municipio}/{id_eleicao}/{cargo}/candidatos"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                dados = res.json()
                if 'candidatos' in dados:
                    candidatos_cidade.extend(dados['candidatos'])
            time.sleep(0.5) 
        except:
            continue
    return candidatos_cidade

# Carrega a lista de cidades (deve estar na raiz do GitHub)
try:
    with open("municipios_pe.json", "r", encoding='utf-8') as f:
        cidades = json.load(f)
except FileNotFoundError:
    print("Erro: O arquivo municipios_pe.json não foi encontrado na raiz!")
    exit(1)

id_atual = descobrir_id_eleicao()

# Cria a pasta 'dados' na raiz do repositório
os.makedirs("dados", exist_ok=True) 

for cidade in cidades:
    print(f"Coletando: {cidade['nome']}...")
    dados_finais = coletar_candidatos(id_atual, cidade['codigo'])
    
    filename = f"dados/{cidade['codigo']}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False)

print("Processo concluído com sucesso!")
