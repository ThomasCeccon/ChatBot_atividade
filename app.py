from flask import Flask, jsonify, render_template, request
import re  #regex

# Instancia a classe Flask
app = Flask(__name__)

# Dicionário que armazena o estado atual da conversa de cada usuário
conversation_state = {}

# Função para validar texto
def is_valid_text(text):
    return bool(text) and not any(char.isdigit() for char in text)

# Função para validar telefone (simplificação)
def is_valid_phone(phone):
    return bool(phone) and re.match(r'^\d{10,15}$', phone)

# Função para validar e-mail
def is_valid_email(email):
    return bool(email) and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

# Rotas de acesso
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')  # Define a rota para a página inicial

# Rota de dúvidas
@app.route('/duvidas')
def duvidas():
    return render_template('duvidas.html')

# Rota de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Rota do chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Obtém a mensagem enviada pelo usuário
    user_id = request.json.get('user_id')  # Obtém o identificador único do usuário

    # Atualiza o estado da conversa do usuário
    if user_id not in conversation_state:
        # Se o user_id não está no dicionário de estados, significa que este é um novo usuário, então inicializamos o estado dele como 'start'
        conversation_state[user_id] = 'start'
    
    response = generate_response(user_input, user_id)  # Gera uma resposta com base na entrada do usuário e no estado atual da conversa

    return jsonify({'response': response})  # Retorna a resposta como um JSON para o frontend

# Função para gerar resposta
def generate_response(user_input, user_id):
    state = conversation_state[user_id]  # Recupera o estado atual da conversa para o user_id fornecido

    if state == 'start':
        if "start" in user_input.lower():
            conversation_state[user_id] = 'coletando_nome'
            return "Olá! Bem-vindo à MF Solar, sua solução para energia solar eficiente e econômica. Posso ajudar você a encontrar o sistema de energia solar perfeito para sua casa ou empresa. Qual é o seu nome?"

    elif state == 'coletando_nome':
        if is_valid_text(user_input):
            conversation_state[user_id] = 'uso'
            return f"Prazer em conhecê-lo, {user_input}! Para começar, você está interessado em um sistema de energia solar para sua casa ou para sua empresa?\n\nDigite [1] Casa\n[2] Empresa"
        else:
            return "Por favor, insira um nome válido (somente texto)."

    elif state == 'uso':
        if "1" in user_input:
            conversation_state[user_id] = 'uso_kw'
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua residência consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        elif "2" in user_input:
            conversation_state[user_id] = 'uso_kw'
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua empresa consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        else:
            return "Desculpe, não entendi. Por favor, Digite [1] para Casa ou [2] para Empresa."

    elif state == 'uso_kw':
        conversation_state[user_id] = 'tipo_telhado'
        return "Entendi. Agora, você tem algum tipo de telhado específico em mente? Por exemplo, telhado inclinado, plano, metálico, etc."

    elif state == 'tipo_telhado':
        conversation_state[user_id] = 'inter_externa'
        return "Perfeito. Para oferecer a melhor solução, preciso saber: você possui algum tipo de sombreamento em sua área de instalação, como árvores ou prédios?\n\n[1]Sim\n[2]Não"

    elif state == 'inter_externa':
        if "1" in user_input or "2" in user_input:
            conversation_state[user_id] = 'objetivo_principal'
            return "Entendi. Agora, qual é o seu objetivo principal com a instalação do sistema de energia solar? Reduzir contas de energia, aumentar a sustentabilidade, ou outro?"
        else:
            return "Desculpe, não entendi. Você pode escolher [1] para Sim ou [2] para Não."

    elif state == 'objetivo_principal':
        conversation_state[user_id] = 'coletando_endereco'
        return "Excelente escolha. Para que possamos fornecer uma cotação personalizada, preciso de algumas informações adicionais. Qual é o seu endereço completo?"

    elif state == 'coletando_endereco':
        if is_valid_text(user_input):
            conversation_state[user_id] = 'coletando_telefone'
            return "Obrigado. E qual é o melhor número de telefone para que possamos entrar em contato com você para uma consulta detalhada?"
        else:
            return "Por favor, insira um endereço válido (somente texto)."

    elif state == 'coletando_telefone':
        if is_valid_phone(user_input):
            conversation_state[user_id] = 'coletando_email'
            return "Obrigado. E qual é o seu e-mail para que possamos enviar uma proposta e mais informações sobre nossos sistemas de energia solar?"
        else:
            return "Por favor, insira um número de telefone válido (somente números)."

    elif state == 'coletando_email':
        if is_valid_email(user_input):
            conversation_state[user_id] = 'completo'
            return "Ótimo! Recebemos todas as suas informações. Um de nossos especialistas em energia solar entrará em contato com você em breve para fornecer uma cotação detalhada e responder a qualquer dúvida que você possa ter. Agradecemos pelo seu interesse na MF Solar! Se precisar de mais alguma coisa, não hesite em nos chamar. Tenha um ótimo dia!"
        else:
            return "Por favor, insira um e-mail válido."

    elif state == 'completo':
        return "Obrigado por sua interação. Se precisar de mais alguma coisa, estamos à disposição."

    return "Desculpe, não entendi. Por favor, forneça uma resposta válida."

# Executado apenas no arquivo principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Inicia o servidor Flask, tornando o aplicativo disponível na rede local
