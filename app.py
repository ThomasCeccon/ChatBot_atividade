
#importando as classes
from flask import Flask,jsonify,render_template
from flask import request

#instancias a classe flask
app = Flask(__name__)

#rotas de acesso
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

#executado apenas no arquivo principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) #executar o flask
   

