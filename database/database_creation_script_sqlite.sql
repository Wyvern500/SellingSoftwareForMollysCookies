-- SQLite Script Converted from MySQL

-- Table: ingredient
CREATE TABLE ingredient (
  idingredient INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  amount INTEGER NOT NULL,
  price REAL NOT NULL,
  description TEXT,
  product_type TEXT NOT NULL,
  image_path TEXT NOT NULL
);

-- Table: product
CREATE TABLE product (
  idproduct INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  price REAL NOT NULL,
  description TEXT,
  image_path TEXT NOT NULL
);

-- Table: order
CREATE TABLE "order" (
  idorder INTEGER PRIMARY KEY,
  name TEXT,
  total REAL NOT NULL,
  date TEXT
);

-- Table: ingredient_has_product
CREATE TABLE ingredient_has_product (
  ingredient_idingredient INTEGER NOT NULL,
  product_idproduct INTEGER NOT NULL,
  PRIMARY KEY (ingredient_idingredient, product_idproduct),
  FOREIGN KEY (ingredient_idingredient) REFERENCES ingredient (idingredient),
  FOREIGN KEY (product_idproduct) REFERENCES product (idproduct)
);

-- Table: product_has_order
CREATE TABLE product_has_order (
  product_idproduct INTEGER NOT NULL,
  order_idorder INTEGER NOT NULL,
  PRIMARY KEY (product_idproduct, order_idorder),
  FOREIGN KEY (product_idproduct) REFERENCES product (idproduct),
  FOREIGN KEY (order_idorder) REFERENCES "order" (idorder)
);

-- Table: order_entry_wraper
CREATE TABLE order_entry_wraper (
  idorder_product_wraper INTEGER PRIMARY KEY AUTOINCREMENT,
  amount INTEGER,
  subtotal REAL,
  product_idproduct INTEGER NOT NULL,
  order_idorder INTEGER NOT NULL,
  FOREIGN KEY (product_idproduct) REFERENCES product (idproduct),
  FOREIGN KEY (order_idorder) REFERENCES "order" (idorder)
);
