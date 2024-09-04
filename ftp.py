from ftplib import FTP
from dotenv import load_dotenv
import os

load_dotenv()

# Параметры FTP сервера
ftp_host = os.getenv('ftp_host_address')
ftp_username = os.getenv('ftp_username')
ftp_password = os.getenv('ftp_password')

# Создание соединения с FTP сервером
ftp = FTP(ftp_host)
ftp.login(user=ftp_username, passwd=ftp_password)

# Открытие файла в бинарном режиме и его загрузка на FTP
with open('data.json', 'rb') as file:
    ftp.storbinary('STOR data.json', file)

ftp.quit()
print("Файл 'data.json' успешно загружен на FTP сервер.")
