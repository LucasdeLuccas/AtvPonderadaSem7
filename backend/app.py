from flask import Flask, render_template, request, jsonify
from modals import PosicaodoRobo
import pydobot
import serial.tools.list_ports
from flask_cors import CORS 

app = Flask(__name__, template_folder='.././frontend/templates') #Caminho para o template

CORS(app)

import os

db_dir = os.path.join(os.path.dirname(__file__), '..', 'Banco de Dados')
os.makedirs(db_dir, exist_ok=True)  # Cria o diretório se ele não existir
db_path = os.path.join(db_dir, 'banco.json')  # Caminho para o banco de dados
db = PosicaodoRobo(db_path)  # Instanciação com o caminho correto



#Classe para o robô

class InteliArm(pydobot.Dobot):
    def __init__(self, port=None, verbose=False):
        super().__init__(port=port, verbose=verbose)
    
    def movej_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)

    def movel_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVL_XYZ, wait=wait)


def encontrar_porta(porta_desejada):
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        if porta.device == porta_desejada:
            return porta.device
    return None


def criar_robot():
    porta_escolhida = encontrar_porta('COM6')
    if porta_escolhida is not None:
        return InteliArm(port=porta_escolhida, verbose=False)
    else:
        return None
    

atuador_ligado = False

def check_movement(desired, actual, tolerance=3):
    return all(abs(d - a) <= tolerance for d, a in zip(desired, actual))

#Código para a rota inicial
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

#Código para a rota de controles
@app.route('/control', methods=['GET'])
def controles():
    return render_template('control.html')

#Código para a rota de log
@app.route('/log' , methods=['GET'])
def log():
    valores = db.valores()
    return render_template('log.html', logs=valores)





#Código para a rota de home
@app.route('/home', methods=["GET", "POST"])
def home():
    robot = criar_robot()
    if robot is not None:
        print(f'Dobot conectado com sucesso')
    else:
        print('Porta do Dobot não encontrada.')
    
    inicial_posicao = (240, 0, 150, 0) #posição inicial do robô

    try:
        robot.move_to(240,0,150,0, wait=True)
        posicao = robot.pose()

        db.coordenadas_add(*inicial_posicao)

        return jsonify({'success': True, 'message': 'Position inserted successfully.', 'Posição': posicao})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



# Rota para pegar a posição atual do ROBO e ele devolve uma lista em json   
@app.route('/posicao_atual', methods=['GET'])
def pos_atual():
    robot = criar_robot()

    if robot is not None:
        print(f'Dobot conectado!')
    else:
        print('Verifique a porta.')

    posicao = robot.pose()

    posicao_data = {
        'x': posicao[0],
        'y': posicao[1],
        'z': posicao[2],
        'r': posicao[3]
    }
    return jsonify(posicao_data)


    


@app.route('/movimentacao', methods=['GET', 'POST'])
def movimento():
    robot = criar_robot()
    if robot is not None:
        print(f'Dobot conectado com sucesso')
        if request.method == 'POST':
            content = request.form #recebendo os dados do formulário

            if not all(key in content for key in ('x', 'y', 'z', 'r')):
                return jsonify({'success': False, 'message': 'Missing one or more required fields: x, y, z, r.'}), 400

            try:
                posicao = (int(content['x']), int(content['y']), int(content['z']), int(content['r']))
            except ValueError:
                
                return jsonify({'success': False, 'message': 'All coordinates must be integer values.'}), 400
            
            try:
                print(*posicao)
                robot.movej_to(*posicao, wait=True)
                posicao_atual = robot.pose()
                db.coordenadas_add(*posicao_atual)

                return jsonify({"status": "Sucesso", "mensagem":"Posicionamento realizado com sucesso."})
            except Exception as e:

                return jsonify({'success': False, 'message': str(e)}), 500
        else:
            return jsonify({'success': False, 'message': 'Method Not Allowed'}), 405
    else:
        return jsonify({'success': False, 'message': 'Porta do Dobot não encontrada.'}), 404
                
                
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

    