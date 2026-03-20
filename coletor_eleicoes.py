import requests
import json
import os
import time

def descobrir_id_eleicao(ano="2024"):
    # ID fixo oficial do TSE para Eleições Municipais 2024 (Ordinária)
    # Tente este primeiro. Se não retornar nada, o TSE pode ter mudado para 619
    return "20452" 

def coletar_candidatos(id_eleicao, cod_municipio):
    candidatos_cidade = []
    # Cargos: 11 (Prefeito), 12 (Vice-Prefeito), 13 (Vereador)
    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_municipio}/{id_eleicao}/{cargo}/candidatos"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                dados = res.json()
                if 'candidatos' in dados and dados['candidatos']:
                    candidatos_cidade.extend(dados['candidatos'])
                    print(f"   - Encontrados {len(dados['candidatos'])} para cargo {cargo}")
            time.sleep(0.5) 
        except Exception as e:
            print(f"Erro na requisição: {e}")
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
