import psycopg2
from config import load_config

def collecting_info_by_pattern(pattern):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT user_id, name, phone_number 
                    FROM phonebook 
                    WHERE name ILIKE %s OR phone_number LIKE %s 
                    ORDER BY user_id
                """, ('%' + pattern + '%', '%' + pattern + '%'))
                
                rows = cur.fetchall()
                print(f"\nНайдено записей: {cur.rowcount}")
                for row in rows:
                    print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при поиске: {error}")

def insert_or_update_user(name, phone_number):
    config = load_config()
    try:
        # Валидация номера телефона
        if not (len(phone_number) == 12 and phone_number.startswith('+7') and phone_number[2:].isdigit()):
            print(f"\nОшибка: Некорректный номер '{phone_number}'. Требуется формат: +7XXXXXXXXXX (12 цифр)")
            return

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Проверка существования имени
                cur.execute("SELECT COUNT(*) FROM phonebook WHERE name = %s", (name,))
                count = cur.fetchone()[0]

                if count > 0:
                    cur.execute("UPDATE phonebook SET phone_number = %s WHERE name = %s", 
                               (phone_number, name))
                    print(f"\nОбновлен контакт: {name} -> {phone_number}")
                else:
                    cur.execute("INSERT INTO phonebook (name, phone_number) VALUES (%s, %s)", 
                               (name, phone_number))
                    print(f"\nДобавлен новый контакт: {name} -> {phone_number}")
                
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка базы данных: {error}")

def insert_multiple_users(data_list):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                valid_count = 0
                for name, phone in data_list:
                    # Валидация номера
                    if not (len(phone) == 12 and phone.startswith('+7') and phone[2:].isdigit()):
                        print(f"Пропуск '{name}': неверный формат номера '{phone}'")
                        continue
                    
                    # Проверка существования
                    cur.execute("SELECT COUNT(*) FROM phonebook WHERE name = %s", (name,))
                    count = cur.fetchone()[0]

                    if count > 0:
                        cur.execute("UPDATE phonebook SET phone_number = %s WHERE name = %s", (phone, name))
                    else:
                        cur.execute("INSERT INTO phonebook (name, phone_number) VALUES (%s, %s)", (name, phone))
                    valid_count += 1

                conn.commit()
                print(f"\nУспешно обработано контактов: {valid_count}/{len(data_list)}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при массовом импорте: {error}")

def collecting_info_with_pagination(limit, offset):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT user_id, name, phone_number 
                    FROM phonebook 
                    ORDER BY user_id 
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                
                rows = cur.fetchall()
                print(f"\nСтраница {offset//limit + 1}:")
                for row in rows:
                    print(f"ID: {row[0]}, {row[1]}: {row[2]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка пагинации: {error}")

def delete_user_by_name(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE name = %s RETURNING phone_number", (name,))
                deleted = cur.fetchone()
                conn.commit()
                print(f"\nУдален контакт '{name}'" if deleted else "\nКонтакт не найден")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка удаления: {error}")

def delete_user_by_phone(phone_number):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE phone_number = %s RETURNING name", (phone_number,))
                deleted = cur.fetchone()
                conn.commit()
                print(f"\nУдален номер '{phone_number}'" if deleted else "\nНомер не найден")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка удаления: {error}")

if __name__ == '__main__':
    operations = {
        "1": "Добавить контакт",
        "2": "Обновить контакт",
        "3": "Поиск по шаблону",
        "4": "Удалить контакт",
        "5": "Массовый импорт",
        "6": "Просмотр с пагинацией"
    }

    print("\n" + "-"*40)
    print("Телефонная книга")
    print("-"*40)
    for key, value in operations.items():
        print(f"{key}. {value}")
    
    choice = input("\nВыберите операцию (1-6): ")

    if choice == "1" or choice == "2":
        name = input("Введите имя: ")
        phone = input("Введите телефон (+7XXXXXXXXXX): ")
        insert_or_update_user(name, phone)

    elif choice == "3":
        pattern = input("Введите поисковый запрос: ")
        collecting_info_by_pattern(pattern)

    elif choice == "4":
        delete_type = input("Удалить по:\n1. Имени\n2. Номеру\nВыбор: ")
        if delete_type == "1":
            name = input("Введите имя для удаления: ")
            delete_user_by_name(name)
        elif delete_type == "2":
            phone = input("Введите номер для удаления: ")
            delete_user_by_phone(phone)

    elif choice == "5":
        contacts = []
        try:
            n = int(input("Количество контактов для добавления: "))
            for _ in range(n):
                name = input("Имя: ")
                phone = input("Телефон (+7XXXXXXXXXX): ")
                contacts.append((name, phone))
            insert_multiple_users(contacts)
        except ValueError:
            print("Ошибка: введите число")

    elif choice == "6":
        limit = int(input("Записей на страницу: "))
        page = int(input("Номер страницы: "))
        collecting_info_with_pagination(limit, (page-1)*limit)

    else:
        print("Неверный выбор операции")