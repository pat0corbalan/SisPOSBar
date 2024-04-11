CREATE TABLE Customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT
);

CREATE TABLE Employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    email TEXT,
    phone TEXT
);

CREATE TABLE FixedCosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL
);

CREATE TABLE "Inventory" (
	"id"	INTEGER,
	"product_id"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"quantity"	INTEGER NOT NULL,
	FOREIGN KEY("product_id") REFERENCES "Products"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE PaymentMethods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE "Products" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	"cost"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"category"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE Sales (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    total REAL NOT NULL
);

CREATE TABLE SalesDetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (sale_id) REFERENCES Sales(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE SalesPaymentMethods (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    payment_method_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES Sales(id),
    FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods(id)
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE VariableCosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    amount REAL
)