import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Параметры подключения к базе данных
hostname = os.getenv('hostname')  # адрес сервера
database = os.getenv('database')  # название базы данных
username = os.getenv('username')  # имя пользователя
password = os.getenv('password')  # пароль
port = 5432  # порт

try:
    # Подключение к базе данных
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=password,
        port=port
    )
    conn.autocommit = True

    # Создание объекта cursor для выполнения SQL команд
    cursor = conn.cursor()

    # SQL для создания таблицы
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS sample_data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        creation_date TIMESTAMP,
        amount DECIMAL(10,2),
        count INTEGER
    );
    '''

    # Выполнение запроса на создание таблицы
    cursor.execute(create_table_query)
    print("Таблица успешно создана.")

    # SQL для вставки данных
    insert_data_query = '''
    INSERT INTO sample_data (name, creation_date, amount, count) VALUES
    ('Item A', '2023-09-01 14:30:00', 150.00, 10),
    ('Item B', '2023-09-02 10:00:00', 99.99, 5),
    ('Item C', '2023-09-03 15:45:00', 300.20, 20),
    ('Item D', '2023-09-04 09:20:00', 120.75, 15),
    ('Item E', '2023-09-05 12:10:00', 180.00, 7);
    '''

    # Выполнение запроса на вставку данных
    cursor.execute(insert_data_query)
    print("Данные успешно вставлены в таблицу.")

    # SQL запрос для получения данных
    query = 'SELECT * FROM sample_data;'

    # Выполнение запроса
    cursor.execute(query)

    # Получение результатов запроса
    rows = cursor.fetchall()

    # Получение названий столбцов
    column_names = [desc[0] for desc in cursor.description]

    # Создание списка словарей, где каждый словарь представляет одну строку
    data = [dict(zip(column_names, row)) for row in rows]

    # Сериализация данных в JSON
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, default=str, indent=4)  # использование default=str для сериализации дат и других объектов

    print("Данные успешно сохранены в файл 'data.json'.")

except Exception as e:
    print(f"Что-то пошло не так: {e}")

finally:
    # Закрытие курсора и соединения
    cursor.close()
    conn.close()

