import requests
import json
import os
import time

# Configurações Oficiais TSE 2024
ANO = "2024"
ID_ELEICAO = "20452" 

def coletar_candidatos(cod_municipio):
    candidatos_cidade = []
    # 11: Prefeito, 13: Vereador
    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/{ANO}/{cod_municipio}/{ID_ELEICAO}/{cargo}/candidatos"
        
        try:
            # HEADERS FORTES: Faz o GitHub parecer um navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://divulgacandcontas.tse.jus.br/divulga/',
                'Accept': 'application/json, text/plain, */*'
            }
            
            res = requests.get(url, headers=headers, timeout=20)
            
            if res.status_code == 200:
                dados = res.json()
                lista = dados.get('candidatos', [])
                if lista:
                    candidatos_cidade.extend(lista)
                    print(f"   ✅ [OK] {len(lista)} candidatos encontrados para o cargo {cargo}")
                else:
                    print(f"   ⚠️ [VAZIO] API retornou sucesso, mas sem dados para cargo {cargo}")
            else:
                print(f"   ❌ [ERRO] Código {res.status_code} na API")
            
            time.sleep(1) # Espera um pouco mais para não ser bloqueado
        except Exception as e:
            print(f"   🔥 [FALHA] Erro de conexão: {e}")
            
    return candidatos_cidade

# --- PROCESSO PRINCIPAL ---

if not os.path.exists("municipios_pe.json"):
    print("ERRO: Arquivo municipios_pe.json não encontrado!")
    exit(1)

with open("municipios_pe.json", "r", encoding='utf-8') as f:
    cidades = json.load(f)

os.makedirs("dados", exist_ok=True)
print(f"🚀 Iniciando coleta para {len(cidades)} cidades...")

for cidade in cidades:
    print(f"🔎 Processando: {cidade['nome']} ({cidade['codigo']})...")
    dados_finais = coletar_candidatos(cidade['codigo'])
    
    with open(f"dados/{cidade['codigo']}.json", "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False)

print("\n✅ FIM: Processo concluído.")
