import psycopg2
from config import load_config

def collecting_info_by_pattern(pattern):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Использование оператора LIKE для поиска подстроки
                cur.execute("SELECT user_id, name, phone_number FROM phonebook WHERE name LIKE %s OR phone_number LIKE %s ORDER BY user_id", 
                            ('%' + pattern + '%', '%' + pattern + '%'))
                rows = cur.fetchall()
                print("Количество найденных записей: ", cur.rowcount)
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_or_update_user(name, phone_number):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM phonebook WHERE name = %s", (name,))
                count = cur.fetchone()[0]

                if count > 0:
                    cur.execute("UPDATE phonebook SET phone_number = %s WHERE name = %s", (phone_number, name))
                else:
                    cur.execute("INSERT INTO phonebook (name, phone_number) VALUES (%s, %s)", (name, phone_number))

                conn.commit()
                print(f"Контакт {name} успешно добавлен или обновлен.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_multiple_users(data_list):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for item in data_list:
                    name = item[0]
                    phone_number = item[1]

                    # Проверка корректности номера телефона
                    if not phone_number.isdigit() or len(phone_number) != 10:
                        print(f"Некорректный номер телефона: {phone_number} для контакта {name}")
                        continue
                    
                    # Проверка, существует ли контакт с таким именем
                    cur.execute("SELECT COUNT(*) FROM phonebook WHERE name = %s", (name,))
                    count = cur.fetchone()[0]

                    if count > 0:
                        # Если контакт существует, обновляем его номер телефона
                        cur.execute("UPDATE phonebook SET phone_number = %s WHERE name = %s", (phone_number, name))
                    else:
                        # Если контакт не существует, вставляем новый контакт
                        cur.execute("INSERT INTO phonebook (name, phone_number) VALUES (%s, %s)", (name, phone_number))

                conn.commit()
                print("Контакты успешно добавлены или обновлены.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Функция для получения данных с пагинацией (limit и offset)
def collecting_info_with_pagination(limit, offset):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, name, phone_number FROM phonebook ORDER BY user_id LIMIT %s OFFSET %s", (limit, offset))
                rows = cur.fetchall()
                print("Количество найденных записей: ", cur.rowcount)
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Функция для удаления данных по имени
def delete_user_by_name(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
                conn.commit()
                print(f"Контакт с именем {name} успешно удален.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Функция для удаления данных по номеру телефона
def delete_user_by_phone(phone_number):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone_number,))
                conn.commit()
                print(f"Контакт с номером {phone_number} успешно удален.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    operation = input("Выберите операцию:\n1 - Записать контакт\n2 - Обновить контакт\n3 - Пройтись по всем контактам\n4 - Удалить контакт\n5 - Записать несколько контактов : ")

    if operation == "1":
        name = input("Введите имя нового контакта: ")
        phone_number = input("Введите номер телефона нового контакта: ")
        insert_or_update_user(name, phone_number)

    elif operation == "2":
        name = input("Введите имя контакта для обновления: ")
        phone_number = input("Введите новый номер телефона: ")
        insert_or_update_user(name, phone_number)

    elif operation == "3":
        pattern = input("Введите паттерн (часть имени, фамилии или номера телефона): ")
        collecting_info_by_pattern(pattern)

    elif operation == "4":
        delete_type = input("Удалить по:\n1 - Имени\n2 - Номеру телефона\nВыберите тип: ")
        if delete_type == "1":
            name = input("Введите имя контакта для удаления: ")
            delete_user_by_name(name)
        elif delete_type == "2":
            phone_number = input("Введите номер телефона для удаления: ")
            delete_user_by_phone(phone_number)

    elif operation == "5":
        num_contacts = int(input("Введите количество контактов для вставки: "))
        data_list = []
        for _ in range(num_contacts):
            name = input("Введите имя: ")
            phone_number = input("Введите номер телефона: ")
            data_list.append([name, phone_number])
        insert_multiple_users(data_list)