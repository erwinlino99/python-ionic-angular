from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) 
connection=MySQL(app)

@app.route('/test')
def index():
      return jsonify({"response": "API DE ERWIN"})
# PARA USUARIOS -->
# PARA USUARIOS -->






















@app.route('/users',methods=['GET'])
def listUsers():
    try:
        cursor=connection.connection.cursor()
        sql="SELECT * from users"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(users)
    except Exception as e:
        return e

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        cursor = connection.connection.cursor()
        sql = f"SELECT * FROM users WHERE id = {id}"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        user = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(user)
    except Exception as e:
        return str(e)
    
    



    
# REGISTRO DE USUARIO -->
@app.route('/users', methods=['POST'])
def add_user():
    try:
        attribute = '[]'
        user_data = request.json
        cursor = connection.connection.cursor()
        sql = "INSERT INTO users (username, password_hash, email, domicile, phone, bornDate, wishlist, cart) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (  
            user_data['username'],
            user_data['password_hash'],
            user_data['email'],
            user_data['domicile'],
            user_data['phone'],
            user_data['bornDate'],attribute, attribute))
        connection.connection.commit()
        cursor.close()
        return "USUARIO AGREGADO"
    except Exception as e:
        return str(e)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:        
        update_user_data = request.json
        cursor = connection.connection.cursor()
        sql = "UPDATE users SET username = %s, email = %s, phone = %s, domicile = %s, bornDate = %s, password_hash = %s WHERE id = %s"
        cursor.execute(sql, (update_user_data['username'], update_user_data['email'], update_user_data['phone'], update_user_data['domicile'], update_user_data['bornDate'], update_user_data['password_hash'], id))
        connection.connection.commit()
        cursor.close()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# PARA LA LISTA DE DESEADOS/FAVORITOS --->
# PARA LA LISTA DE DESEADOS/FAVORITOS --->
@app.route('/wishlist/<int:id>', methods=['GET'])
def bringWishlist(id):
    try:
        cursor = connection.connection.cursor()
        sql = f"SELECT wishlist FROM users WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            wishlist = json.loads(result[0])
            return jsonify(wishlist)
        else:
            return "Usuario no encontrado"
    except Exception as e:
        return str(e)

    
@app.route('/wishlist/<int:id>', methods=['PUT'])
def updateWishlist(id):
    try:
        # Aqui recibo los datos del Fronted
        frontend_data = request.json
        # Lo convertimos de formato Json a String para luego meterlo en el campo deseado
        frontend_data_str = json.dumps(frontend_data)
        cursor = connection.connection.cursor()
        sql = f"UPDATE USERS SET WISHLIST = %s WHERE id = %s"
        # Ejecucion del cursor
        cursor.execute(sql, (frontend_data_str, id))
        connection.connection.commit()
        return 'Lista de deseos actualizada correctamente',200
    except Exception as e:
        return str(e)
    

# PARA LA LISTA DE CARRITO --->
# PARA LA LISTA DE CARRITO --->
@app.route('/cart/<int:id>', methods=['GET'])
def bringCart(id):
    try:
        cursor = connection.connection.cursor()
        sql = f"SELECT cart FROM users WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            wishlist = json.loads(result[0])  # Convertir la cadena JSON en una lista de Python
            return jsonify(wishlist)
        else:
            return "Usuario no encontrado"
    except Exception as e:
        return str(e)

# EXPLICAR ESTO 
@app.route('/cart/<int:id>', methods=['PUT'])
def updateCart(id):
    try:
        # Aqui recupero lo que el front me envia
        frontend_data = request.json
        print(frontend_data)
        # lo transformo a un formato json y lo meto en columna correspondiente
        frontend_data_str = json.dumps(frontend_data)
        # Hago conexion a la BBDD
        cursor = connection.connection.cursor()
        sql = f"UPDATE USERS SET CART = %s WHERE id = %s"
        cursor.execute(sql, (frontend_data_str, id))
        connection.connection.commit()
        return 'Se ha agregado al carrito',200
    except Exception as e:
        return str(e)

# //! ME QUEDE AQUI 
@app.route('/cart/<int:id>', methods=['DELETE'])
def delete_cart(id):
    try:
        front_data = request.json
        data = json.dumps(front_data)
        cursor = connection.connection.cursor()
        cursor.execute('SELECT cart FROM users WHERE id = %s', (id,))
        current_data = cursor.fetchone()[0]
        obj = json.loads(current_data)
        print(obj)
        for product in obj:
            if product['id'] == front_data['id']:
                obj.remove(product)
                break
        update_data = json.dumps(obj)
        sql = "UPDATE users SET cart = %s WHERE id = %s"
        cursor.execute(sql, (update_data, id))
        connection.connection.commit()
        return jsonify({'message': 'Producto eliminado del carrito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/products',methods=['GET'])
def listProduct():
    try:
        cursor=connection.connection.cursor()
        sql="SELECT * from products"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(products)
    except Exception as e:
        return e
 
    
@app.route('/products/<int:id>', methods=['GET'])
def bringProduct(id):
    try:
        cursor = connection.connection.cursor()
        sql = f"SELECT * FROM products WHERE id = {id}"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        # DE ESTA FORMA SE PUEDEN VER CLAVE-VALOR
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(products)
    except Exception as e:
        return str(e)
    
@app.route('/products/<int:id>', methods=['PUT'])
def updateProduct(id):
    try:
        prod = request.json
        times = prod['times']
        cursor = connection.connection.cursor()
        # Verificar el stock actual
        cursor.execute('SELECT STOCK FROM PRODUCTS WHERE ID = %s', (id,))
        current_stock = cursor.fetchone()[0]
        # Verificar si el stock resultante sería negativo
        if current_stock - times < 0:
            return jsonify({'error': 'Stock insuficiente'}), 400
        # Actualizar el stock
        sql = 'UPDATE PRODUCTS SET STOCK = STOCK - %s WHERE ID = %s'
        cursor.execute(sql, (times, id))
        connection.connection.commit()
        
        return jsonify({'message': 'Producto actualizado stock'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400 
    
@app.route('/products', methods=['POST'])
def addProduct():
    try:
        # Obtener los datos del producto del cuerpo de la solicitud JSON
        product_data = request.json
        # Conectar a la base de datos
        cursor = connection.connection.cursor()
        # Construir y ejecutar la consulta SQL de inserción
        sql = "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (product_data['name'], product_data['category'], product_data['price'], product_data['stock']))
        # Confirmar la accion de que se ha metido en la BBDD
        connection.connection.commit()
        cursor.close()
        return "Productor registrado correctamente"
    except Exception as e:
        return str(e)

    
# Cuando un endopint no existe -->
def not_found(error):
    return "<h1>Esta pagina no existe manin</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['dev'])
    app.register_error_handler(404,not_found)
    app.run()
