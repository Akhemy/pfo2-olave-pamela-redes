import sqlite3
import sys

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Se fuerza UTF-8 en la salida de la consola porq Windows a veces usa otra
# codificacion, y eso podria hacer q los acentos se vean mal en los mensajes
# q imprime el servidor al arrancar
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

HOST = 'localhost'
PUERTO = 5000
NOMBRE_DB = 'tareas.db'


def inicializar_db():
    # Se crea la tabla de usuarios si todavia no existe, para q el servidor
    # pueda reiniciarse sin perder los datos ni fallar por tabla duplicada
    try:
        conn_db = sqlite3.connect(NOMBRE_DB)
        cursor = conn_db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena_hash TEXT NOT NULL
            )
        ''')
        conn_db.commit()
        conn_db.close()
    except sqlite3.Error as error:
        print(f"No se pudo acceder a la base de datos: {error}")
        raise


def obtener_conexion():
    # Flask atiende las peticiones con varios hilos y una conexion sqlite3 no
    # se puede compartir entre hilos, por eso se abre una conexion nueva en
    # cada peticion y se cierra apenas termina de usarse
    return sqlite3.connect(NOMBRE_DB)


def verificar_credenciales(usuario, contrasena):
    # Busca el usuario en la base y compara la contraseña contra el hash
    # guardado. Devuelve True solo si el usuario existe y la contraseña coincide
    conn_db = obtener_conexion()
    cursor = conn_db.cursor()
    cursor.execute('SELECT contrasena_hash FROM usuarios WHERE usuario = ?', (usuario,))
    fila = cursor.fetchone()
    conn_db.close()

    if fila is None:
        return False
    return check_password_hash(fila[0], contrasena)


@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos: se necesita usuario y contraseña"}), 400

    # Las contraseñas se guardan hasheadas con werkzeug.security porq esta
    # libreria ya viene incluida con Flask (no suma dependencias nuevas) y
    # asi nunca se guarda la contraseña en texto plano en la base de datos
    contrasena_hash = generate_password_hash(contrasena)

    conn_db = obtener_conexion()
    cursor = conn_db.cursor()
    try:
        cursor.execute(
            'INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)',
            (usuario, contrasena_hash)
        )
        conn_db.commit()
    except sqlite3.IntegrityError:
        # Salta aca si el usuario ya existe, porq la columna usuario es UNIQUE
        return jsonify({"error": "El usuario ya existe"}), 409
    finally:
        conn_db.close()

    return jsonify({"mensaje": "Usuario registrado"}), 201


@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos: se necesita usuario y contraseña"}), 400

    if not verificar_credenciales(usuario, contrasena):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    return jsonify({"mensaje": "Login exitoso"}), 200


@app.route('/tareas', methods=['GET'])
def tareas():
    auth = request.authorization

    if auth is None or not verificar_credenciales(auth.username, auth.password):
        # Sin el header WWW-Authenticate el cliente no sabe q tiene q
        # mandar usuario y contraseña con Basic Auth
        return 'No autorizado', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

    html = f'''
    <html>
        <body>
            <h1>Bienvenido, {auth.username}</h1>
        </body>
    </html>
    '''
    return html, 200


def main():
    inicializar_db()
    print(f"El servidor queda escuchando en {HOST}:{PUERTO}")
    app.run(host=HOST, port=PUERTO)


if __name__ == '__main__':
    main()
