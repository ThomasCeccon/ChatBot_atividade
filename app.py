from flask import Flask, jsonify, render_template, request

# Instância a classe Flask
app = Flask(__name__)

# Rotas de acesso
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_response(user_input)
    return jsonify({'response': response})

# Função para gerar resposta
def generate_response(user_input):
    user_input = user_input.lower()
    
    if "1" in user_input:
        return "Para escolher uma placa, por favor, diga qual é a sua necessidade: residencial, comercial ou industrial?"
    
    elif "residencial" in user_input:
        return "Para uma necessidade residencial, recomendamos 20 placas solares."
    
    elif "comercial" in user_input:
        return "Para uma necessidade comercial, recomendamos 40 placas solares."
    
    elif "industrial" in user_input:
        return "Para uma necessidade industrial, recomendamos 70 placas solares."
    
    elif "2" in user_input:
        return "Ótimo! Para prosseguir com a compra, por favor, informe seu nome completo."
    
    elif "nome" in user_input:  # Para capturar o nome do usuário
        return "Obrigado! Agora, por favor, informe seu número de telefone para que possamos entrar em contato."
    
    elif "telefone" in user_input:  # Para capturar o número de telefone
        return "Recebemos suas informações. Entraremos em contato em breve para finalizar a compra. Muito obrigado!"
    
    else:
        return "Desculpe, não entendi. Você pode escolher uma opção: 1 para escolher uma placa ou 2 se estiver interessado em comprar."

# Executado apenas no arquivo principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
