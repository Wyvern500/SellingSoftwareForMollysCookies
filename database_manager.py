import sqlite3

# Ruta al archivo SQL y a la base de datos
sql_file_path = "database/database_creation_script_sqlite.sql"
sqlite_db_path = "database/database.db"

class DataBaseManager:

    def __init__(self):
        # Crear conexión a SQLite
        self.InitDataBase()
        # self.insert_data("ingredient", {"name": "Dildo", "amount":5, "price":10.50,
        #                                "description":"Sientate,relajate, disfruta...","product_type":"Unidad", "image_path": ""} )
        """
            name TEXT NOT NULL,
          amount INTEGER NOT NULL,
          price REAL NOT NULL,
          description TEXT,
          product_type TEXT NOT NULL,
          image_path TEXT NOT NULL
        """
        print(self.get_all_data_from_table("ingredient"))

    def InitDataBase(self):
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        # Leer el script SQL
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Ejecutar el script
        try:
            cursor.executescript(sql_script)
            print("Base de datos creada exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al ejecutar el script: {e}")

        conn.close()

    def get_all_data_from_table (self, table_name):

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows  # La conexión se cierra automáticamente aquí

    def create_connection(self):
        # Conectar o crear la base de datos
        conn = sqlite3.connect(sqlite_db_path)
        # Crear un cursor para ejecutar sentencias SQL
        return conn, conn.cursor()

    def insert_data(self, table_name, data: dict):
        conn, cursor = self.create_connection()

        # Construir las columnas y los placeholders
        keys = ",".join(data.keys())  # Nombres de las columnas
        values = ",".join(["?"] * len(data))  # Placeholders para los valores

        # Crear la consulta dinámica
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"

        try:
            # Ejecutar la consulta
            cursor.execute(query, list(data.values()))
            conn.commit()  # Confirmar los cambios
            print("Datos insertados correctamente.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
        finally:
            conn.close()  # Cerrar la conexión


