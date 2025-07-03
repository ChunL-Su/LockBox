from cryptography.fernet import Fernet


class EncryptedMessage:
    def __init__(self, secret_key):
        self.cipher = Fernet(secret_key)

    def encrypt(self, text):
        encrypted_data = self.cipher.encrypt(bytes(text, encoding='utf-8'))
        return encrypted_data.decode('utf-8')


    def decrypt(self, encrypted_text):
        decrypted_data = self.cipher.decrypt(encrypted_text)
        return decrypted_data.decode('utf-8')


    @staticmethod
    def generate_secret_key()->str:
        return Fernet.generate_key().decode(encoding='utf-8')


if __name__ == '__main__':
    key = EncryptedMessage.generate_secret_key()
    e = EncryptedMessage(key)
    file_path = 'd:/test.txt'
    s = e.encrypt('asd1234')
    print('s: '+s)
    a = e.decrypt(s)
    print(a)
