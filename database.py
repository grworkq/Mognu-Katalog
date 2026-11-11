import sqlite3
from datetime import datetime
import auth

DB_PATH = "shop.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TEXT
            )
        """)
        
        c.execute("PRAGMA table_info(users)")
        cols = [col[1] for col in c.fetchall()]
        if 'is_admin' not in cols:
            c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")

        c.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                description TEXT,
                stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
                category_id INTEGER NOT NULL,
                created_at TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                added_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                UNIQUE (user_id, product_id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_date TEXT,
                total_price REAL NOT NULL CHECK (total_price >= 0),
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price_at_purchase REAL NOT NULL CHECK (price_at_purchase >= 0),
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT,
                created_at TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()

def add_user(username, email, password, phone, address):
    hashed_pass = auth.hashing(password)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO users (username, email, password, phone, address, is_admin, created_at)
                VALUES (?, ?, ?, ?, ?, 0, ?)
            """, (username, email, hashed_pass, phone, address, now))
            conn.commit()
            print("✓ Регистрация прошла успешно!")
            return True
        except sqlite3.IntegrityError:
            print("✗ Ошибка: Пользователь с таким именем или email уже существует.")
            return False
        except Exception as e:
            print(f"✗ Ошибка регистрации: {e}")
            return False

def check_user(username_or_email, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT id, username, password, is_admin, email 
            FROM users 
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))
        user = c.fetchone()

    if user and auth.checking(password, user[2]):
        current_user = {
            'id': user[0],
            'username': user[1],
            'is_admin': bool(user[3]),
            'email': user[4]
        }
        return True, current_user
    else:
        return False, None

def view_categories():]
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, description FROM categories')
        rows = c.fetchall()
        print("\n" + "="*50)
        print("КАТЕГОРИИ")
        print("="*50)
        if not rows:
            print("Список категорий пуст.")
        for cat_id, name, desc in rows:
            print(f"{cat_id}. {name} - {desc if desc else 'Нет описания'}")
        return rows

def add_category():
    name = input("Введите название категории: ").strip()
    desc = input("Описание категории: ").strip()

    if not name:
        print("Название категории не может быть пустым.")
        return

    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, desc if desc else None))
            conn.commit()
            print(f"✓ Категория '{name}' добавлена.")
        except Exception as e:
            print(f"✗ Ошибка при добавлении категории: {e}")

def delete_category():
    rows = view_categories()
    if not rows:
        return

    try:
        cat_id = int(input("\nID категории для удаления: ").strip())
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
            conn.commit()
            print(f"✓ Категория ID {cat_id} удалена.")
    except ValueError:
        print("✗ Ошибка: введен некорректный ID.")
    except Exception as e:
        print(f"✗ Ошибка удаления: {e}")

def get_products_by_category(category_id: int):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, description, price, stock FROM products WHERE category_id = ?", (category_id,))
        return c.fetchall()

def get_all_products():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT p.id, p.name, p.description, p.price, p.stock, c.name FROM products p LEFT JOIN categories c ON p.category_id = c.id")
        return c.fetchall()

def get_product_details(product_id: int):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT p.id, p.name, p.description, p.price, p.stock, c.name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.id = ?
        """, (product_id,))
        return c.fetchone()

def filter_products(category_id=None, min_price=None, max_price=None, search_query=None, sort_by=None):
    """
    Сложный гибкий поиск и фильтрация товаров с использованием условий WHERE, LIKE, ORDER BY
    """
    with get_connection() as conn:
        c = conn.cursor()
        
        query = """
            SELECT p.id, p.name, p.description, p.price, p.stock, c.name as cat_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE 1=1
        """
        params = []

        if category_id:
            query += " AND p.category_id = ?"
            params.append(category_id)
        
        if min_price is not None:
            query += " AND p.price >= ?"
            params.append(min_price)

        if max_price is not None:
            query += " AND p.price <= ?"
            params.append(max_price)

        if search_query:
            query += " AND (p.name LIKE ? OR p.description LIKE ?)"
            params.append(f"%{search_query}%")
            params.append(f"%{search_query}%")

        if sort_by == "price_asc":
            query += " ORDER BY p.price ASC"
        elif sort_by == "price_desc":
            query += " ORDER BY p.price DESC"
        elif sort_by == "name":
            query += " ORDER BY p.name ASC"
        else:
            query += " ORDER BY p.id DESC"

        c.execute(query, params)
        return c.fetchall()

def add_product(name, description, price, stock, category_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO products (name, description, price, stock, category_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, price, stock, category_id, now))
            conn.commit()
            return True
        except Exception as e:
            print(f"✗ Ошибка при добавлении товара: {e}")
            return False

def update_product(product_id, name, description, price, stock, category_id):
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("""
                UPDATE products 
                SET name = ?, description = ?, price = ?, stock = ?, category_id = ?
                WHERE id = ?
            """, (name, description, price, stock, category_id, product_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"✗ Ошибка обновления товара: {e}")
            return False

def delete_product(product_id):
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"✗ Ошибка удаления товара: {e}")
            return False

def add_to_cart(user_id, product_id, quantity):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
        prod = c.fetchone()
        if not prod:
            print("✗ Товар не найден.")
            return False
        
        stock = prod[0]
        c.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        cart_item = c.fetchone()
        current_cart_qty = cart_item[0] if cart_item else 0
        
        if current_cart_qty + quantity > stock:
            print(f"✗ Недоступно такое количество! Доступно на складе: {stock}, в вашей корзине: {current_cart_qty}.")
            return False

        if cart_item:
            c.execute("UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?", 
                      (quantity, user_id, product_id))
        else:
            c.execute("INSERT INTO cart (user_id, product_id, quantity, added_at) VALUES (?, ?, ?, ?)",
                      (user_id, product_id, quantity, now))
        conn.commit()
        print("✓ Товар успешно добавлен в корзину.")
        return True

def get_cart_items(user_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT c.id, p.id, p.name, p.price, c.quantity, (p.price * c.quantity) as subtotal
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        """, (user_id,))
        return c.fetchall()

