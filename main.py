import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem
from archivo import Ui_MainWindow  # Importa el diseño generado por Qt Designer
from PyQt6.QtGui import QPixmap

class CustomWidget(QWidget):
    def __init__(self, image_path, product_name, price, parent=None):
        super().__init__(parent)

        # Creación de los widgets hijos
        image_label = QLabel()
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen en {image_path}")
        else:
            # Ajusta el tamaño de la imagen para que tenga un tamaño más pequeño (por ejemplo 50x50)
            image_label.setPixmap(pixmap.scaled(50, 50))  # Escalamos la imagen con relación de aspecto

        # Establecemos un tamaño fijo para el QLabel de la imagen para que no sea muy ancho
        image_label.setFixedSize(50, 50)  # Tamaño fijo para el QLabel que contiene la imagen

        name_label = QLabel(product_name)
        price_label = QLabel(f"${price:.2f}")

        # Estilos opcionales para el texto
        name_label.setStyleSheet("background-color: transparent; color: black;")
        price_label.setStyleSheet("background-color: transparent; color: black;")

        # Layout horizontal para los widgets
        layout = QHBoxLayout()
        layout.addWidget(image_label)  # Añadimos la imagen con tamaño fijo
        layout.addWidget(name_label)
        layout.addWidget(price_label)

        # Asignamos el layout al widget
        self.setLayout(layout)

        # Guardamos referencias a los textos por si los necesitamos luego
        self.name_label = name_label
        self.price_label = price_label


# Clase principal para la ventana
from PyQt6.QtWidgets import QTableWidgetItem

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Inicializamos la lista de productos
        self.selected_products = {}

        # Lista de productos con su información (imagen, nombre, precio)
        products = [
            {"image": "imagenes/galleta1.jpg", "name": "Galleta de Chocolate", "price": 10},
            {"image": "imagenes/galleta2.jpg", "name": "Galleta de Chocolate de corazon", "price": 8},
            # Agrega más productos según sea necesario
        ]

        for product in products:
            item = QListWidgetItem(self.items)
            custom_widget = CustomWidget(product["image"], product["name"], product["price"])
            item.setSizeHint(custom_widget.sizeHint())
            self.items.setItemWidget(item, custom_widget)

        # Conectar la selección de un producto con la función para agregarlo a la orden
        self.items.itemClicked.connect(self.add_to_order)

    def add_to_order(self, item):

        custom_widget = self.items.itemWidget(item)
        product_name = custom_widget.name_label.text()
        product_price = float(custom_widget.price_label.text().replace('$', ''))

        # Si el producto ya está en la tabla, solo incrementamos la cantidad
        if product_name in self.selected_products:
            self.selected_products[product_name]["quantity"] += 1
        else:
            # Si es la primera vez que se selecciona, agregamos el producto a la lista
            self.selected_products[product_name] = {
                "price": product_price,
                "quantity": 1
            }

        # Actualizamos la tabla con los productos seleccionados
        self.update_table()

    def update_table(self):
        # Limpiamos la tabla antes de actualizarla
        self.tableWidget.setRowCount(0)

        # Recorremos los productos seleccionados y los agregamos a la tabla
        for row, (product_name, details) in enumerate(self.selected_products.items()):
            price = details["price"]
            quantity = details["quantity"]
            subtotal = price * quantity

            # Insertamos una nueva fila en la tabla
            self.tableWidget.insertRow(row)

            # Insertamos los valores en la tabla
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product_name))  # Columna Producto
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(quantity)))  # Columna Cantidad
            self.tableWidget.setItem(row, 2, QTableWidgetItem(f"${subtotal:.2f}"))  # Columna Subtotal

        # Actualizamos el precio total de la orden
        self.update_total_price()

    def update_total_price(self):
        # Calculamos el precio total sumando los subtotales de todos los productos
        total_price = sum(details["price"] * details["quantity"] for details in self.selected_products.values())
        self.totalPriceLabel.setText(f"Precio total: ${total_price:.2f}")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()  # Instanciamos la ventana principal
    win.show()  # Mostramos la ventana
    sys.exit(app.exec())  # Ejecutamos la aplicación
