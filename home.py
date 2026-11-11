import database

def catalog_menu(user=None):
    while True:
        print("\n" + "="*50)
        print(" КАТАЛОГ ТОВАРОВ И РАСШИРЕННЫЙ ПОИСК ")
        print("="*50)
        print("1. Посмотреть все категории и товары")
        print("2. 🔍 Расширенный поиск и фильтрация товаров")
        print("0. Назад в главное меню")
        
        choice = input(">> ").strip()
        
        if choice == "1":
            database.view_categories()
            try:
                cat_id = int(input("\nВведите ID категории (0 для отмены): ").strip())
                if cat_id == 0:
                    continue
                products = database.get_products_by_category(cat_id)
                display_products(products, user)
            except ValueError:
                print("✗ Некорректный ввод.")
                
        elif choice == "2":
            advanced_filter_menu(user)
        elif choice == "0":
            break

def advanced_filter_menu(user):
    print("\n--- Фильтрация и поиск ---")
    database.view_categories()
    
    cat_input = input("\nID категории (оставьте пустым для всех): ").strip()
    cat_id = int(cat_input) if cat_input.isdigit() else None
    
    search_query = input("Ключевое слово для поиска в названии/описании (Enter если нет): ").strip()
    search_query = search_query if search_query else None
    
    min_p_input = input("Минимальная цена (Enter если нет): ").strip()
    min_price = float(min_p_input) if min_p_input else None
    
    max_p_input = input("Максимальная цена (Enter если нет): ").strip()
    max_price = float(max_p_input) if max_p_input else None
    
    print("\nСортировка:")
    print("1. Сначала дешевые")
    print("2. Сначала дорогие")
    print("3. По алфавиту")
    print("0. Без сортировки")
    sort_choice = input(">> ").strip()
    
    sort_by = None
    if sort_choice == "1":
        sort_by = "price_asc"
    elif sort_choice == "2":
        sort_by = "price_desc"
    elif sort_choice == "3":
        sort_by = "name"
        
    products = database.filter_products(category_id=cat_id, min_price=min_price, max_price=max_price, search_query=search_query, sort_by=sort_by)
    display_products(products, user)

def display_products(products, user):
    print("\n" + "="*70)
    print(f"{'ID':<4} | {'Название':<25} | {'Цена (руб.)':<12} | {'Склад':<6} | {'Категория':<15}")
    print("="*70)
    if not products:
        print("Товары по вашему запросу не найдены.")
    else:
        for p in products:
            # p can be (id, name, desc, price, stock, cat_name)
            print(f"{p[0]:<4} | {p[1]:<25} | {p[3]:<12.2f} | {p[4]:<6} | {p[5] if len(p) > 5 and p[5] else 'N/A':<15}")
            if p[2]:
                print(f"       ↪ Описание: {p[2]}")
    print("="*70)

    if products and user:
        ans = input("\nХотите добавить товар в корзину? (y/n): ").strip().lower()
        if ans == 'y':
            try:
                p_id = int(input("Введите ID товара: ").strip())
                qty = int(input("Введите количество: ").strip())
                database.add_to_cart(user['id'], p_id, qty)
            except ValueError:
                print("✗ Некорректный ввод.")

def cart_menu(user):
    while True:
        items = database.get_cart_items(user['id'])
        print("\n" + "="*50)
        print("ВАША КОРЗИНА")
        print("="*50)
        if not items:
            print("Корзина пуста.")
            input("\nНажмите Enter для выхода в меню...")
            break

        total = 0
        for cart_id, prod_id, name, price, qty, subtotal in items:
            total += subtotal
            print(f"Позиция ID: {cart_id} | {name} | {qty} шт. x {price:.2f} руб. = {subtotal:.2f} руб.")

        print("-" * 50)
        print(f"Итого к оплате: {total:.2f} руб.")

        print("\n1. Оформить заказ")
        print("2. Удалить товар из корзины")
        print("0. Назад")
        choice = input(">> ").strip()

        if choice == "1":
            if database.create_order(user['id']):
                input("\nНажмите Enter...")
                break
        elif choice == "2":
            try:
                c_id = int(input("Введите ID позиции из корзины: ").strip())
                database.remove_from_cart(user['id'], c_id)
            except ValueError:
                print("✗ Некорректный ID.")
        elif choice == "0":
            break

def user_orders_menu(user):
    orders = database.get_user_orders(user['id'])
    print("\n" + "="*50)
    print("МОИ ЗАКАЗЫ")
    print("="*50)
    if not orders:
        print("У вас пока нет оформленных заказов.")
    else:
        for order_info, items in orders:
            o_id, date, total, status = order_info
            print(f"\nЗаказ #{o_id} от {date} | Статус: {status} | Итого: {total:.2f} руб.")
            for name, qty, price in items:
                print(f"   - {name} x{qty} ({price:.2f} руб./шт)")
    input("\nНажмите Enter для продолжения...")

def user_home_page(user):
    while True:
        role_str = "👨‍💼 АДМИНИСТРАТОР" if user['is_admin'] else "👤 Пользователь"
        print(f"\n=== ГЛАВНОЕ МЕНЮ | {user['username']} ({role_str}) ===")
        print("1. Каталог товаров и фильтрация")
        print("2. Корзина")
        print("3. Мои заказы")
        if user['is_admin']:
            print("4. Панель Администратора")
        print("0. Выйти из аккаунта")

        choice = input(">> ").strip()
        if choice == "1":
            catalog_menu(user)
        elif choice == "2":
            cart_menu(user)
        elif choice == "3":
            user_orders_menu(user)
        elif choice == "4" and user['is_admin']:
            import admin
            admin.admin_panel(user)
        elif choice == "0":
            print("Вы успешно вышли из аккаунта.")
            break

def guest_home_page():
    while True:
        print("\n=== РЕЖИМ ГОСТЯ ===")
        print("1. Просмотр каталога и поиск")
        print("0. Назад к авторизации")

        choice = input(">> ").strip()
        if choice == "1":
            catalog_menu(None)
        elif choice == "0":
            break
