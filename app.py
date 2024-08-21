from flask import Flask, jsonify, render_template, request

# Instância a classe Flask
app = Flask(__name__)  

 # Dicionário que armazena o estado atual da conversa de cada usuário
conversation_state = {} 

# Rotas de acesso
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')# Define a rota para a página inicial.

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Obtem a mensagem enviada pelo usuario
    user_id = request.json.get('user_id')  # Obtem o identificador unico do usuario

    # Atualiza o estado da conversa do usuário
    if user_id not in conversation_state:
        # Se o user_id não está no dicionário de estados, significa que este é um novo usuário, então inicializamos o estado dele como 'start'.
        conversation_state[user_id] = 'start'
    
    response = generate_response(user_input, user_id)  # Gera uma resposta com base na entrada do usuário e no estado atual da conversa.

    return jsonify({'response': response})  # Retorna a resposta como um JSON para o frontend.

# Função para gerar resposta
def generate_response(user_input, user_id):
    # Função principal que gera a resposta do chatbot com base no estado da conversa e na entrada do usuário.
    state = conversation_state[user_id]  # Recupera o estado atual da conversa para o user_id fornecido.
    user_input = user_input

    # início da conversa
    if state == 'start':
        if "start" in user_input:
            conversation_state[user_id] = 'coletando_nome'  
            return "Olá! Bem-vindo à MF Solar, sua solução para energia solar eficiente e econômica. Posso ajudar você a encontrar o sistema de energia solar perfeito para sua casa ou empresa. Qual é o seu nome?"  # Responde com a mensagem inicial.

    
    elif state == 'coletando_nome':
        conversation_state[user_id] = 'uso'  # Atualiza o estado perguntando sobre o uso
        return f"Prazer em conhecê-lo, {user_input}! Para começar, você está interessado em um sistema de energia solar para sua casa ou para sua empresa?\n\n1)Casa\n2)Empresa"  # Responde com uma pergunta sobre o tipo de uso (residencial ou comercial).

    # Se o estado for perguntando sobre o uso
    elif state == 'uso':
        if "1" in user_input:
            conversation_state[user_id] = 'uso_kw'  # Atualiza o estado perguntando sobre o consumo em kW na residencia
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua residência consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        elif "2" in user_input:
            conversation_state[user_id] = 'uso_kw'  # Atualiza o estado perguntando sobre o consumo em kW na empresa
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua empresa consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        else:
            return "Desculpe, não entendi. Por favor, escolha 1) para Casa ou 2) para Empresa."  # Resposta padrão para entradas inválidas.


# Executado apenas no arquivo principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Inicia o servidor Flask, tornando o aplicativo disponível na rede local.
