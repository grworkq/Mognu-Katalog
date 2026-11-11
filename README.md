# 🛒 CLI Online Shop with SQLite & Advanced SQL Analytics

A modular Command Line Interface (CLI) application built in **Python** powered by a **SQLite** relational database. It features secure password authentication, shopping cart functionality, checkout management, an admin dashboard, and complex analytical SQL queries.

## 🌟 Key Features

* **🔑 Secure Authentication:** Password hashing using unique salt values via the industry-standard `PBKDF2-HMAC-SHA256` algorithm.

* **🛍 Modular Catalog & Advanced Search:** Keyword search (`LIKE`), price range filtering, category selection, and flexible sorting algorithms.

* **🛒 Shopping Cart & Checkout:** Real-time stock verification (`stock`), subtotal/total calculations, and automated order creation.

* **👨‍💼 Admin Panel:** Full management of product categories, inventory stock editing, and order status updates.

* **📊 Complex SQL Analytics:** Built-in reporting module utilizing `GROUP BY`, `JOIN`, `SUM`, `AVG`, `COUNT`, and `LEFT JOIN ... IS NULL` queries.

* **📦 Pre-populated Database:** Includes **20 categories** and **320+ products** with realistic data and pricing.

## 📁 Project Structure

```
├── main.py      # Main entry point and CLI menu logic
├── database.py    # SQLite database handlers, CRUD operations & analytical queries
├── auth.py        # Cryptographic password hashing and verification module (SHA-256)
├── home.py        # Customer menu, catalog navigation, and cart management
├── admin.py       # Admin dashboard and analytical SQL report views
└── shop.db        # SQLite database file (pre-filled with 20 categories & 320+ items)
```

## 🚀 Quick Start

### Prerequisites

* Python `3.8` or higher.

* Built-in Python modules (`sqlite3`, `hashlib`, `os`, `sys`, `datetime`). No external third-party dependencies are required.

### Execution Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/grworkq/Mognu-Katalog.git
   cd Mognu-Katalog
   ```

2. Run the main application entry point:

   ```bash
   python main.py
   ```

## 🔑 Default Credentials

For testing purposes, pre-configured accounts are available out of the box:

| Role | Username / Email | Password | Available Features |
| ----- | ----- | ----- | ----- |
| **Administrator** | `admin` or `admin@shop.com` | `admin123` | Admin dashboard, inventory management, SQL analytics |
| **Customer 1** | `ivan_petrov` | `ivan2026` | Catalog search, filtering, cart management, ordering |
| **Customer 2** | `anna_smirnova` | `anna2026` | Catalog search, filtering, cart management, ordering |

## 📊 Analytical SQL Queries Demonstrated

The application incorporates advanced SQL concepts required for relational database analysis:

1. **Category Sales & Revenue Report:**
   `JOIN`, `LEFT JOIN`, `SUM()`, `COUNT(DISTINCT)`, `GROUP BY`, `COALESCE()`, `ORDER BY`.

2. **Top Customers by Total Spending:**
   `JOIN`, `SUM()`, `GROUP BY`, `WHERE`, `ORDER BY`, `LIMIT`.

3. **Unsold Product Analysis (Zero Sales):**
   `LEFT JOIN ... WHERE oi.product_id IS NULL`.

4. **Product Rating Report:**
   `LEFT JOIN`, `AVG()`, `COUNT()`, `GROUP BY`, `ORDER BY`.

## 👨‍💻 Development Team

* **Gor Ogannisyan** — Project Manager

* **Musab Alhadi** — CLI UI & Presentation

* **Ivan Zyz** — Deputy PM / Database Architect

* **Egor Krasnousov** — Database Developer & Data Analyst