"""
    Pokemon Go Protocol Client
"""
import socket

trainers = {
    1: {'id': 1, 'name': 'ASH',   'pokemons': []},
    2: {'id': 2, 'name': 'SAMUS', 'pokemons': []},
    3: {'id': 3, 'name': 'MARIO', 'pokemons': []},
    4: {'id': 4, 'name': 'SONIC', 'pokemons': []},
}

pokemons = {
    1: {'id': 1, 'name': 'Pikachu'},
    2: {'id': 2, 'name': 'Squirtle'},
    3: {'id': 3, 'name': 'Charmander'},
    4: {'id': 4, 'name': 'Lucario'},
    5: {'id': 5, 'name': 'Mew'},
    6: {'id': 6, 'name': 'MewTwo'}
}

CLIENT_CAPTURE = 10
SERVER_CAPTURE = 20
SERVER_CAPTURE_AGAIN = 21
SERVER_SEND_POKEMON = 22
SERVER_RUN_OUT_ATTEMPTS = 23
BOTH_YES = 30
BOTH_NO = 31
BOTH_FINISH = 32
ERROR_WRONG_CODE = 40
ERROR_WRONG_TRAINER = 41
ERROR_CONNECTION_CLOSED = 42


def get_code_bytes(code):
    return bytes([code])


def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def get_pokemon(pokemon_id):
    return pokemons.get(pokemon_id, {})


def connect_to_server(sock):
    code = 10
    data = get_code_bytes(code)
    id_trainer = int(input('¿Qué entrenador eres?:'))
    data += get_code_bytes(id_trainer)
    sock.send(data)
    return trainers.get(id_trainer, {})


def check_if_the_connection_is_closed(code):
    return code == ERROR_CONNECTION_CLOSED
    
    
def capturar_pokemon(sock, trainer):
    response = sock.recv(2)
    print(response[0])
    if response[0] != SERVER_CAPTURE: #code 20
        if check_if_the_connection_is_closed(response[0]):
            print("El servidor cerró la conexión")
        elif response[0] == ERROR_WRONG_TRAINER:
            print("El entrenador que ingresaste no existe")
        else:
            print("Sucedió un error :(")
        return None

    # Ya que se pasó el filtro de los posibles errores damos la bienvenida
    print("¡Bienvenido", trainer['name'],"!")

    pokemon = get_pokemon(response[1])
    quiere_pokemon = 'si' ==  str(input("¿Quieres capturar a " + pokemon.get('name', '') + "? "))
    if not quiere_pokemon:
        data = get_code_bytes(BOTH_NO)
        print("¡Nos vemos entrenador!")
        sock.send(data)
        return None
    data = get_code_bytes(BOTH_YES)
    data += get_code_bytes(1)
    sock.send(data)
    response = sock.recv(3)
    while response[0] == SERVER_CAPTURE_AGAIN:
        # Mensajes al cliente
        print("No pudiste capturar a" , pokemon.get('name', ''), ".")
        print("Te queda(n)", response[2], "intento(s).\n")
        quiere_pokemon = 'si' == str(input("¿Quieres intentar capturar a " + pokemon.get('name', '') + " de nuevo? "))
        if not quiere_pokemon:
            data = get_code_bytes(BOTH_NO)
            sock.send(data)
            print("¡Nos vemos entrenador!")
            return None
        data = get_code_bytes(BOTH_YES)
        sock.send(data)
        response = sock.recv(3)
    if response[0] == SERVER_SEND_POKEMON:
        print("!"+pokemon.get('name', ''), "capturado!")
        # Gets the size of the file
        size = bytes_to_int(response[2:3] + sock.recv(3))
        # Receives the file bytes
        image_bytes = sock.recv(size)
        # Writes the file
        out_file = open("client_pokemons/" + pokemon['name'] + ".jpg", "wb")
        out_file.write(image_bytes)
        out_file.close()
        print("Se guardó tu pokemon en: client_pokemons/" + pokemon['name'] + ".jpg")
    elif response[0] == SERVER_RUN_OUT_ATTEMPTS:
        print("Se acabaron los Intentos :(")
        print("¡Nos vemos entrenador!")
    elif check_if_the_connection_is_closed(response[0]):
        print("El servidor cerró la conexión")
    else:
        print("Sucedió un error :(")
    return None



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(input("Server hostname o ip? "))
port = int(input("Server port? "))
sock.connect((host, port))
trainer = connect_to_server(sock)
capturar_pokemon(sock, trainer)
sock.close()
