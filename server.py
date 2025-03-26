# server

from db_handler import DB_handler

import jsonpickle
import socket

IP = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)

conn, addr = server.accept()

while True:
    try:
        binary_data = conn.recv(1024)
        data = jsonpickle.decode(binary_data)

        match data['act']:
            case 'log_in':
                username = data['username']
                password = data['enc_password']

                if DB_handler.find_user(username, password):
                    conn.send(b'ok')
                else:
                    conn.send(b'wrong_password')

            case 'sign_up':
                username = data['username']

                if username in DB_handler.usernames_iter():
                    conn.send(b'name_error')
                    continue

                password = data['enc_password']
                aes_key  = data['aes_key']
                nonce    = data['nonce']

                DB_handler.add_user(username, password, aes_key, nonce)
                conn.send(b'ok')

            case _:
                conn.close()
                server.close()
                raise 'server.py: match act default case'

    except:
        print(' - client forcefully closed connection - ')
        break

print('\n\n')
print('all connections were closed')
print('server was closed')
print('\n\n')

conn.close()
server.close()