from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Carregar o modelo de recomendação
def load_model():
    try:
        with open('../data/association_rules.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Modelo carregado com sucesso!")
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

# Inicializar o modelo
app.model = load_model()

# print("Modelo carregado:", app.model)

# Definir o endpoint /api/recommend
@app.route('/api/recommend', methods=['POST'])
def recommend():
    if app.model is None:
        print("Modelo não carregado!")
        return jsonify({'error': 'Modelo não carregado'}), 500
    
    try:
        # Exibir o corpo da requisição para depuração
        print("Requisição recebida:", request.get_json())
        
        # Obter a lista de músicas enviada na solicitação
        data = request.get_json(force=True)
        liked_songs = data.get('songs', [])
        
        if not liked_songs:
            print("Nenhuma música fornecida")
            return jsonify({'error': 'Nenhuma música fornecida'}), 400
        
        # Gerar recomendações com base nas músicas que o usuário gosta 
        recommended_songs = [] 
        for song in liked_songs:
            print(f"Verificando regras para a música: {song}")
            for rule in app.model:
                antecedent = rule[0]  # Acessa o antecedente da regra
                consequent = rule[1]  # Acessa o consequente da regra
                # print(f"Regra: {antecedent} -> {consequent}")
                if song in antecedent:
                    recommended_songs.extend(consequent)
        
        # Garantir que não haja duplicatas nas recomendações
        recommended_songs = list(set(recommended_songs))
        
        # Exibir as músicas recomendadas para depuração
        print("Músicas recomendadas:", recommended_songs)
        
        # Definir a resposta com a versão do código e data de atualização do modelo
        response = {
            'songs': recommended_songs,
            'version': '1.0',  
            'model_date': '2024-12-25' 
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    # Definir a porta para 52020
    app.run(debug=True, host='0.0.0.0', port=52020)