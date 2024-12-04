from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem, QTableWidget, QTableWidgetItem, QFileDialog, QPushButton
from gui import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout

class CreateOrderManager:

    def __init__(self, parent):
        from window import Window
        self.parent: Window = parent

        # Conectar la selección de un producto con la función para agregarlo a la orden y mostrar características
        self.parent.crear_items_listWidget.itemClicked.connect(self.display_product_features)
        self.parent.crear_items_listWidget.itemDoubleClicked.connect(self.add_to_order)


    def update_table(self):
        # Limpiamos la tabla antes de actualizarla
        self.parent.crear_orderList_tableWidget.setRowCount(0)
        self.parent.crear_orderList_tableWidget.setColumnCount(3)
        self.parent.crear_orderList_tableWidget.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal"])

        # Recorremos los productos seleccionados y los agregamos a la tabla
        for row, (product_name, details) in enumerate(self.parent.selected_products.items()):
            print("0")
            image_path = details["image"]
            price = details["price"]
            quantity = details["quantity"]
            subtotal = price * quantity
            print("1")
            # Insertamos una nueva fila en la tabla
            self.parent.crear_orderList_tableWidget.insertRow(row)
            print("2")
            product_widget = ProductWidget(image_path, product_name)
            self.parent.crear_orderList_tableWidget.setCellWidget(row, 0, product_widget)

            # Insertamos los valores en la tabla
            self.parent.crear_orderList_tableWidget.setItem(row, 1, QTableWidgetItem(str(quantity)))  # Columna Cantidad
            self.parent.crear_orderList_tableWidget.setItem(row, 2, QTableWidgetItem(f"${subtotal:.2f}"))  # Columna Subtotal
            print("3")
        # Actualizamos el precio total de la orden
        self.update_total_price()
        print("4")

    def update_total_price(self):
        # Calculamos el precio total sumando los subtotales de todos los productos
        total_price = sum(details["price"] * details["quantity"] for details in self.parent.selected_products.values())
        self.parent.crear_totalprice_button.setText(f"Precio total: ${total_price:.2f}")

    def add_to_order(self, item):
        custom_widget = self.parent.crear_items_listWidget.itemWidget(item)
        product_name = custom_widget.name_label.text()
        product_price = float(custom_widget.price_label.text().replace('$', ''))
        image_path = custom_widget.image_path

        # Si el producto ya está en la tabla, solo incrementamos la cantidad
        if product_name in self.parent.selected_products:
            self.parent.selected_products[product_name]["quantity"] += 1
        else:

            self.parent.selected_products[product_name] = {         # Diccionario que guarda todos los productos seleccionados con detalles como precio, cantidad y la ruta de la imagen:
                "price": product_price,
                "quantity": 1,                                      # Si es la primera vez que se selecciona, agregamos el producto a la lista
                "image": image_path
            }

        # Actualizamos la tabla con los productos seleccionados
        self.update_table()


    def display_product_features(self, item):
        custom_widget = self.parent.crear_items_listWidget.itemWidget(item)
        product_name = custom_widget.name_label.text()
        # Mostrar las características en el cuadro de texto
        self.parent.crear_description_textEdit.setText(custom_widget.product_description)

# Clase personalizada para mostrar imagen y nombre en la tabla
class ProductWidget(QWidget):

    def __init__(self, image_path, product_name, parent=None):
        super().__init__(parent)

        # Crear los widgets para la imagen y el nombre
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(50, 50))  # Ajusta el tamaño de la imagen

        name_label = QLabel(product_name)
        name_label.setStyleSheet("background-color: transparent; color: black;")
        #name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Alinea el texto a la izquierda

        # Crear el layout y añadir los widgets
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Alinea todoo el layout a la izquierda
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina márgenes
        self.setLayout(layout)



class CustomWidget(QWidget):
    def __init__(self, image_path: str, product_name: str, price: float, product_description, parent=None):
        super().__init__(parent)

        # Crear QLabel para la imagen
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)

        self.image_path = image_path
        self.product_description = product_description

        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen desde {image_path}")
        else:
            # Escalar la imagen a un tamaño fijo (por ejemplo, 50x50)
            self.image_label.setPixmap(pixmap.scaled(50, 50))

        self.image_label.setFixedSize(50, 50)  # Fija el tamaño para evitar deformaciones

        # Crear QLabel para el nombre del producto
        self.name_label = QLabel(product_name)
        self.name_label.setStyleSheet("background-color: transparent; color: black; font-weight: bold;")

        # Crear QLabel para el precio del producto
        self.price_label = QLabel(f"${price:.2f}")
        self.price_label.setStyleSheet("background-color: transparent; color: black; font-weight: bold;")

        # Configurar el layout horizontal para imagen, nombre y precio
        layout = QHBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)

        # Crear un contenedor para los elementos con borde
        card_container = QWidget()
        card_container.setLayout(layout)

        # Estilo del contenedor para crear una "tarjeta" con bordes y márgenes
        card_container.setStyleSheet("""
            QWidget {
                border: 1px solid #black;
                border-radius: 10px;
                padding: 1px;
                margin: 1px;
                background-color: #f9f9f9;
            }
        """)

        # Crear un layout vertical para contener la tarjeta (esto puede ser útil si deseas más control)
        main_layout = QVBoxLayout()
        main_layout.addWidget(card_container)

        # Asignar el layout principal al widget
        self.setLayout(main_layout)


