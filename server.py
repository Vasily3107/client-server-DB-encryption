# server
print('server-side:\n')

from db_handler      import DB_handler
from binary_io_loops import looprecv

from jsonpickle      import decode as jsonpickle_decode
from socket          import socket, AF_INET, SOCK_STREAM

IP = "127.0.0.1"
PORT = 12345

server = socket(AF_INET, SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)

conn, addr = server.accept()

while True:
  try:
    binary_data: bytes                  = looprecv(conn)
    data       : dict[str, str | bytes] = jsonpickle_decode(binary_data)

    act: str = data['act']
    match act:
    
        case 'log_in':
            username    : str   = data['username']
            enc_password: bytes = data['enc_password']
    
            if DB_handler.find_user(username, enc_password):
                conn.send(b'ok')
                DB_handler._update_user_last_online(username)
            else:
                conn.send(b'wrong_password')
    
    
        case 'sign_up':
            username: str = data['username']
    
            if username in DB_handler.usernames_iter():
                conn.send(b'name_error')
                continue
    
            enc_password: bytes = data['enc_password']
            aes_key     : bytes = data['aes_key']
            nonce       : bytes = data['nonce']
    
            DB_handler.add_user(username, enc_password, aes_key, nonce)
            conn.send(b'ok')
            DB_handler._update_user_last_online(username)
    
    
        case _:
            conn.close()
            server.close()
            print(f'{act=}')
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