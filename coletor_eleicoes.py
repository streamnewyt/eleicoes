import requests
import json
import os
import time

# Configurações Oficiais
ANO = "2024"
# Tentaremos o ID padrão, se falhar, o log nos avisará
ID_ELEICAO = "20452" 

def coletar_candidatos(cod_municipio):
    candidatos_cidade = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://divulgacandcontas.tse.jus.br/divulga/',
        'Accept': 'application/json, text/plain, */*'
    }

    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/{ANO}/{cod_municipio}/{ID_ELEICAO}/{cargo}/candidatos"
        
        try:
            res = requests.get(url, headers=headers, timeout=30)
            if res.status_code == 200:
                dados = res.json()
                lista = dados.get('candidatos', [])
                if lista:
                    candidatos_cidade.extend(lista)
                    print(f"   ✅ {len(lista)} candidatos encontrados para cargo {cargo} em {cod_municipio}")
                else:
                    print(f"   ⚠️ API retornou VAZIO para {cod_municipio} cargo {cargo}")
            else:
                print(f"   ❌ Erro HTTP {res.status_code} para {cod_municipio}")
            
            time.sleep(2) # Pausa maior para evitar bloqueio por IP
        except Exception as e:
            print(f"   🔥 Erro de rede: {e}")
            
    return candidatos_cidade

# --- EXECUÇÃO ---
with open("municipios_pe.json", "r", encoding='utf-8') as f:
    cidades = json.load(f)

os.makedirs("dados", exist_ok=True)

for cidade in cidades:
    print(f"🔎 Coletando: {cidade['nome']}...")
    resultado = coletar_candidatos(cidade['codigo'])
    
    # SÓ SALVA SE TIVER DADOS! Se resultado for vazio, não cria o JSON.
    if resultado:
        with open(f"dados/{cidade['codigo']}.json", "w", encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False)
        print(f"   💾 Arquivo {cidade['codigo']}.json SALVO com sucesso.")
    else:
        print(f"   🚫 Arquivo {cidade['codigo']}.json NÃO gerado (sem dados).")

print("\nFim do processo.")
