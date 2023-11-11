# frosit_ecommerce_FAST_API

[Frosit_HR] Back-end Development Position - Home task
## Overview

This project implements a back-end API for an e-commerce system, providing functionalities for sales analysis, revenue tracking, inventory management, and product registration. The API is developed using Python and FastAPI, with data storage handled by a MySQL database.

I have assumed two categories i.e ( Mobile Phones and Laptops )  
Use 1 category id for Mobile phone and 2 for laptop while add/running the add product API

## API Endpoints   (Total : 9)

### 1. Sales Status API

- Endpoint: `/sales`
- Functionality: Retrieve, filter, and analyze sales data.

### 2. Revenue Analysis API

- Endpoint: `/revenue`
- Functionality: Analyze revenue on a daily, weekly, monthly, or annual basis.
  - Input: `interval` (daily, weekly, monthly, annual)
  - Output: List of dictionaries with date and revenue.

### 3. Compare Revenue Across Periods and Categories API

- Endpoint: `/revenue/comparison`
- Functionality: Compare revenue across different periods and categories.
  - Input: `start_date`, `end_date`, `category_ids`
  - Output: List of dictionaries with period, category ID, category name, and revenue.

### 4. View Current Inventory API

- Endpoint: `/inventory`
- Functionality: View current inventory status.

### 5. Low Stock Alerts API

- Endpoint: `/inventory/low-stock-alerts/{thrashold}`
- Functionality: View products with low stock.
  - Input: `threshold` (optional, default is 10)
  - Output: List of products with low stock.

### 6. Update Inventory Levels API

- Endpoint: `/inventory/update`
- Functionality: Update inventory levels for a product.
  - Input: `product_id`, `new_quantity`
  - Output: Updated inventory information.

### 7. Inventory History API

- Endpoint: `/inventory/history/{product_id}`
- Functionality: Retrieve inventory history for a product.
  - Input: `product_id`
  - Output: List of inventory history entries.

### 8. Get Products API

- Endpoint: `/products`
- Functionality: Retrieve a list of all products.
  - Output: List of products.

### 9. Add Product API

- Endpoint: `/products/add`
- Functionality: Add a new product to the database.
  - Input: Product details (e.g., name, description, price).
  - Output: New product information.

## Database Tables

1. Products Table
   - Fields: `product_id`, `name`, `description`, `price`, ...

2. Sales Table
   - Fields: `sale_id`, `product_id`, `sale_date`, `amount`, ...

3. Inventory Table
   - Fields: `inventory_id`, `product_id`, `quantity_available`, `last_updated`, ...

4. Categories Table
   - Fields: `category_id`, `name`, ...
5.  Inventory History Table 
    -Fileds: `history_id`, `product_id`, `quantity_available , last_updated`

## Getting Started

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the MySQL database and configure the connection in `config.py`.
4. Run the FastAPI application: `uvicorn main:app --reload`

--- To check APIs on local host – 
http://127.0.0.1:8000/docs         (change the port number according to your port numberer )


---  Datbase ---

Database is exported and file name is ecommerce_db.sql 
Import the database file in Mysql and the database name is ecommerce


Folders Structure
 forsit_ecommerce/
│   ├── api_routes/
│   │   ├── endpoints/
│   │   │   ├── sales.py
│   │   │   ├── inventory.py
│   │   │   ├── products.py
│   │   │   └── revenue.py
│   │   
│   ├── db/
│   │   └── base.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   ├── sale.py
│   │   ├── inventory.py
│   │   └── category.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   ├── sale.py
│   │   ├── inventory.py
│   │   └── revenue.py
│   │
│   ├── main.py│
└── README.md
