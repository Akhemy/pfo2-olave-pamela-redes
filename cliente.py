import sys

import requests

# Se fuerza UTF-8 en la entrada y salida de la consola, igual q en el TP 1,
# para q los acentos se vean bien sin importar como este configurada Windows
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

URL_BASE = 'http://localhost:5000'

# Se guardan aca las credenciales del usuario logueado, para poder usarlas
# despues en "Ver tareas" (Basic Auth) sin tener q pedirlas de nuevo
usuario_actual = None
contrasena_actual = None


def registrar():
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    try:
        respuesta = requests.post(
            f"{URL_BASE}/registro",
            json={"usuario": usuario, "contraseña": contrasena}
        )
    except requests.exceptions.ConnectionError:
        # Si el servidor no esta corriendo, se avisa al usuario en vez de q
        # el programa se corte con un traceback (misma correccion q en el TP 1)
        print(f"No se pudo conectar: el servidor no está corriendo en {URL_BASE}")
        return

    print(f"Código: {respuesta.status_code}")
    print(respuesta.json())


def iniciar_sesion():
    global usuario_actual, contrasena_actual

    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    try:
        respuesta = requests.post(
            f"{URL_BASE}/login",
            json={"usuario": usuario, "contraseña": contrasena}
        )
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar: el servidor no está corriendo en {URL_BASE}")
        return

    print(f"Código: {respuesta.status_code}")
    print(respuesta.json())

    # Solo se guardan las credenciales si el login fue exitoso, para usarlas
    # despues en "Ver tareas"
    if respuesta.status_code == 200:
        usuario_actual = usuario
        contrasena_actual = contrasena


def ver_tareas():
    if usuario_actual is None:
        print("Primero tenés q iniciar sesión")
        return

    try:
        respuesta = requests.get(
            f"{URL_BASE}/tareas",
            auth=(usuario_actual, contrasena_actual)
        )
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar: el servidor no está corriendo en {URL_BASE}")
        return

    print(f"Código: {respuesta.status_code}")
    print(respuesta.text)


def main():
    while True:
        print("\n1. Registrarse\n2. Iniciar sesión\n3. Ver tareas\n4. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == '1':
            registrar()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            ver_tareas()
        elif opcion == '4':
            break
        else:
            print("Opción inválida")


if __name__ == '__main__':
    main()
