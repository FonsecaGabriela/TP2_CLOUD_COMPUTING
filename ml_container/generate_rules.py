import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

# Função para carregar e processar dados
def load_and_process_data(file_url):
    try:
        df = pd.read_csv(file_url)  
        playlists = df.groupby('pid')['track_name'].apply(list).tolist()
        return playlists
    except Exception as e:
        print(f"Erro ao carregar ou processar o arquivo {file_url}: {e}")
        return []

# Função para aplicar o algoritmo FP-Growth
def apply_fpgrowth(playlists, minSupRatio=0.1, minConf=0.5):
    try:
        freqItemSet, rules = fpgrowth(playlists, minSupRatio=minSupRatio, minConf=minConf)
        return rules
    except Exception as e:
        print(f"Erro ao aplicar o algoritmo FP-Growth: {e}")
        return []

# Obter a URL dos dados a partir da variável de ambiente
file_url = os.getenv("DATA_URL") 

if not file_url:
    print("A variável de ambiente DATA_URL não está definida.")
    exit(1)

# Definir o caminho para salvar os arquivos de regras de associação
output_dir = '../data'
os.makedirs(output_dir, exist_ok=True)

# Carregar e processar o conjunto de dados
playlists = load_and_process_data(file_url)
rules = apply_fpgrowth(playlists)

# Salvar as regras de associação
with open(os.path.join(output_dir, 'association_rules.pkl'), 'wb') as f:
    pickle.dump(rules, f)

print("Modelo gerado e salvo com sucesso!")
