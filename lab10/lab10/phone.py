import psycopg2
import csv
from config import load_config  # Файл с параметрами подключения

# ======================== 1. Table Design ========================
def create_table():
    """Создание таблицы phonebook с правильной структурой"""
    conn = None
    try:
        conn = psycopg2.connect(**load_config())
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                user_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                phone VARCHAR(20) UNIQUE NOT NULL
            )
        """)
        conn.commit()
        print("Таблица 'phonebook' создана успешно!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# ================= 2. Data Insertion Methods =====================
def insert_from_console():
    """Ручной ввод данных через консоль"""
    first = input("Имя: ")
    last = input("Фамилия (опционально): ")
    phone = input("Телефон: ")
    
    sql = """INSERT INTO phonebook(first_name, last_name, phone)
             VALUES(%s, %s, %s) RETURNING user_id"""
    
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first, last, phone))
                user_id = cur.fetchone()[0]
                conn.commit()
                print(f"Контакт добавлен. ID: {user_id}")
    except psycopg2.IntegrityError:
        print("Ошибка: номер телефона уже существует!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_from_csv(filename):
    """Импорт данных из CSV файла"""
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur, open(filename, 'r', encoding='cp1251', errors='ignore') as f:
                reader = csv.reader(f)
                next(reader)  # Пропуск заголовка
                
                for row in reader:
                    try:
                        cur.execute("""
                            INSERT INTO phonebook (first_name, last_name, phone)
                            VALUES (%s, %s, %s)
                        """, (row[0], row[1], row[2]))
                    except psycopg2.IntegrityError:
                        print(f"Пропуск дубликата: {row[2]}")
                        conn.rollback()
                        continue
                conn.commit()
        print("Данные из CSV успешно импортированы!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# ====================== 3. Data Update ===========================
def update_contact():
    """Обновление данных контакта"""
    search_term = input("Введите телефон или имя для поиска: ")
    
    # Поиск контакта
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM phonebook 
                WHERE phone = %s 
                   OR first_name ILIKE %s 
                   OR last_name ILIKE %s
            """, (search_term, f'%{search_term}%', f'%{search_term}%'))
            
            results = cur.fetchall()
            if not results:
                print("Контакт не найден!")
                return
                
            # Вывод найденных контактов
            for i, row in enumerate(results):
                print(f"{i+1}. ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}")

            choice = int(input("Выберите номер контакта для изменения: ")) - 1
            selected = results[choice]

    # Выбор поля для изменения
    field = input("Что меняем? (1-Имя, 2-Фамилия, 3-Телефон): ")
    new_value = input("Новое значение: ")

    fields = {
        '1': 'first_name',
        '2': 'last_name',
        '3': 'phone'
    }
    
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE phonebook 
                    SET {fields[field]} = %s 
                    WHERE user_id = %s
                """, (new_value, selected[0]))
                conn.commit()
                print("Контакт обновлен!")
    except psycopg2.IntegrityError:
        print("Ошибка: новый номер телефона уже существует!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# ===================== 4. Data Querying ==========================
def search_contacts():
    """Поиск контактов с фильтрами"""
    search_term = input("Введите имя, фамилию или телефон для поиска: ")
    
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM phonebook 
                    WHERE first_name ILIKE %s 
                       OR last_name ILIKE %s 
                       OR phone LIKE %s
                    ORDER BY first_name
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                
                results = cur.fetchall()
                print(f"Найдено контактов: {len(results)}")
                for row in results:
                    print(f"ID: {row[0]}, {row[1]} {row[2]}, тел.: {row[3]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# ===================== 5. Data Deletion ==========================
def delete_contact():
    """Удаление контакта"""
    identifier = input("Введите ID, телефон или имя для удаления: ")
    
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                # Попытка интерпретировать как ID
                if identifier.isdigit():
                    cur.execute("DELETE FROM phonebook WHERE user_id = %s", (identifier,))
                else:
                    cur.execute("""
                        DELETE FROM phonebook 
                        WHERE phone = %s 
                           OR first_name ILIKE %s 
                           OR last_name ILIKE %s
                    """, (identifier, f'%{identifier}%', f'%{identifier}%'))
                
                deleted = cur.rowcount
                conn.commit()
                print(f"Удалено контактов: {deleted}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# ==================== 6. User Interface ==========================
def main_menu():
    while True:
        print("\n===== PhoneBook Manager =====")
        print("1. Добавить контакт (вручную)")
        print("2. Импорт из CSV")
        print("3. Поиск контактов")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("6. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            filename = input("Введите имя CSV файла: ")
            insert_from_csv(filename)
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Неверный ввод!")

if __name__ == '__main__':
    create_table()  # Создание таблицы при первом запуске
    main_menu()