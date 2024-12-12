from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QPushButton
from datetime import datetime

import error_utils
import utils
from Order.order_widgets import Order, OrderEntryWrapper, OrderEntryItemWidget
import Product.add_product_manager as Product
from gui import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout
from datetime import datetime

from simple_manager import AbstractTabManager


class CreateOrderManager(AbstractTabManager):

    def __init__(self, parent):
        super().__init__(parent)

        # Conectar las senales pertinentes
        # Conectar la selección de un producto con la función para agregarlo a la orden y mostrar características
        self.parent.crear_items_listWidget.itemClicked.connect(self.display_product_features)
        self.parent.crear_items_listWidget.itemDoubleClicked.connect(self.add_to_order)

        self.parent.crear_orden_crear_orden_button.pressed.connect(self.create_order)
        self.parent.crear_order_delete_product_button.pressed.connect(self.delete_product)
        self.parent.crear_orden_delete_order_entry.pressed.connect(self.delete_order_entry)

        self.parent.crear_order_search_product_lineEdit.textChanged.connect(self.search_products)
        self.parent.crear_orden_search_order_entry_lineEdit.textChanged.connect(self.search_order_entries)

        self.load_items_from_database()

    def create_order(self):
        order_name = self.parent.crear_orden_nombre_orden_lineEdit.text()

        if not order_name:
            return

        order_data = self.parent.database_manager.get_records_by_field("order",
                                                                       "name",
                                                                       order_name)

        if len(order_data) > 0:
            return

        if not order_name:
            order_name = utils.get_formatted_current_datetime()
        # Esto se hace porque si no da error, ya que el string que retorna este label
        # tiene texto incluido (Total price: 1000.0), por eso se hace este sencillo
        # tratamiento de string
        true_total_price_value: str = (self.parent.crear_orden_totalprice_label.text()
                                       .split(":")[1].replace("$", "").strip())
        order = Order(order_name, float(true_total_price_value))

        for i in range(self.parent.crear_orden_orderList_listWidget.count()):
            list_widget_item = self.parent.crear_orden_orderList_listWidget.item(i)
            order_entry_widget: OrderEntryItemWidget = (self.parent
                                                        .crear_orden_orderList_listWidget
                                                        .itemWidget(list_widget_item))
            order.add_order_entry(order_entry_widget.order_entry)
            
        self.add_order_to_database(order)
        self.parent.crear_orden_orderList_listWidget.clear()

    def delete_product(self):
        selected_products = self.parent.crear_items_listWidget.selectedItems()

        for product in selected_products:
            product_item_widget = self.parent.crear_items_listWidget.itemWidget(product)
            product_id = self.parent.database_manager.get_id_for_table_by_field("product",
                                                                                "name",
                                                                                product_item_widget.
                                                                                product.name)[0][0]
            data = self.parent.database_manager.get_records_by_field("order_entry_wraper",
                                                                     "product_idproduct",
                                                                     product_id)
            if len(data) > 0:
                error_utils.show_error_message("Para eliminar un producto, no debe estar en ninguna orden")
                return

        for product in selected_products:
            product_item_widget = self.parent.crear_items_listWidget.itemWidget(product)
            product_id = self.parent.database_manager.get_id_for_table_by_field("product",
                                                                                "name",
                                                                                product_item_widget.
                                                                                product.name)[0][0]

            # Eliminando el producto de la base de datos
            self.parent.database_manager.remove_record_from_table_by_field("product",
                                                                           "idproduct",
                                                                           product_id)

            # Eliminando el producto del QListWidget
            row = self.parent.crear_items_listWidget.row(product)
            self.parent.crear_items_listWidget.takeItem(row)
    
    def delete_order_entry(self):
        for item in self.parent.crear_orden_orderList_listWidget.selectedItems():
            
            self.parent.crear_orden_orderList_listWidget.takeItem(self.parent
                                                                  .crear_orden_orderList_listWidget
                                                                  .row(item))
            
    def search_products(self):
        text = self.parent.crear_order_search_product_lineEdit.text().lower()
        for i in range(self.parent.crear_items_listWidget.count()):
            item = self.parent.crear_items_listWidget.item(i)
            widget = self.parent.crear_items_listWidget.itemWidget(item)
            
            # Mostrar u ocultar ítems según la coincidencia
            if text in widget.product.name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def search_order_entries(self):
        text = self.parent.crear_orden_search_order_entry_lineEdit.text().lower()
        for i in range(self.parent.crear_orden_orderList_listWidget.count()):
            item = self.parent.crear_orden_orderList_listWidget.item(i)
            widget: OrderEntryItemWidget = self.parent.crear_orden_orderList_listWidget.itemWidget(item)
            
            # Mostrar u ocultar ítems según la coincidencia
            if text in widget.product.name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

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

    def update_total_price(self):
        pass
        """
        # Calculamos el precio total sumando los subtotales de todos los productos
        total_price = sum(
            details["product"].price * details["quantity"] for details in self.parent.selected_products.values())
        self.parent.crear_orden_totalprice_label.setText(f"Precio total: ${total_price:.2f}")
        """

    def add_to_order(self, item_to_add):
        product_widget: Product.ProductItemWidget = (self.parent
                                                     .crear_items_listWidget
                                                     .itemWidget(item_to_add))
        for i in range(self.parent.crear_orden_orderList_listWidget.count()):
            list_widget_item = self.parent.crear_orden_orderList_listWidget.item(i)
            order_entry_widget: OrderEntryItemWidget = (self.parent
                                                        .crear_orden_orderList_listWidget
                                                        .itemWidget(list_widget_item))
            if product_widget.product.name == order_entry_widget.product.name:
                order_entry_amount = int(order_entry_widget.quantity_line_edit.text())
                order_entry_widget.setAmount(order_entry_amount + 1)
                return
        self.add_order_entry_to_list(OrderEntryWrapper(product_widget.product, 1))

    def add_order_entry_to_list(self, order_entry: OrderEntryWrapper):
        # Crear el widget personalizado
        order_entry_widget = OrderEntryItemWidget(order_entry)
        order_entry_widget.event.add_listener(self.on_finished_editing_amount)
        order_entry_widget.amount_changed_event.add_listener(self.on_amount_changed)

        # Crear un QListWidgetItem para envolver el widget
        list_item = QListWidgetItem(self.parent.crear_orden_orderList_listWidget)
        # Ajustar el tamaño del item al tamaño del widget
        list_item.setSizeHint(order_entry_widget.sizeHint())
        # Agregar el widget al QListWidget
        self.parent.crear_orden_orderList_listWidget.setItemWidget(list_item, order_entry_widget)
        self.set_total()

    def on_finished_editing_amount(self, data):
        if data["name"] == "editing_finished":
            order_entry: OrderEntryItemWidget = data["sender"]
            
            new_amount = int(order_entry.quantity_line_edit.text())
            order_entry.setAmount(new_amount)
    
    def on_amount_changed(self, data):
        self.set_total()
    
    def set_total(self):
        total = 0
        
        for i in range(self.parent.crear_orden_orderList_listWidget.count()):
            list_widget_item = self.parent.crear_orden_orderList_listWidget.item(i)
            order_entry_widget: OrderEntryItemWidget = (self.parent
                                                        .crear_orden_orderList_listWidget
                                                        .itemWidget(list_widget_item))
            total += order_entry_widget.product.price * order_entry_widget.order_entry.amount
            
        self.parent.crear_orden_totalprice_label.setText(f"Total a pagar: ${total}")

    def display_product_features(self, item):
        custom_widget = self.parent.crear_items_listWidget.itemWidget(item)

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
    
    def tab_changed(self, index: int):
        if self.parent.tabs.indexOf(self.parent.crearordenTab) == index:
            self.parent.crear_items_listWidget.clear()
            self.load_items_from_database()


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
