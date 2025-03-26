import pyodbc

class DB_handler:
    server   = 'localhost\SQLEXPRESS'
    database = 'test_db'
    dsn      =f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    @classmethod
    def set_server(cls, server_name: str):
        cls.server = server_name

    @classmethod
    def set_database(cls, db_name: str):
        cls.database = db_name


    from typing import Generator
    @classmethod
    def usernames_iter(cls) -> Generator[str, None, None]:
        conn = pyodbc.connect(cls.dsn)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT username FROM users')
            for row in cursor:
                yield row[0]

        except StopIteration:
            cursor.close()
            conn.close()


    @classmethod
    def get_decryption_data(cls, username: str) -> tuple[bytes] | None:
        '''
        returns tuple(AES_key, nonce)
        '''
        conn = pyodbc.connect(cls.dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM decryption_data WHERE username = ?', (username,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return tuple(row[1:])


    @classmethod
    def find_user(cls, username: str, password: bytes) -> bool:
        conn = pyodbc.connect(cls.dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ? AND [password] = ?', (username, password))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return True if row else False


    @classmethod
    def add_user(cls, username: str, password: bytes, aes_key: bytes, nonce: bytes) -> None:
        conn = pyodbc.connect(cls.dsn)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (username, [password]) values (?, ?)', (username, password))
        conn.commit()

        cursor.execute('INSERT INTO decryption_data (username, aes_key, nonce) values (?, ?, ?)', (username, aes_key, nonce))
        conn.commit()

        cursor.close()
        conn.close()


    @classmethod
    def get_password(cls, username: str) -> bytes:
        '''
        use for debuggin
        '''
        conn = pyodbc.connect(cls.dsn)
        cursor = conn.cursor()

        cursor.execute('SELECT [password] FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row[0]