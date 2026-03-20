import requests
import json
import os
import time

# Configurações Oficiais TSE 2024
ANO = "2024"
# O ID 20452 é o código da Eleição Municipal Ordinária de 2024
ID_ELEICAO = "20452" 

def coletar_candidatos(cod_municipio):
    candidatos_cidade = []
    # Cargos: 11 (Prefeito), 13 (Vereador)
    for cargo in ["11", "13"]:
        # URL que o próprio site do TSE usa
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/{ANO}/{cod_municipio}/{ID_ELEICAO}/{cargo}/candidatos"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=15)
            
            if res.status_code == 200:
                dados = res.json()
                lista = dados.get('candidatos', [])
                if lista:
                    candidatos_cidade.extend(lista)
                    print(f"   [OK] {len(lista)} candidatos encontrados para cargo {cargo}")
            else:
                print(f"   [ERRO] Status {res.status_code} na URL: {url}")
            
            time.sleep(0.5) 
        except Exception as e:
            print(f"   [FALHA] {e}")
            
    return candidatos_cidade

# --- INÍCIO DO PROCESSO ---

# 1. Carregar Cidades
try:
    with open("municipios_pe.json", "r", encoding='utf-8') as f:
        cidades = json.load(f)
except Exception as e:
    print(f"Erro ao ler municipios_pe.json: {e}")
    exit()

# 2. Criar pasta
os.makedirs("dados", exist_ok=True)

# 3. Loop de Coleta
print(f"🚀 Iniciando coleta para {len(cidades)} cidades...")

for cidade in cidades:
    nome = cidade['nome']
    codigo = cidade['codigo']
    
    print(f"🔎 Processando: {nome} ({codigo})...")
    
    dados_finais = coletar_candidatos(codigo)
    
    # Salva o arquivo (mesmo que vazio, para sabermos que passou por ali)
    path = f"dados/{codigo}.json"
    with open(path, "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False)

print("\n✅ FIM: Todos os arquivos foram gerados na pasta 'dados'.")
