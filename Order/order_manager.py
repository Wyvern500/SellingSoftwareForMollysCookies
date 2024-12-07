from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidgetItem, QHBoxLayout

from Order.create_order_manager import OrderEntryWrapper
from simple_manager import AbstractTabManager
import Product.add_product_manager as Product
from Order.create_order_manager import Order


class OrderListItem(QWidget):
    def __init__(self, order: Order, parent=None):
        super().__init__(parent)

        self.order = order

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Opcional: Ajusta los márgenes
        layout.setSpacing(2)

        # Etiquetas para mostrar el nombre y la fecha
        self.name_label = QLabel(order.name)
        self.name_label.setStyleSheet("color: black; background-color: white; font-weight: bold;")  # Estilo opcional
        self.date_label = QLabel(order.datetime)
        self.date_label.setStyleSheet("color: black; background-color: white; font-size: 11px;")  # Estilo opcional

        # Añadir widgets al layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.date_label)

        # Asignar layout
        self.setLayout(layout)


class OrderEntryItemWidget(QWidget):

    def __init__(self, order_entry: OrderEntryWrapper, parent=None):
        super().__init__(parent)

        self.order_entry = order_entry
        self.product = order_entry.product

        self.setToolTip(self.product.description)

        # Agregando estilo a los items
        self.add_style()

        # Layout principal
        layout = QHBoxLayout(self)
        # Imagen a la izquierda
        self.image_label = QLabel(self)

        image = QPixmap(self.product.image_path)
        if image.isNull():
            image = QPixmap("imagenes/image_not_found.png")

        self.image_label.setPixmap(image.scaled(64, 64))
        layout.addWidget(self.image_label)
        # Ajustar el espacio ocupado por la imagen
        layout.setStretch(0, 1)  # Imagen toma menos espacio

        # Detalles a la derecha de la imagen
        details_layout = QVBoxLayout()

        self.name_label = QLabel(f"Producto: {self.product.name}")
        self.quantity_label = QLabel(f"Cantidad: {order_entry.amount}")
        self.total_label = QLabel(f"Total: ${self.product.price * order_entry.amount}")

        details_layout.addWidget(self.name_label)
        details_layout.addWidget(self.quantity_label)
        details_layout.addWidget(self.total_label)

        layout.addLayout(details_layout)
        layout.setStretch(1, 4)  # Detalles toman más espacio

    def add_style(self):
        # Aplicar un borde al widget
        self.setStyleSheet("""
                QWidget{
                    background-color: white;
                    padding: 3px;       /* Espaciado interno */
                }
                """)


class OrderManager(AbstractTabManager):

    def __init__(self, parent):
        super().__init__(parent)

        self.load_orders_from_database()

        self.parent.order_orders_listWidget.itemDoubleClicked.connect(self.on_order_double_click)
        self.parent.order_delete_order_button.pressed.connect(self.on_delete_order)
        self.parent.order_delete_order_entry_button.pressed.connect(self.on_delete_order_entry)

    def on_order_double_click(self, item: QListWidgetItem):
        self.parent.order_order_entries_listWidget.clear()
        self.load_order_entries_from_database(self.parent.order_orders_listWidget
                                              .itemWidget(item))

    def on_delete_order(self):
        selected_orders = self.parent.order_orders_listWidget.selectedItems()

        for selected_order in selected_orders:
            order_item: OrderListItem = (self.parent.order_orders_listWidget
                                         .itemWidget(selected_order))
            order_id = self.get_order_id(order_item.order.name)

            # Eliminando la orden de la base de datos
            self.parent.database_manager.remove_record_from_table_by_field("order",
                                                                           "idorder",
                                                                           order_id)

            # Eliminando la orden de la QListWidget
            self.parent.order_orders_listWidget.takeItem(self.parent
                                                         .order_orders_listWidget
                                                         .row(selected_order))

    def on_delete_order_entry(self):
        selected_order_entries = self.parent.order_order_entries_listWidget.selectedItems()

        for selected_order_entry in selected_order_entries:
            order_id = self.get_order_id()

            order_entry: OrderEntryItemWidget = (self.parent.order_order_entries_listWidget
                                                 .itemWidget(selected_order_entry))
            order_entry_id = self.parent.database_manager.get_id_for_table_by_field("order_entry_wraper",
                                                                      "name",
                                                                      order_name)[0][0]
            

            # Eliminando la entrade de la orden de la base de datos
            self.parent.database_manager.remove_record_from_table_by_field("order",
                                                                           "idorder",
                                                                           order_id)

            # Eliminando la entrada de la orden de la QListWidget
            self.parent.order_order_entries_listWidget.takeItem(self.parent
                                                         .order_order_entries_listWidget
                                                         .row(selected_order_entry))

    def load_orders_from_database(self):
        alldata = self.parent.database_manager.get_all_data_from_table("order")

        for entry in alldata:
            self.add_order_to_list(Order(entry[1], entry[2], entry[3]))

    def load_order_entries_from_database(self, order: OrderListItem):
        order_id = self.get_order_id(order.order.name)
        data = self.parent.database_manager.get_record_by_field("order_entry_wraper",
                                                                "order_idorder",
                                                                order_id)
        for entry in data:
            product_data = self.parent.database_manager.get_record_by_field("product",
                                                                            "idproduct",
                                                                            entry[3])
            product = Product.deserialize(product_data[0])
            order_entry_wraper = OrderEntryWrapper(product, entry[1])

            self.add_order_entry_to_list(order_entry_wraper)

    def get_order_id(self, order_name: str):
        return self.parent.database_manager.get_id_for_table_by_field("order",
                                                                      "name",
                                                                      order_name)[0][0]

    def add_order_to_list(self, order: Order):
        # Crear el widget personalizado
        order_widget = OrderListItem(order)

        # Crear un QListWidgetItem para envolver el widget
        list_item = QListWidgetItem(self.parent.order_orders_listWidget)

        # Ajustar el tamaño del item al tamaño del widget
        list_item.setSizeHint(order_widget.sizeHint())

        # Agregar el widget al QListWidget
        self.parent.order_orders_listWidget.setItemWidget(list_item, order_widget)

    def add_order_entry_to_list(self, order_entry: OrderEntryWrapper):
        # Crear el widget personalizado
        order_entry_widget = OrderEntryItemWidget(order_entry)

        # Crear un QListWidgetItem para envolver el widget
        list_item = QListWidgetItem(self.parent.order_order_entries_listWidget)

        # Ajustar el tamaño del item al tamaño del widget
        list_item.setSizeHint(order_entry_widget.sizeHint())

        # Agregar el widget al QListWidget
        self.parent.order_order_entries_listWidget.setItemWidget(list_item, order_entry_widget)

    def tab_changed(self, index: int):
        if self.parent.tabs.indexOf(self.parent.ordenesTab) == index:
            self.parent.order_orders_listWidget.clear()
            self.load_orders_from_database()
