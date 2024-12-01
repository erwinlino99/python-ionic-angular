from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS

# MODELOS 
from model.web_user import WebUser;


app = Flask(__name__)
CORS(app) 
connection=MySQL(app)

@app.route('/test')
def index():
      return jsonify({"response": "API DE ERWIN"})
# PARA USUARIOS -->
# PARA USUARIOS -->

@app.route('/web_user', methods=['POST'])
def login():
    try:
        
        dataUser = request.json  # Recibe los datos como JSON
        email = dataUser.get('email')
        password = dataUser.get('password')
        return jsonify({"ESTO ES LO QUE QUIERO METER": dataUser})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/new_user', methods=['POST'])
def newUser():
    try:
        
        # SEGUIR HACIENDO ESTO PARA DAR DE ALTA A LA BBDD
        dataUser = request.json  
        return jsonify(dataUser)

    except Exception as e:
        return jsonify({'error': str(e)}), 500






















# Cuando un endopint no existe -->
def not_found(error):
    return "<h1>Esta pagina no existe manin</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['dev'])
    app.register_error_handler(404,not_found)
    app.run()
