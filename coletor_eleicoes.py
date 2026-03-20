import requests
import json
import os
import time

# Configurações Oficiais TSE 2024
ANO = "2024"
ID_ELEICAO = "20452" 

def coletar_candidatos(cod_municipio):
    candidatos_cidade = []
    # Cargos: 11 (Prefeito), 13 (Vereador)
    for cargo in ["11", "13"]:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/{ANO}/{cod_municipio}/{ID_ELEICAO}/{cargo}/candidatos"
        
        try:
            # HEADERS REAIS: Isso impede o bloqueio do TSE
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://divulgacandcontas.tse.jus.br/divulga/',
                'Origin': 'https://divulgacandcontas.tse.jus.br'
            }
            
            res = requests.get(url, headers=headers, timeout=20)
            
            if res.status_code == 200:
                dados = res.json()
                lista = dados.get('candidatos', [])
                if lista:
                    candidatos_cidade.extend(lista)
                    print(f"   ✅ [SUCESSO] {len(lista)} candidatos encontrados (Cargo {cargo})")
                else:
                    print(f"   ⚠️ [AVISO] API respondeu vazio para cargo {cargo}. ID Eleição pode ter mudado.")
            else:
                print(f"   ❌ [ERRO] Servidor TSE negou (Status {res.status_code})")
            
            time.sleep(1.5) # Pausa estratégica para não ser banido
        except Exception as e:
            print(f"   🔥 [FALHA] Conexão interrompida: {e}")
            
    return candidatos_cidade

# --- INÍCIO ---
if not os.path.exists("municipios_pe.json"):
    print("ERRO: municipios_pe.json não encontrado na raiz!")
    exit(1)

with open("municipios_pe.json", "r", encoding='utf-8') as f:
    cidades = json.load(f)

os.makedirs("dados", exist_ok=True)
print(f"🚀 Iniciando coleta para {len(cidades)} cidades...")

for cidade in cidades:
    print(f"🔎 Processando: {cidade['nome']} ({cidade['codigo']})...")
    resultado = coletar_candidatos(cidade['codigo'])
    
    with open(f"dados/{cidade['codigo']}.json", "w", encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False)

print("\n✅ FIM: Todos os arquivos foram atualizados.")
