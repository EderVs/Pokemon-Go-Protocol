"""
    Pokemon Go Protocol Server
"""

import os
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
ERROR_CONNECTION_CLOSED = 42
numAttemps = 3


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
            client.settimeout(5)
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

    
    def image_size_to_bytes(self, size):
        b_array = []
        while size >= 256:
            b_array.append(size % 256)
            size = size // 256
        b_array.append(size)
        b_array.reverse()
        b = b''
        for i in range(4-len(b_array)):
            b += b'\x00'
        b += bytes(b_array)
        return b
        

    def data_to_send_pokemon(self, pokemon):
        path = "pokemons/" + pokemon["name"] + ".jpg"
        data = get_code_bytes(SERVER_SEND_POKEMON)
        data += get_code_bytes(pokemon['id'])
        size = os.path.getsize(path)
        f = open(path, "rb") 
        data += self.image_size_to_bytes(size)
        data += f.read()
        f.close()
        return data


    def capture_pokemon(self, client, address):
        pokemon_to_capture = pokemons[randint(1, len((pokemons.keys())))]
        print("Pokemón que se quiere capturar:", pokemon_to_capture.get('name', "NONE"))
        data = get_code_bytes(SERVER_CAPTURE)
        data += get_code_bytes(pokemon_to_capture.get('id', -1))
        client.send(data)
        response = client.recv(2)
        actual_num_attemps = numAttemps
        while response[0] == BOTH_YES and actual_num_attemps > 0 :
            # Get in a random way if the pokemon is captured
            catch_pokemon = randint(0,100)
            if True or catch_pokemon < 30: 
                # Gets the data to send when the client captures a pokemon
                data = self.data_to_send_pokemon(pokemon_to_capture)
                client.send(data)
                return pokemon_to_capture
            actual_num_attemps -= 1
            # We check if we are running out of attemps to capture
            if actual_num_attemps <= 0:
                break
            data = get_code_bytes(SERVER_CAPTURE_AGAIN)
            data += get_code_bytes(pokemon_to_capture.get('id', -1))
            data += get_code_bytes(actual_num_attemps)
            client.send(data)  #21
            response = client.recv(2)
        if response[0] == BOTH_YES:
            print("Se acabaron los intentos.")
            client.send(get_code_bytes(SERVER_RUN_OUT_ATTEMPTS))
            return {}
        if response[0] == BOTH_NO:
            print("No quiso el pokemón. Cierre de conexión.")
            return {}
        else:
            print("No se recibió respuesta válida.")
            return {}

    def listenToClient(self, client, address):
        size = 1024
        try:
            trainer = self.connect_trainer(client, address)
            print(trainer)
            if trainer == {}:
                client.close()
                return False
            pokemon = self.capture_pokemon(client, address)
            if pokemon != {}:
                print("!Se capturó!: ", pokemon)
                trainer['pokemons'].append(pokemon)
                print("Pokemones de",trainer['name'],": ",trainer['pokemons'])
            client.close()
            print("Se ha cerrado la conexión con el cliente.")
            return True
        except socket.timeout:
            print("Se acabó el tiempo")
            data = get_code_bytes(ERROR_CONNECTION_CLOSED)
            client.send(data)
            client.close()
            return False


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    ThreadServer('', port_num).listen()
