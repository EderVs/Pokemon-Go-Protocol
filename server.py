"""
    Pokemon Go Protocol Server
"""

import socket
import threading
from random import randint


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


def get_code_bytes(code):
    return bytes([code])


def get_trainer(trainer_id):
    return trainers.get(trainer_id, {})


def get_pokemon(pokemon_id):
    return pokemons.get(pokemon_id, {})


class ThreadServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient, args = (client, address)).start()


    def connect_trainer(self, client, address):
        b_code = client.recv(2)
        print(b_code)
        code = b_code[0]
        if code != CLIENT_CAPTURE:
            client.send(get_code_bytes(ERROR_WRONG_CODE))
            return {}
        trainer_id = b_code[1]
        trainer = get_trainer(trainer_id)
        if trainer == {}: 
            client.send(get_code_bytes(ERROR_WRONG_CODE))
        return trainer


    def capture_pokemon(self, client, address):
        pokemon_to_capture = pokemons[randint(0, len((pokemons.keys())))]
        print(pokemon_to_capture)
        data = get_code_bytes(SERVER_CAPTURE)
        data += get_code_bytes(pokemon_to_capture.get('id', -1))
        client.send(data)
        

    def listenToClient(self, client, address):
        size = 1024
        """try:"""
        trainer = self.connect_trainer(client, address)
        print(trainer)
        if trainer == {}:
            client.close()
            return False
        self.capture_pokemon(client, address)
        client.close()
        """except:
            print("Error")
            client.close()
            return False
        """


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    ThreadServer('', port_num).listen()
