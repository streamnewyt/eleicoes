import requests
import json
import os
import time

def descobrir_id_eleicao(ano="2024", uf="PE"):
    # Esta URL lista todas as eleições municipais de 2024 para o estado (PE)
    url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/listar/municipais/{ano}"
    try:
        response = requests.get(url, timeout=10)
        dados = response.json()
        # Procuramos a eleição de 2024 que seja "ORDINÁRIA"
        for eleicao in dados.get('eleicoes', []):
            if eleicao['nome'].upper().find("ORDINÁRIA") != -1:
                print(f"✅ ID da Eleição encontrado: {eleicao['codigo']} ({eleicao['nome']})")
                return eleicao['codigo']
        return "20452" # Fallback caso falhe
    except Exception as e:
        print(f"Erro ao buscar ID da eleição: {e}")
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
