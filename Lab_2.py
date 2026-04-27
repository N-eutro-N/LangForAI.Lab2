
def run_task_1():
    print("\nЗадача 1 (Права администратора)")

def run_task_2():
    print("\nЗадача 2 (Кэширование)")

def run_task_3():
    print("\nЗадача 3 (safe_write)")

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
