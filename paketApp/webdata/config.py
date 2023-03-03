

class Config():
    def __init__(self):
        self.DB_PLATFORM = 'postgresql'
        self.DB_SERVER = 'localhost'
        self.DB_NAME = 'paket'
        self.DB_USERNAME = ''
        self.DB_PASSWORD = ''
        self.DB_PORT = '5432'
        #Generate a randoms secret key utf-8
        self.SECRET_KEY = 'secret_key'

        self.DB_URL = f'{self.DB_PLATFORM}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'
        