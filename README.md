# Sistema de Gestion de Tareas con API y Base de Datos

## Descripcion

API REST hecha con Flask que permite registrar usuarios, iniciar sesi on y acceder a una pagina de bienvenida protegida con autenticaci on basica (HTTP Basic Auth). Los usuarios persisten en una base de datos SQLite, con las contraseñas guardadas como hash. Incluye un cliente de consola que consume la API usando la libreria requests.

## Requisitos

- Python 3
- pip

## Instalacion

1. Clonar o descargar este repositorio.
2. Crear un entorno virtual:
   - Windows: python -m venv venv
   - Linux/Mac: python3 -m venv venv
3. Activar el entorno virtual:
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate
4. Instalar las dependencias:
   pip install -r requirements.txt

## Como ejecutar

1. En una terminal (con el entorno virtual activado): python servidor.py
2. En otra terminal (con el entorno virtual activado): python cliente.py

## Como probar con curl

### Registro

curl -X POST http://localhost:5000/registro -H "Content-Type: application/json" -d "{\"usuario\": \"pame\", \"contraseña\": \"1234\"}"

Respuesta esperada (201): {"mensaje": "Usuario registrado"}

### Login

curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"usuario\": \"pame\", \"contraseña\": \"1234\"}"

Respuesta esperada (200): {"mensaje": "Login exitoso"}

### Ver tareas (con credenciales)

curl -u pame:1234 http://localhost:5000/tareas

Respuesta esperada (200): un HTML con el texto "Bienvenido, pame".

### Ver tareas (sin credenciales)

curl http://localhost:5000/tareas

Respuesta esperada (401): "No autorizado".

## Capturas de pantalla

Las capturas se encuentran en la carpeta capturas/:

- registro_exitoso.png: registro de un usuario nuevo.
- login_exitoso.png: login con credenciales correctas.
- login_fallido_usuario_incorrecto.png: login con un usuario que no existe.
- login_fallido_contrasena_incorrecta.png: login con la contraseña incorrecta para un usuario que si existe.
- tareas_con_credenciales.png: acceso a tareas con usuario y contraseña validos.
- tareas_sin_credenciales.png: acceso a tareas sin credenciales (401).

Nota: en los dos casos de login fallido, el servidor responde con el mismo mensaje generico ("Usuario o contraseña incorrectos"), sin aclarar cual de los dos datos estaba mal. Es una medida de seguridad para no revelar q nombres de usuario existen en el sistema.

## Preguntas conceptuales

### Por que hashear contraseñas?

Porq si alguien accede a la base de datos sin permiso, las contraseñas no qdan expuestas en texto plano. El hash es una transformaci on q no se puede revertir: aunq se vea el valor guardado, no se puede saber cual era la contraseña original. Al hacer login no se compara la contraseña real, sino que se vuelve a calcular el hash de lo q escribió el usuario y se compara contra el hash guardado.

### Ventajas de usar SQLite en este proyecto

La ventaja es que con SQLite no se necesita instalar ni configurar un servidor de base de datos aparte: todo queda guardado en un solo archivo (tareas.db) dentro del proyecto, lo que lo hace simple para un proyecto chico como este. Ademas viene incluido en la libreria Python, asi q no es necesario instalar nada.

## Nota sobre GitHub Pages

GitHub Pages solo aloja archivos estaticos (HTML, CSS, JS); no puede ejecutar un servidor Flask ni codigo Python. Por eso esta pagina tiene solo la documentacion, mientras que la API real (servidor.py) se tiene que ejecutar localmente en la propia computadora, siguiendo los pasos de la seccion "Como ejecutar".
