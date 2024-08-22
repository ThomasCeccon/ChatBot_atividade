from flask import Flask, jsonify, render_template, request

# Instancia a classe Flask
app = Flask(__name__)  

 # Dicionario que armazena o estado atual da conversa de cada usuario
conversation_state = {} 

# Rotas de acesso
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')# Define a rota para a pagina inicial

# Rota de duvidas
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
    user_input = request.json.get('message')  # Obtem a mensagem enviada pelo usuario
    user_id = request.json.get('user_id')  # Obtem o identificador unico do usuario

    # Atualiza o estado da conversa do usuário
    if user_id not in conversation_state:
        # Se o user_id nao está no dicionario de estados, significa que este é um novo usuario, então inicializamos o estado dele como 'start'
        conversation_state[user_id] = 'start'
    
    response = generate_response(user_input, user_id)  # Gera uma resposta com base na entrada do usuario e no estado atual da conversa

    return jsonify({'response': response})  # Retorna a resposta como um JSON para o frontend

# Função para gerar resposta
def generate_response(user_input, user_id):
    # Funcao principal que gera a resposta do chatbot com base no estado da conversa e na entrada do usuario
    state = conversation_state[user_id]  # Recupera o estado atual da conversa para o user_id fornecido
    user_input = user_input

    # inicio da conversa
    if state == 'start':
        if "start" in user_input:
            conversation_state[user_id] = 'coletando_nome'  
            return "Olá! Bem-vindo à MF Solar, sua solução para energia solar eficiente e econômica. Posso ajudar você a encontrar o sistema de energia solar perfeito para sua casa ou empresa. Qual é o seu nome?"  # Responde com a mensagem inicial.

    elif state == 'coletando_nome':
        conversation_state[user_id] = 'uso'  # Atualiza o estado perguntando sobre o uso
        return f"Prazer em conhecê-lo, {user_input}! Para começar, você está interessado em um sistema de energia solar para sua casa ou para sua empresa?\n\nDigite [1] Casa\n[2] Empresa"  # Responde com uma pergunta sobre o tipo de uso (residencial ou comercial).

    # Se o estado for perguntando sobre o uso
    elif state == 'uso':
        if "1" in user_input:
            conversation_state[user_id] = 'uso_kw'  # Atualiza o estado perguntando sobre o consumo em kW na residencia
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua residência consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        elif "2" in user_input:
            conversation_state[user_id] = 'uso_kw'  # Atualiza o estado perguntando sobre o consumo em kW na empresa
            return "Ótimo! Quantos quilowatts (kW) de energia você acredita que sua empresa consome por mês? Se não souber, sem problemas, podemos estimar isso juntos."
        else:
            return "Desculpe, não entendi. Por favor, Digite [1] para Casa ou [2] para Empresa."  # Resposta padrao para entradas invalidas.
        
          # Se o estado for 'uso_kw' perguntando sobre o consumo em kW
    elif state == 'uso_kw':
        conversation_state[user_id] = 'tipo_telhado'  # Atualiza o estado perguntando sobre o tipo de telhado
        return "Entendi. Agora, você tem algum tipo de telhado específico em mente? Por exemplo, telhado inclinado, plano, metálico, etc."

    # perguntando sobre o tipo de telhado
    elif state == 'tipo_telhado':
        conversation_state[user_id] = 'inter_externa'  # Atualiza o estado perguntando sobre sombreamento
        return "Perfeito. Para oferecer a melhor solução, preciso saber: você possui algum tipo de sombreamento em sua área de instalação, como árvores ou prédios?\n\n[1]Sim\n[2]Não"

    # Se o estado for 'inter_externa' perguntando sobre o sombreamento
    elif state == 'inter_externa':
        if "1" in user_input or "2" in user_input:
            conversation_state[user_id] = 'objetivo_principal'  # Atualiza o estado perguntando sobre o objetivo principal
            return "Entendi. Agora, qual é o seu objetivo principal com a instalação do sistema de energia solar? Reduzir contas de energia, aumentar a sustentabilidade, ou outro?"
        else:
            return "Desculpe, não entendi. Você pode escolher [1] para Sim ou [2] para Não."  # Resposta padrão para entradas invalidas.

    elif state == 'objetivo_principal':
        conversation_state[user_id] = 'coletando_endereco'  # Atualiza o estado para coletar o endereço
        return "Excelente escolha. Para que possamos fornecer uma cotação personalizada, preciso de algumas informações adicionais. Qual é o seu endereço completo?"

    # Se o estado for 'coletando_endereço' coletando o endereço
    elif state == 'coletando_endereco':
        conversation_state[user_id] = 'coletando_telefone'  # Atualiza o estado para coletar o telefone
        return "Obrigado. E qual é o melhor número de telefone para que possamos entrar em contato com você para uma consulta detalhada?"

    # Se o estado for 'coletando_telefone'
    elif state == 'coletando_telefone':
        conversation_state[user_id] = 'coletando_email'  # Atualiza o estado para coletar o e-mail
        return "Obrigado. E qual é o seu e-mail para que possamos enviar uma proposta e mais informações sobre nossos sistemas de energia solar?"

    # Se o estado for coletando o e-mail
    elif state == 'coletando_email':
        conversation_state[user_id] = 'completo'  # Atualiza o estado para 'completo' para conversa concluída
        return "Ótimo! Recebemos todas as suas informações. Um de nossos especialistas em energia solar entrará em contato com você em breve para fornecer uma cotação detalhada e responder a qualquer dúvida que você possa ter. Agradecemos pelo seu interesse na MF Solar! Se precisar de mais alguma coisa, não hesite em nos chamar. Tenha um ótimo dia!"

    # Se o estado for 'completo' para conversa concluída
    elif state == 'completo':
        return "Obrigado por sua interação. Se precisar de mais alguma coisa, estamos à disposição."  # Resposta final quando o processo foi concluído

    return "Desculpe, não entendi. Por favor, forneça uma resposta válida."  # Resposta padrão para entradas invalidas ou casos inesperados


# Executado apenas no arquivo principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Inicia o servidor Flask, tornando o aplicativo disponivel na rede local
