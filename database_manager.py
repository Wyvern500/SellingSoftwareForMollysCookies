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

    def get_all_data_from_table(self, table_name):
        table_name = self.process_table_name(table_name)

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows  # La conexión se cierra automáticamente aquí

    def get_id_for_table_by_field(self, table: str, field: str, target_value, id_prefix: str = "id"):
        table = self.process_table_name(table)

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            to_delete = "'"
            if type(target_value) is str:
                query = f"SELECT {id_prefix}{table.replace(to_delete, '')} FROM {table} WHERE {field} = '{target_value}';"
            else:
                query = f"SELECT {id_prefix}{table.replace(to_delete, '')} FROM {table} WHERE {field} = {target_value};"
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows

    def get_id_for_table_by_fields(self, table: str, data: dict, id_prefix: str = "id",
                                   id_name: str = ""):
        table = self.process_table_name(table)

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            to_delete = "'"
            to_check = []
            for key, value in data.items():
                if type(value) is str:
                    to_check.append(f"{key} = '{value}'")
                else:
                    to_check.append(f"{key} = {value}")

            conditions = " AND ".join(to_check)

            id_processed = ""

            if not id_name:
                id_processed = f"{id_prefix}{table.replace(to_delete, '')}"
            else:
                id_processed = f"{id_prefix}{id_name}"

            query = f"SELECT {id_processed} FROM {table} WHERE {conditions};"
            try:
                cursor.execute(query)
            except sqlite3.Error as e:
                print(f"Error al ejecutar el script: {e}")
            rows = cursor.fetchall()

        return rows

    def get_records_by_fields(self, table_name: str, conditions: dict, order_by: str = "", ascendent = True, 
                              literal = False):
        table_name = self.process_table_name(table_name)

        to_check = []
        for key, value in conditions.items():
            if not literal:
                if type(value) is str:
                    to_check.append(f"{key} = '{value}'")
                else:
                    to_check.append(f"{key} = {value}")
            else:
                to_check.append(f"{key}{value}")

        conditions = " AND ".join(to_check)
        
        order_by_str = ""
        if len(order_by) > 0:
            order = ""
            if ascendent:
                order = "ASC"
            else:
                order = "DESC"
            order_by_str = f" ORDER BY {order_by} {order}"
            print(f"Order by: {order_by_str}")

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name} WHERE {conditions}{order_by_str};"
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows

    def get_records_by_field(self, table_name: str, field: str, target_value):
        table_name = self.process_table_name(table_name)

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()
            if type(target_value) is str:
                query = f"SELECT * FROM {table_name} WHERE {field} = '{target_value}';"
            else:
                query = f"SELECT * FROM {table_name} WHERE {field} = {target_value};"
            try:
                cursor.execute(query)
                print("Record obtenido exitosamente.")
            except sqlite3.Error as e:
                print(f"Error al ejecutar el script: {e}")
            rows = cursor.fetchall()

        return rows

    def remove_record_from_table_by_field(self, table: str, field: str, target_value):
        table = self.process_table_name(table)

        with sqlite3.connect(sqlite_db_path) as conn:
            cursor = conn.cursor()

            if type(target_value) is str:
                query = f"DELETE FROM {table} WHERE {field} = '{target_value}';"
            else:
                query = f"DELETE FROM {table} WHERE {field} = {target_value};"
            print("Query: " + query)
            try:
                cursor.execute(query)
                print("Record eliminado exitosamente.")
            except sqlite3.Error as e:
                print(f"Error al ejecutar el script: {e}")


    def update_record_by_id(self, table: str, data: dict, conditions: dict):
        table = self.process_table_name(table)

        to_check = []
        for key, value in conditions.items():
            if type(value) is str:
                to_check.append(f"{key} = '{value}'")
            else:
                to_check.append(f"{key} = {value}")

        conditions = " AND ".join(to_check)

        to_update = []
        for key, value in data.items():
            if type(value) is str:
                to_update.append(f"{key} = '{value}'")
            else:
                to_update.append(f"{key} = {value}")

        updates = ", ".join(to_update)

        with sqlite3.connect(sqlite_db_path, isolation_level="EXCLUSIVE") as conn:
            cursor = conn.cursor()

            query = f"UPDATE {table} SET {updates} WHERE {conditions};"
            print(f"Update Query: {query}")
            try:
                cursor.execute(query)
                conn.commit()
                print("Datos actualizados exitosamente.")
            except sqlite3.Error as e:
                print(f"Error al ejecutar el script: {e}")

            # Verifica si se actualizó alguna fila
            if cursor.rowcount == 0:
                print("No se actualizó ninguna fila. Verifica las condiciones del WHERE.")

            rows = cursor.fetchall()

        return rows

    def create_connection(self):
        # Conectar o crear la base de datos
        conn = sqlite3.connect(sqlite_db_path)
        # Crear un cursor para ejecutar sentencias SQL
        return conn, conn.cursor()

    def insert_data(self, table_name, data: dict):
        table_name = self.process_table_name(table_name)

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

    def process_table_name(self, table_name: str):
        if table_name == "order":
            return "'order'"
        return table_name
