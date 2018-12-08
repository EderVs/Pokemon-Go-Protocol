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
numAttemps = 3

def get_code_bytes(code):
    return bytes([code])


def get_code_from_bytes(code_b):
    return int.from_bytes(code_b)


def get_pokemon(pokemon_id):
    return pokemons.get(pokemon_id, {})


def connect_to_server(sock):
    code = 10
    data = get_code_bytes(code)
    id_trainer = int(input('¿Qué entrenador eres?:'))
    data += get_code_bytes(id_trainer)
    sock.send(data)
    trainer = trainers[id_trainer]
    print("¡Bienvenido",trainer['name'],"!")
    
def capturar_pokemon(sock):
    response = sock.recv(2)
    if response[0] != SERVER_CAPTURE: #code 20
        return None
    pokemon = get_pokemon(response[1])
    quiere_pokemon = str(input("¿Quieres capturar a " + pokemon.get('name', '') + "? "))
    capturar_pokemon = quiere_pokemon == "si"
    if not capturar_pokemon:
        data = get_code_bytes(BOTH_NO)
        print("¡Nos vemos entrenador!")
        sock.send(data)
        return None
    data = get_code_bytes(BOTH_YES)
    data += get_code_bytes(1)
    sock.send(data)
    response = sock.recv(3)
    while response[0] == SERVER_CAPTURE_AGAIN:
        print("No pudiste capturar a" , pokemon.get('name', ''), ".")
        print("Te queda(n)", (numAttemps+1) - response[1], "intento(s).\n")
        quiere_pokemon = str(input("¿Quieres intentar capturar a " + pokemon.get('name', '') + " de nuevo?"))
        capturar_pokemon_ = quiere_pokemon == 'si' #30
        if not capturar_pokemon:
            data = get_code_bytes(BOTH_NO)
            print("¡Nos vemos entrenador!")
            sock.send(data)
            return None
        data = get_code_bytes(BOTH_YES)
        data += get_code_bytes(response[1])
        sock.send(data)
        response = sock.recv(3)
    if response[0] == SERVER_SEND_POKEMON:
        print(pokemon.get('name', ''), "capturado!")
    elif response[0] == SERVER_RUN_OUT_ATTEMPTS:
        print("Se acabaron los Intentos :(")
        print("¡Nos vemos entrenador!")
    else:
        print("Sucedió un error :(")
    sock.close()
    return None



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(input("Server hostname o ip? "))
port = int(input("Server port? "))
sock.connect((host, port))
connect_to_server(sock)
capturar_pokemon(sock)
sock.close()