def remove_from_cart(user_id, cart_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (cart_id, user_id))
        conn.commit()
        print("✓ Товар удален из корзины.")

def create_order(user_id):
    items = get_cart_items(user_id)
    if not items:
        print("✗ Корзина пуста. Нечего оформлять.")
        return False

    with get_connection() as conn:
        c = conn.cursor()
        total_price = 0
        for cart_id, prod_id, name, price, qty, subtotal in items:
            c.execute("SELECT stock FROM products WHERE id = ?", (prod_id,))
            stock_res = c.fetchone()
            if not stock_res or stock_res[0] < qty:
                print(f"✗ Недостаточно товара '{name}' на складе.")
                return False
            total_price += subtotal

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO orders (user_id, order_date, total_price, status) VALUES (?, ?, ?, ?)",
                  (user_id, now, total_price, "Оформлен"))
        order_id = c.lastrowid

        for cart_id, prod_id, name, price, qty, subtotal in items:
            c.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)",
                      (order_id, prod_id, qty, price))
            c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, prod_id))

        c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()
        print(f"✓ Заказ #{order_id} успешно оформлен! Сумма: {total_price:.2f} руб.")
        return True

def get_user_orders(user_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, order_date, total_price, status FROM orders WHERE user_id = ? ORDER BY id DESC", (user_id,))
        orders = c.fetchall()
        result = []
        for o in orders:
            c.execute("""
                SELECT oi.product_id, p.name, oi.quantity, oi.price_at_purchase
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """, (o[0],))
            result.append((o, c.fetchall()))
        return result

def get_all_orders():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT o.id, u.username, o.order_date, o.total_price, o.status 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            ORDER BY o.id DESC
        """)
        orders = c.fetchall()
        result = []
        for o in orders:
            c.execute("""
                SELECT p.name, oi.quantity, oi.price_at_purchase
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """, (o[0],))
            result.append((o, c.fetchall()))
        return result

def update_order_status(order_id, new_status):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        print(f"✓ Статус заказа #{order_id} изменен на '{new_status}'.")


def get_sales_report_by_category():
    """Сложный запрос: GROUP BY, JOIN, SUM, COALESCE, ORDER BY"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT 
                c.name AS category_name,
                COUNT(DISTINCT p.id) AS total_products,
                COALESCE(SUM(oi.quantity), 0) AS items_sold,
                COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0.0) as total_revenue
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            LEFT JOIN order_items oi ON p.id = oi.product_id
            GROUP BY c.id, c.name
            ORDER BY total_revenue DESC;
        """)
        return c.fetchall()

def get_top_customers():
    """Сложный запрос: Топ клиентов по сумме покупок"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT 
                u.username,
                u.email,
                COUNT(o.id) AS total_orders,
                SUM(o.total_price) AS money_spent
            FROM users u
            JOIN orders o ON u.id = o.user_id
            WHERE o.status != 'Отменен'
            GROUP BY u.id, u.username, u.email
            ORDER BY money_spent DESC
            LIMIT 5;
        """)
        return c.fetchall()

def get_unsold_products():
    """Сложный запрос: Неликвидные товары (LEFT JOIN ... IS NULL)"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT p.id, p.name, p.price, p.stock
            FROM products p
            LEFT JOIN order_items oi ON p.id = oi.product_id
            WHERE oi.product_id IS NULL;
        """)
        return c.fetchall()

def get_products_with_ratings():
    """Сложный запрос: Рейтинг товаров через AVG() и GROUP BY"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT 
                p.id, 
                p.name, 
                p.price, 
                p.stock,
                COALESCE(AVG(r.rating), 0) AS avg_rating,
                COUNT(r.id) AS reviews_count
            FROM products p
            LEFT JOIN reviews r ON p.id = r.product_id
            GROUP BY p.id, p.name, p.price, p.stock
            ORDER BY avg_rating DESC;
        """)
        return c.fetchall()
