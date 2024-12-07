from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QPushButton
from datetime import datetime

import Product.add_product_manager as Product
from gui import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout
from datetime import datetime

from simple_manager import AbstractTabManager


def get_formatted_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class OrderEntryWrapper:

    def __init__(self, product: Product, amount: int):
        self.product = product
        self.amount = amount


class Order:

    def __init__(self, name: str, total: float, date_time: str = get_formatted_current_datetime()):
        self.name: str = name
        self.total: float = total
        self.datetime: str = date_time
        self.order_entries: list[OrderEntryWrapper] = []

    def add_order_entry(self, order_entry: OrderEntryWrapper):
        self.order_entries.append(order_entry)

    def serialize(self):
        return {"name": f'{self.name}', "total": self.total, "date": f'{self.datetime}'}


class CreateOrderManager(AbstractTabManager):

    def __init__(self, parent):
        super().__init__(parent)

        # Conectar las senales pertinentes
        # Conectar la selección de un producto con la función para agregarlo a la orden y mostrar características
        self.parent.crear_items_listWidget.itemClicked.connect(self.display_product_features)
        self.parent.crear_items_listWidget.itemDoubleClicked.connect(self.add_to_order)

        self.parent.crear_orden_crear_orden_button.pressed.connect(self.create_order)

        self.load_items_from_database()
        print(self.parent.database_manager.get_all_data_from_table("order"))
        print(self.parent.database_manager.get_all_data_from_table("order_entry_wraper"))

    def create_order(self):
        order_name = self.parent.crear_orden_nombre_orden_lineEdit.text()
        if not order_name:
            order_name = get_formatted_current_datetime()
        # Esto se hace porque si no da error, ya que el string que retorna este label
        # tiene texto incluido (Total price: 1000.0), por eso se hace este sencillo
        # tratamiento de string
        true_total_price_value: str = (self.parent.crear_orden_totalprice_label.text()
                                       .split(":")[1].replace("$", "").strip())
        order = Order(order_name, float(true_total_price_value))

        for row in range(0, self.parent.crear_orden_orderList_tableWidget.rowCount()):
            product: Product = (self.parent.crear_orden_orderList_tableWidget
                                .cellWidget(row, 0).product)
            amount: int = int(self.parent.crear_orden_orderList_tableWidget.item(row, 1)
                                .text())
            order.add_order_entry(OrderEntryWrapper(product, amount))
        self.add_order_to_database(order)

    def add_order_to_database(self, order: Order):
        # Agregando la orden a la base de datos, ojo, esto es solo la orden, no los
        # productos
        database = self.parent.database_manager
        database.insert_data("order", order.serialize())

        order_id = database.get_id_for_table_by_field("order", "name", order.name)[0][0]

        # Agregando los productos de la orden a la base de datos
        for order_entry in order.order_entries:
            # Obteniendo el id del producto para enlazar la orden con el producto
            # en la base de datos
            product_id = (database.get_id_for_table_by_field("product", "name",
                                                             order_entry.product.name))[0][0]
            database.insert_data("order_entry_wraper",
                                                     {"amount": order_entry.amount,
                                                      "subtotal": order_entry.amount * order_entry.product.price,
                                                      "product_idproduct": product_id,
                                                      "order_idorder": order_id})
        self.parent.selected_products.clear()

    def update_table(self):
        # Limpiamos la tabla antes de actualizarla
        self.parent.crear_orden_orderList_tableWidget.setRowCount(0)
        self.parent.crear_orden_orderList_tableWidget.setColumnCount(3)
        self.parent.crear_orden_orderList_tableWidget.setHorizontalHeaderLabels(["Producto", "Cantidad", "Subtotal"])

        # Recorremos los productos seleccionados y los agregamos a la tabla
        for row, (product_name, details) in enumerate(self.parent.selected_products.items()):
            product: Product = details["product"]
            price = product.price
            quantity = details["quantity"]
            subtotal = price * quantity
            # Insertamos una nueva fila en la tabla
            self.parent.crear_orden_orderList_tableWidget.insertRow(row)

            product_widget = ProductWidget(product)
            self.parent.crear_orden_orderList_tableWidget.setCellWidget(row,
                                                                        0, product_widget)
            # Insertamos los valores en la tabla
            self.parent.crear_orden_orderList_tableWidget.setItem(row, 1,
                                                                  QTableWidgetItem(str(quantity)))  # Columna Cantidad
            self.parent.crear_orden_orderList_tableWidget.setItem(row, 2,
                                                                  QTableWidgetItem(
                                                                      f"${subtotal:.2f}"))  # Columna Subtotal

        # Actualizamos el precio total de la orden
        self.update_total_price()

    def update_total_price(self):
        # Calculamos el precio total sumando los subtotales de todos los productos
        total_price = sum(
            details["product"].price * details["quantity"] for details in self.parent.selected_products.values())
        self.parent.crear_orden_totalprice_label.setText(f"Precio total: ${total_price:.2f}")

    def add_to_order(self, item):
        custom_widget = self.parent.crear_items_listWidget.itemWidget(item)
        product_name = custom_widget.product.name
        # Si el producto ya está en la tabla, solo incrementamos la cantidad
        if product_name in self.parent.selected_products:
            self.parent.selected_products[product_name]["quantity"] += 1
        else:
            self.parent.selected_products[product_name] = {
                # Diccionario que guarda todos los productos seleccionados con detalles como precio, cantidad y la ruta de la imagen:
                "product": custom_widget.product,
                "quantity": 1,  # Si es la primera vez que se selecciona, agregamos el producto a la lista
            }
        # Actualizamos la tabla con los productos seleccionados
        self.update_table()

    def display_product_features(self, item):
        custom_widget = self.parent.crear_items_listWidget.itemWidget(item)
        product_name = custom_widget.name_label.text()
        # Mostrar las características en el cuadro de texto
        self.parent.crear_description_textEdit.setText(custom_widget.product.description)

    def load_items_from_database(self):
        alldata = self.parent.database_manager.get_all_data_from_table("product")

        for entry in alldata:
            # Crear un nuevo QListWidgetItem
            item = QListWidgetItem(self.parent.crear_items_listWidget)

            # Crear un widget personalizado para el producto
            product = Product.deserialize(entry)

            custom_widget = Product.ProductItemWidget(product)
            item.setSizeHint(custom_widget.sizeHint())

            # Agregar el widget personalizado al QListWidget
            self.parent.crear_items_listWidget.setItemWidget(item, custom_widget)


# Clase personalizada para mostrar imagen y nombre en la tabla
class ProductWidget(QWidget):

    def __init__(self, product, parent=None):
        super().__init__(parent)

        self.product = product

        # Crear los widgets para la imagen y el nombre
        image_label = QLabel()
        pixmap = QPixmap(self.product.image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(50, 50))  # Ajusta el tamaño de la imagen

        name_label = QLabel(self.product.name)
        name_label.setStyleSheet("background-color: transparent; color: black;")
        # name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Alinea el texto a la izquierda

        # Crear el layout y añadir los widgets
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Alinea todoo el layout a la izquierda
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina márgenes
        self.setLayout(layout)
