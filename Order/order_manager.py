from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget, QListWidgetItem, QHBoxLayout

from Order.create_order_manager import OrderEntryWrapper
from Order.order_widgets import OrderListItem, OrderEntryItemWidget
from simple_manager import AbstractTabManager
import Product.add_product_manager as Product
from Order.create_order_manager import Order


class OrderManager(AbstractTabManager):

    def __init__(self, parent):
        super().__init__(parent)

        self.current_order: OrderListItem = None

        self.load_orders_from_database()

        self.parent.order_orders_listWidget.itemDoubleClicked.connect(self.on_order_double_click)
        self.parent.order_order_entries_listWidget.itemDoubleClicked.connect(self.on_order_entry_double_click)

        self.parent.order_delete_order_button.pressed.connect(self.on_delete_order)
        self.parent.order_delete_order_entry_button.pressed.connect(self.on_delete_order_entry)
        
        self.parent.order_search_order_lineEdit.textChanged.connect(self.search_orders)
        self.parent.order_search_order_entry_lineEdit.textChanged.connect(self.search_order_entries)

    def search_orders(self):
        text = self.parent.order_search_order_lineEdit.text().lower()
        for i in range(self.parent.order_orders_listWidget.count()):
            item = self.parent.order_orders_listWidget.item(i)
            widget: OrderListItem = self.parent.order_orders_listWidget.itemWidget(item)
            
            # Mostrar u ocultar ítems según la coincidencia
            if text in widget.order.name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def search_order_entries(self):
        text = self.parent.order_search_order_entry_lineEdit.text().lower()
        for i in range(self.parent.order_order_entries_listWidget.count()):
            item = self.parent.order_order_entries_listWidget.item(i)
            widget: OrderEntryItemWidget = self.parent.order_order_entries_listWidget.itemWidget(item)
            
            # Mostrar u ocultar ítems según la coincidencia
            if text in widget.product.name.lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def on_order_double_click(self, item: QListWidgetItem):
        self.parent.order_order_entries_listWidget.clear()
        self.load_order_entries_from_database(self.parent.order_orders_listWidget
                                              .itemWidget(item))
        self.current_order = self.parent.order_orders_listWidget.itemWidget(item)

        self.set_total()

    def on_order_entry_double_click(self, item: QListWidgetItem):
        order_entry = self.parent.order_order_entries_listWidget.itemWidget(item)

        self.parent.order_description_label.setText(order_entry.product.description)

    def set_total(self):
        total = 0

        order_id = self.get_order_id(self.current_order.order.name)
        data = self.parent.database_manager.get_records_by_field("order_entry_wraper",
                                                                 "order_idorder",
                                                                 order_id)
        for order_entry in data:
            total += order_entry[2]

        self.parent.order_total_label.setText(f"Total a pagar: {total}")

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
            order_entry: OrderEntryItemWidget = (self.parent.order_order_entries_listWidget
                                                 .itemWidget(selected_order_entry))

            order_id = self.get_order_id(self.current_order.order.name)
            product_id = self.parent.database_manager.get_id_for_table_by_field("product",
                                                                                "name",
                                                                                order_entry.product.name)[0][0]
            order_entry_id = self.parent.database_manager.get_id_for_table_by_fields("order_entry_wraper",
                                                                                     {"product_idproduct": product_id,
                                                                                      "order_idorder": order_id},
                                                                                     id_name="order_product_wraper")[0][0]
            # Eliminando la entrade de la orden de la base de datos
            self.parent.database_manager.remove_record_from_table_by_field("order_entry_wraper",
                                                                           "idorder_product_wraper",
                                                                           order_entry_id)
            # Eliminando la entrada de la orden de la QListWidget
            self.parent.order_order_entries_listWidget.takeItem(self.parent
                                                                .order_order_entries_listWidget
                                                                .row(selected_order_entry))

        self.set_total()

    def load_orders_from_database(self):
        alldata = self.parent.database_manager.get_all_data_from_table("order")

        for entry in alldata:
            self.add_order_to_list(Order(entry[1], entry[2], entry[3]))

    def load_order_entries_from_database(self, order: OrderListItem):
        order_id = self.get_order_id(order.order.name)
        data = self.parent.database_manager.get_records_by_field("order_entry_wraper",
                                                                 "order_idorder",
                                                                 order_id)
        for entry in data:
            product_data = self.parent.database_manager.get_records_by_field("product",
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
        order_entry_widget.event.add_listener(self.on_amount_changed)

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

    def on_amount_changed(self, data):
        if data["name"] == "editing_finished":
            order_id = self.get_order_id(self.current_order.order.name)

            order_entry: OrderEntryItemWidget = data["sender"]

            product_id = self.parent.database_manager.get_records_by_field("product",
                                                                           "name",
                                                                           order_entry
                                                                           .product
                                                                           .name)[0][0]

            print(f"Order id: {order_id} Product Id: {product_id}")

            new_amount = int(order_entry.quantity_line_edit.text())
            product_price = order_entry.product.price

            order_entry.total_label.setText(f"Total: ${new_amount * product_price}")

            print(f"New Amount: {new_amount} Product Price: {product_price}")

            self.parent.database_manager.update_record_by_id("order_entry_wraper",
                                                             {"subtotal": new_amount * product_price,
                                                              "amount": new_amount},
                                                             {"product_idproduct": product_id,
                                                              "order_idorder": order_id})

            print(f"Order Entries: {self.parent.database_manager.get_records_by_fields('order_entry_wraper', {'product_idproduct': product_id, 'order_idorder': order_id})}")

            self.set_total()
