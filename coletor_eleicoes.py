import requests
import json
import os
import time

def descobrir_id_eleicao():
    # Para 2024, o ID 20452 é o padrão nacional das Eleições Municipais.
    # Se o retorno for 0, testaremos o ID 20455 (comum em PE) ou buscaremos na lista.
    return "20452" 

def coletar_candidatos(id_eleicao, cod_municipio):
    candidatos_cidade = []
    # 11: Prefeito, 13: Vereador
    cargos = ["11", "13"]
    
    for cargo in cargos:
        # URL OFICIAL DO TSE PARA LISTAGEM
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_municipio}/{id_eleicao}/{cargo}/candidatos"
        
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                dados = res.json()
                if 'candidatos' in dados and dados['candidatos']:
                    qtd = len(dados['candidatos'])
                    candidatos_cidade.extend(dados['candidatos'])
                    print(f"   ✅ Sucesso: {qtd} candidatos encontrados para o cargo {cargo}")
                else:
                    print(f"   ⚠️ Aviso: Nenhum candidato encontrado para o cargo {cargo} (ID: {id_eleicao})")
            else:
                print(f"   ❌ Erro API: Status {res.status_code} para o cargo {cargo}")
            
            time.sleep(0.5) 
        except Exception as e:
            print(f"   🔥 Erro na conexão: {e}")
            continue
            
    return candidatos_cidade

# --- EXECUÇÃO ---

try:
    with open("municipios_pe.json", "r", encoding='utf-8') as f:
        cidades = json.load(f)
except FileNotFoundError:
    print("ERRO CRÍTICO: municipios_pe.json não encontrado!")
    exit(1)

# Tenta o ID padrão de 2024
id_atual = descobrir_id_eleicao()
print(f"Iniciando coleta com o ID de Eleição: {id_atual}")

os.makedirs("dados", exist_ok=True) 

for cidade in cidades:
    print(f"--- Coletando: {cidade['nome']} ({cidade['codigo']}) ---")
    dados_finais = coletar_candidatos(id_atual, cidade['codigo'])
    
    filename = f"dados/{cidade['codigo']}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False)

print("\n🚀 Processo concluído!")
