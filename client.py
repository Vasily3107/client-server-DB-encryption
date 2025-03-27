# client
print('client-side:\n')

from tkinter         import Tk, Label, Button, Entry
from tkinter.ttk     import Notebook, Frame

from Crypto.Cipher   import AES
from Crypto.Random   import get_random_bytes

from db_handler      import DB_handler
from binary_io_loops import loopsend

from jsonpickle      import encode as jsonpickle_encode
from socket          import socket, AF_INET, SOCK_STREAM

IP = "127.0.0.1"
PORT = 12345

client = socket(AF_INET, SOCK_STREAM)
client.connect((IP, PORT))

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

root = Tk()
tab_switch = Notebook(root)



# - - - LOG IN - - - - - - - - - - - - - - - - - - - - - - - - - - -
log_in_frame = Frame(tab_switch)

log_in_info_label = Label(log_in_frame, text='', wraplength=WINDOW_WIDTH)
log_in_info_label.grid(row=3, column=0, columnspan=2)

Label(log_in_frame, text='Username:').grid(row=0, column=0)
log_in_username_entry = Entry(log_in_frame)
log_in_username_entry.grid(row=0, column=1)

Label(log_in_frame, text='Password:').grid(row=1, column=0)
log_in_password_entry = Entry(log_in_frame)
log_in_password_entry.grid(row=1, column=1)

def log_in():
    def clear_error():
        log_in_info_label.config(fg='black', text='')
    def show_error(message):
        log_in_info_label.config(fg='red', text=f'Error: {message}')

    clear_error()

    username = log_in_username_entry.get()
    password = log_in_password_entry.get()

    if username == '':
        show_error("Username can't be empty")
        return
    if password == '':
        show_error("Password can't be empty")
        return

    try: key, nonce = DB_handler.get_decryption_data(username)
    except:
        show_error(f'username "{username}" wasn\'t found')
        return

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    encrypted_password = cipher.encrypt_and_digest(password.encode())[0]

    binary_data = jsonpickle_encode({
                 'act': 'log_in',
            'username': username,
        'enc_password': encrypted_password,
    }).encode()

    loopsend(client, binary_data)

    res_msg = client.recv(1024).decode()
    match res_msg:
        case 'wrong_password':
            show_error(f'wrong password')

        case 'unexpected_error':
            show_error(f'something went wrong. Please check your input or try again later')

        case 'ok':
            log_in_info_label.config(fg='green', text='Log in successful')

        case _:
            print(f'{res_msg=}')
            raise 'server respose message matched default case'

Button(log_in_frame, text='Log in', command=log_in).grid(row=2, column=0, columnspan=2)



# - - - SIGN UP - - - - - - - - - - - - - - - - - - - - - - - - - - -
sign_up_frame = Frame(tab_switch)

sign_up_info_label = Label(sign_up_frame, text='', wraplength=WINDOW_WIDTH)
sign_up_info_label.grid(row=3, column=0, columnspan=2)

Label(sign_up_frame, text='Username:').grid(row=0, column=0)
sign_up_username_entry = Entry(sign_up_frame)
sign_up_username_entry.grid(row=0, column=1)

Label(sign_up_frame, text='Password:').grid(row=1, column=0)
sign_up_password_entry = Entry(sign_up_frame)
sign_up_password_entry.grid(row=1, column=1)

def sign_up():
    def clear_error():
        sign_up_info_label.config(fg='black', text='')
    def show_error(message):
        sign_up_info_label.config(fg='red', text=f'Error: {message}')

    clear_error()

    username = sign_up_username_entry.get()
    password = sign_up_password_entry.get()

    if username == '':
        show_error("Username can't be empty")
        return
    if password == '':
        show_error("Password can't be empty")
        return

    rand_key = get_random_bytes(16)
    cipher = AES.new(rand_key, AES.MODE_EAX)
    encrypted_password = cipher.encrypt_and_digest(password.encode())[0]
    nonce = cipher.nonce

    binary_data = jsonpickle_encode({
                 'act': 'sign_up',
            'username': username,
        'enc_password': encrypted_password,
             'aes_key': rand_key,
               'nonce': nonce
    }).encode()
    
    loopsend(client, binary_data)

    res_msg = client.recv(1024).decode()
    match res_msg:
        case 'name_error':
            show_error(f'username "{username}" is already taken')

        case 'unexpected_error':
            show_error(f'something went wrong. Please check your input or try again later')

        case 'ok':
            sign_up_info_label.config(fg='green', text='Sign up successful')

        case _:
            print(f'{res_msg=}')
            raise 'server respose message matched default case'

Button(sign_up_frame, text='Sign up', command=sign_up).grid(row=2, column=0, columnspan=2)



# - - - VISUAL & MISCELLANEOUS SETTINGS - - - - - - - - - - - - - - - - - - - - - - - - - - -
root.title('Log in  or  Sign up')
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

def on_window_close():
    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_window_close)

tab_switch.add(log_in_frame, text='Log in')
tab_switch.add(sign_up_frame, text='Sign up')
tab_switch.pack(expand=1, fill='both')

root.mainloop()