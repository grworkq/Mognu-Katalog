import database

def admin_panel(user):
    while True:
        print(f"\n=== ПАНЕЛЬ АДМИНИСТРАТОРА ({user['username']}) ===")
        print("1. Управление категориями")
        print("2. Добавить новый товар")
        print("3. Просмотреть и редактировать товары")
        print("4. Удалить товар")
        print("5. Просмотреть все заказы клиентов")
        print("6. Изменить статус заказа")
        print("--------------------------------------------------")
        print("7. 📊 АНАЛИТИКА")
        print("0. Назад в главное меню")

        choice = input(">> ").strip()
        if choice == "1":
            categories_management()
        elif choice == "2":
            admin_add_product()
        elif choice == "3":
            admin_view_edit_products()
        elif choice == "4":
            admin_delete_product()
        elif choice == "5":
            admin_view_all_orders()
        elif choice == "6":
            admin_change_order_status()
        elif choice == "7":
            complex_sql_reports_menu()
        elif choice == "0":
            break

def complex_sql_reports_menu():
    while True:
        print("\n" + "="*60)
        print(" 📊 НАЛИТИКА БАЗЫ ДАННЫХ ")
        print("="*60)
        print("1. Отчет по продажам и выручке по категориям")
        print("2. ТОП-5 самых активных покупателей")
        print("3. Список неликвидных товаров — без заказов")
        print("4. Рейтинг товаров по отзывам")
        print("0. Назад в админ-панель")

        choice = input(">> ").strip()

        if choice == "1":
            print("\n--- 1. Отчет по продажам по категориям ---")
            rows = database.get_sales_report_by_category()
            print(f"{'Категория':<25} | {'Товаров':<8} | {'Продано':<8} | {'Выручка (руб.)':<15}")
            print("-" * 65)
            for r in rows:
                print(f"{r[0]:<25} | {r[1]:<8} | {r[2]:<8} | {r[3]:<15.2f}")
            input("\nНажмите Enter для продолжения...")

        elif choice == "2":
            print("\n--- 2. ТОП-5 активных покупателей ---")
            rows = database.get_top_customers()
            print(f"{'Пользователь':<20} | {'Email':<20} | {'Заказов':<8} | {'Потрачено (руб.)':<15}")
            print("-" * 70)
            for r in rows:
                print(f"{r[0]:<20} | {r[1]:<20} | {r[2]:<8} | {r[3]:<15.2f}")
            input("\nНажмите Enter для продолжения...")

        elif choice == "3":
            print("\n--- 3. Неликвидные товары (Ни разу не купленные) ---")
            rows = database.get_unsold_products()
            print(f"{'ID':<4} | {'Название':<30} | {'Цена':<10} | {'Склад':<6}")
            print("-" * 55)
            if not rows:
                print("Все товары хотя бы раз покупались!")
            else:
                for r in rows:
                    print(f"{r[0]:<4} | {r[1]:<30} | {r[2]:<10.2f} | {r[3]:<6}")
            input("\nНажмите Enter для продолжения...")

        elif choice == "4":
            print("\n--- 4. Рейтинг товаров по отзывам ---")
            rows = database.get_products_with_ratings()
            print(f"{'ID':<4} | {'Название':<25} | {'Цена':<10} | {'Рейтинг':<8} | {'Отзывов':<8}")
            print("-" * 65)
            for r in rows:
                print(f"{r[0]:<4} | {r[1]:<25} | {r[3]:<10.2f} | {r[4]:<8.2f} | {r[5]:<8}")
            input("\nНажмите Enter для продолжения...")

        elif choice == "0":
            break

def categories_management():
    while True:
        print("\n--- Управление Категориями ---")
        print("1. Просмотреть категории")
        print("2. Добавить категорию")
        print("3. Удалить категорию")
        print("0. Назад")

        c = input(">> ").strip()
        if c == "1":
            database.view_categories()
        elif c == "2":
            database.add_category()
        elif c == "3":
            database.delete_category()
        elif c == "0":
            break

def admin_add_product():
    print("\n--- Добавление нового товара ---")
    database.view_categories()
    try:
        cat_id = int(input("Введите ID категории: ").strip())
        name = input("Название товара: ").strip()
        desc = input("Описание товара: ").strip()
        price = float(input("Цена товара (руб): ").strip())
        stock = int(input("Количество на складе: ").strip())

        if database.add_product(name, desc, price, stock, cat_id):
            print(f"✓ Товар '{name}' успешно добавлен!")
    except ValueError:
        print("✗ Ошибка: некорректный числовой ввод.")

def admin_view_edit_products():
    print("\n--- Список всех товаров ---")
    products = database.get_all_products()
    if not products:
        print("Товаров нет.")
        return

    for p in products:
        print(f"ID: {p[0]} | {p[1]} | Цена: {p[3]} руб. | Склад: {p[4]} шт. | Категория: {p[5]}")

    edit_choice = input("\nХотите отредактировать товар? (y/n): ").strip().lower()
    if edit_choice == 'y':
        try:
            p_id = int(input("Введите ID товара для редактирования: ").strip())
            prod = database.get_product_details(p_id)
            if not prod:
                print("✗ Товар не найден.")
                return

            print(f"Редактирование: {prod[1]}")
            name = input(f"Новое название [{prod[1]}]: ").strip() or prod[1]
            desc = input(f"Новое описание [{prod[2]}]: ").strip() or prod[2]
            price_str = input(f"Новая цена [{prod[3]}]: ").strip()
            price = float(price_str) if price_str else prod[3]
            stock_str = input(f"Новое количество на складе [{prod[4]}]: ").strip()
            stock = int(stock_str) if stock_str else prod[4]
            
            database.view_categories()
            cat_str = input("Новый ID категории (Enter чтобы оставить текущую): ").strip()
            cat_id = int(cat_str) if cat_str else prod[0]

            if database.update_product(p_id, name, desc, price, stock, cat_id):
                print("✓ Товар обновлен!")
        except ValueError:
            print("✗ Некорректные данные.")

def admin_delete_product():
    products = database.get_all_products()
    for p in products:
        print(f"ID: {p[0]} | {p[1]}")
    try:
        p_id = int(input("Введите ID товара для удаления: ").strip())
        if database.delete_product(p_id):
            print("✓ Товар удален.")
    except ValueError:
        print("✗ Некорректный ID.")

def admin_view_all_orders():
    orders = database.get_all_orders()
    print("\n" + "="*50)
    print("ВСЕ ЗАКАЗЫ КЛИЕНТОВ")
    print("="*50)
    if not orders:
        print("Заказов нет.")
    else:
        for order_info, items in orders:
            o_id, uname, date, total, status = order_info
            print(f"\nЗаказ #{o_id} | Клиент: {uname} | Дата: {date} | Статус: {status} | Итого: {total:.2f} руб.")
            for name, qty, price in items:
                print(f"   - {name} x{qty} ({price:.2f} руб./шт)")
    input("\nНажмите Enter для продолжения...")

def admin_change_order_status():
    admin_view_all_orders()
    try:
        o_id = int(input("Введите ID заказа для изменения статуса: ").strip())
        print("Варианты статусов: Обработка, Отправлен, Доставлен, Отменен")
        new_status = input("Введите новый статус: ").strip()
        if new_status:
            database.update_order_status(o_id, new_status)
    except ValueError:
        print("✗ Некорректный ID.")
