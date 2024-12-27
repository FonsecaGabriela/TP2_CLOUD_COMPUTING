import requests
import json

# Função para enviar a solicitação de recomendação de músicas
def get_recommendations(songs):
    url = 'http://localhost:52020/api/recommend'  
    headers = {'Content-Type': 'application/json'}
    
    # Dados da solicitação
    data = {'songs': songs}
    
    try:
        # Enviar a solicitação POST para o servidor Flask
        response = requests.post(url, headers=headers, json=data)
        
        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Processar a resposta JSON
            response_data = response.json()
            print("Recomendações recebidas:")
            print(f"Versão do código: {response_data['version']}")
            print(f"Data de atualização do modelo: {response_data['model_date']}")
            print(f"Músicas recomendadas: {response_data['songs']}")
        else:
            print(f"Erro na solicitação: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao servidor: {e}")

if __name__ == '__main__':
    # Permitir que o usuário insira as músicas
    songs = input("Digite as músicas separadas por vírgula: ").split(", ")
    
    # Obter recomendações de músicas
    get_recommendations(songs)