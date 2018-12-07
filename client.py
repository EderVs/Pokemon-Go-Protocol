"""
    Pokemon Go Protocol Client
"""
import socket

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


def get_code_bytes(code):
    return bytes([code])


def get_code_from_bytes(code_b):
    return int.from_bytes(code_b)


def get_pokemon(pokemon_id):
    return pokemons.get(pokemon_id, {})


def connect_to_server(sock):
    code = 10
    data = get_code_bytes(code)
    id_trainer = int(input('Who are you, Trainer?:'))
    data += get_code_bytes(id_trainer)
    sock.send(data)


def capturar_pokemon(sock):
    response = sock.recv(2)
    print(response)
    if response[0] != SERVER_CAPTURE:
        return None
    pokemon = get_pokemon(response[1])
    capturar_pokemon_ = str(input("Capturar a", pokemon.get('name', ''), "?")) == 'si'
    if not capturar_pokemon:
        data = get_code_bytes(BOTH_NO)
        print("Nos vemos entrenador!")
        sock.send(data)
        return None
    data = get_code_bytes(BOTH_YES)
    sock.send(data)
    response = sock.recv(3)
    while response[0] == SERVER_CAPTURE_AGAIN:
        print("No pudiste capturar a" , pokemon.get('name', ''))
        capturar_pokemon_ = str(input("Seguir capturando a", pokemon.get('name', ''), "?")) == 'si'
        if not capturar_pokemon:
            data = get_code_bytes(BOTH_NO)
            print("Nos vemos entrenador!")
            sock.send(data)
            return None
        data = get_code_bytes(BOTH_YES)
        sock.send(data)
        response = sock.recv(3)
    if response[0] == SERVER_SEND_POKEMON:
        print(pokemon.get('name', ''), "capturado!")
    elif response[0] == SERVER_RUN_OUT_ATTEMPTS:
        print("Se acabaron los Intentos :(")
        print("Nos vemos entrenador!")
    else:
        print("Sucedió un error :(")
    sock.close()
    return None



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(input("Server hostname or ip? "))
port = int(input("Server port? "))
sock.connect((host, port))
connect_to_server(sock)
capturar_pokemon(sock)
sock.close()
