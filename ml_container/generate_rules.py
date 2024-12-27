import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import os

# Função para carregar e processar dados
def load_and_process_data(file_path):
    try:
        df = pd.read_csv(file_path)
        playlists = df.groupby('pid')['track_name'].apply(list).tolist()
        return playlists
    except Exception as e:
        print(f"Erro ao carregar ou processar o arquivo {file_path}: {e}")
        return []

# Função para aplicar o algoritmo FP-Growth
def apply_fpgrowth(playlists, minSupRatio=0.1, minConf=0.5):
    try:
        freqItemSet, rules = fpgrowth(playlists, minSupRatio=minSupRatio, minConf=minConf)
        return rules
    except Exception as e:
        print(f"Erro ao aplicar o algoritmo FP-Growth: {e}")
        return []
    
# Definir o caminho para salvar os arquivos de regras de associação
output_dir = '../data'
os.makedirs(output_dir, exist_ok=True)


# Carregar e processar o primeiro conjunto de dados
playlists1 = load_and_process_data('/home/datasets/spotify/2023_spotify_ds1.csv')
rules1 = apply_fpgrowth(playlists1)

# Salvar as regras iniciais
with open(os.path.join(output_dir, 'association_rules_v1.pkl'), 'wb') as f:
    pickle.dump(rules1, f)

print("Modelo inicial gerado com 2023_spotify_ds1.csv!")

# Carregar e processar o segundo conjunto de dados
playlists2 = load_and_process_data('/home/datasets/spotify/2023_spotify_ds2.csv')
rules2 = apply_fpgrowth(playlists2)

# Atualizar as regras de associação com as novas regras, removendo duplicatas
updated_rules = list({frozenset(rule.items()): rule for rule in rules1 + rules2}.values())

# Salvar as regras atualizadas
with open(os.path.join(output_dir, 'association_rules.pkl'), 'wb') as f:
    pickle.dump(updated_rules, f)

print("Modelo atualizado com 2023_spotify_ds2.csv!")