import database
import home
import sys

database.init_db()

ORANGE = "\033[38;5;214m"
RESET = "\033[0m"
    
def main():
    while True:
        print(f"""{ORANGE}
=======================================
   ДОБРО ПОЖАЛОВАТЬ В ИНТЕРНЕТ-МАГАЗИН   
======================================={RESET}
выберите действие:
1. Регистрация
2. Войти
3. Войти как гость
0. Выход
""")

        choice = input(">> ").strip()

        if choice == "1":
            print("\n--- Регистрация ---")
            username = input("введите юзернейм: ").strip()
            email = input("введите почту: ").strip()
            password = input("введите пароль: ").strip()
            phone = input("Введите номер телефона: ").strip()
            address = input("Введите домашний адрес: ").strip()
            
            if username and email and password:
                database.add_user(username, email, password, phone, address)
            else:
                print("✗ Имя, email и пароль обязательны!")

        elif choice == "2":
            print("\n--- Авторизация ---")
            username = input("введите юзернейм или почту: ").strip()
            password = input("введите пароль: ").strip()
            
            success, user = database.check_user(username, password)
            if success:
                role_str = "👨‍💼 АДМИНИСТРАТОР" if user['is_admin'] else "👤 Пользователь"
                print(f"✓ Добро пожаловать, {user['username']}! ({role_str})")
                home.user_home_page(user)
            else:
                print("✗ Неверный логин/email или пароль!")

        elif choice == "3":
            home.guest_home_page()

        elif choice == "0":
            print(f"{ORANGE}Спасибо за визит!")
            sys.exit()
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
