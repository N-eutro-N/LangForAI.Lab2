import os

current_user_role = 'guest'

def role_required(*allowed_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if current_user_role in allowed_roles:
                return func(*args, **kwargs)
            else:
                print(f"Доступ запрещен")
                print(f"Разрешенные роли: {allowed_roles}")
        return wrapper
    return decorator

@role_required('admin', 'hr')
def secret_resource():
    return ">>> Доступ разрешен."

def run_task_1():
    print("\nЗадача 1 (Права администратора)")
    global current_user_role

    current_user_role = 'user'
    print(f"Текущая роль: {current_user_role}")
    result = secret_resource()
    if result:
        print(result)

    current_user_role = 'hr'
    print(f"Текущая роль: {current_user_role}")
    result = secret_resource()
    if result:
        print(result)

    current_user_role = 'admin'
    print(f"Текущая роль: {current_user_role}")
    result = secret_resource()
    if result:
        print(result)

def custom_sorted(iterable):
    lst = list(iterable)
    n = len(lst)
    for i in range(n):
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def cache(db: str, expiration: int):
    def decorator(func):
        cached_data = {}
        counters = {}
        def wrapper(data_str: str):
            if data_str not in cached_data or counters.get(data_str, 0) == 0:
                result = func(data_str)
                cached_data[data_str] = result
                counters[data_str] = expiration
                print(f"Инфо: '{data_str}' из {db}, теперь кэшируется и истекает через={counters[data_str]}")
            else:
                counters[data_str] -= 1
                print(f"Инфо: '{data_str}' кэшировано в {db}, истекает через={counters[data_str]}")
            return cached_data[data_str]
        return wrapper
    return decorator

@cache(db='postgresql', expiration=5)
def process_list_task(data_str: str):
    print(f"\n[ВЫЧИСЛЕНИЕ ФУНКЦИИ для '{data_str}']")
    try:
        items = [float(x) if '.' in x else int(x) for x in data_str.split()]
    except ValueError:
        return "Ошибка: список должен содержать только числа."

    has_positive = any(x > 0 for x in items)
    is_all_numbers = all(isinstance(x, (int, float)) for x in items)
    sorted_items = custom_sorted(items)

    res_str = (
        f"Исходный список: {items}\n"
        f"Есть положительное (any): {has_positive}\n"
        f"Все числа (all): {is_all_numbers}\n"
        f"Отсортировано (custom_sorted): {sorted_items}"
    )
    return res_str

def run_task_2():
    print("\nЗадача 2 (Кэширование)")
    print(">>> Вызов 1:")
    print(process_list_task("5 -2 10 0"))
    print("\n>>> Вызов 2:")
    print(process_list_task("5 -2 10 0"))
    print("\n>>> Вызов 3:")
    print(process_list_task("5 -2 10 0"))
    print("\n>>> Вызов 4 (новые данные):")
    print(process_list_task("100 50 20 10"))

class safe_write:
    def __init__(self, filename):
        self.filename = filename
        self.saved_content = None
        self.file_obj = None

    def __enter__(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.saved_content = f.read()
        self.file_obj = open(self.filename, 'w', encoding='utf-8')
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
        if exc_type is not None:
            print(f"Во время записи в файл было обнаружено исключение {exc_type.__name__}")
            if self.saved_content is not None:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(self.saved_content)
            else:
                if os.path.exists(self.filename):
                    os.remove(self.filename)
            return True
        return False

def run_task_3():
    print("\nЗадача 3 (Контекстный менеджер safe_write)")
    filename = 'song.txt'

    print("Тест 1: Успешная запись текста")
    with safe_write(filename) as f:
        f.write("Провекра безопасной записи текста\n")
        f.write("Раз, два, три, раз, два, три\n")

    with open(filename, 'r', encoding='utf-8') as f:
        print("Содержимое файла:")
        print(f.read())

    print("Тест 2: Запись с ошибкой (rollback).")
    try:
        with safe_write(filename) as f:
            f.write("ЭТОТ ТЕКСТ НЕ ДОЛЖЕН СОХРАНИТЬСЯ.\n")
            raise ValueError("Сбой системы!")
    except Exception:
        pass

    print("Проверка содержимого после ошибки:")
    with open(filename, 'r', encoding='utf-8') as f:
        print(f.read())

    if os.path.exists(filename):
        os.remove(filename)

def main():
    while True:
        print("\n ЛАБОРАТОРНАЯ РАБОТА 2 (Вариант 8)")
        print("1. Задача 1. Права администратора")
        print("2. Задача 2. Кэширование")
        print("3. Задача 3. Контекстный менеджер safe_write")
        print("0. Выход")
        choice = input("Выберите пункт меню: ")
        if choice == '1':
            run_task_1()
        elif choice == '2':
            run_task_2()
        elif choice == '3':
            run_task_3()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
