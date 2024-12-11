from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit

import utils
from Product.add_product_manager import Product


class Event:
    def __init__(self):
        self.listeners = []  # Lista para almacenar los escuchadores

    def add_listener(self, listener):
        """Agrega un escuchador (función o método)."""
        if callable(listener):
            self.listeners.append(listener)

    def remove_listener(self, listener):
        """Elimina un escuchador."""
        if listener in self.listeners:
            self.listeners.remove(listener)

    def emit(self, *args, **kwargs):
        """Lanza el evento y notifica a todos los escuchadores."""
        for listener in self.listeners:
            listener(*args, **kwargs)

class OrderEntryWrapper:

    def __init__(self, product: Product, amount: int):
        self.product = product
        self.amount = amount


class Order:

    def __init__(self, name: str, total: float, date_time: str = utils.get_formatted_current_datetime()):
        self.name: str = name
        self.total: float = total
        self.datetime: str = date_time
        self.order_entries: list[OrderEntryWrapper] = []

    def add_order_entry(self, order_entry: OrderEntryWrapper):
        self.order_entries.append(order_entry)

    def serialize(self):
        return {"name": f'{self.name}', "total": self.total, "date": f'{self.datetime}'}

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

        self.event = Event()
        self.amount_changed_event = Event()

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
        hbox_container = QWidget()
        hbox_layout = QHBoxLayout()
        self.quantity_line_edit: QLineEdit = QLineEdit(f"{order_entry.amount}")
        self.quantity_line_edit.editingFinished.connect(lambda: self.event.emit({"name": "editing_finished",
                                                                                 "sender": self}))
        hbox_layout.addWidget(QLabel("Cantidad: "))
        hbox_layout.addWidget(self.quantity_line_edit)
        self.total_label = QLabel(f"Total: ${self.product.price * order_entry.amount}")

        hbox_container.setLayout(hbox_layout)

        details_layout.addWidget(self.name_label)
        details_layout.addWidget(hbox_container)
        details_layout.addWidget(self.total_label)

        layout.addLayout(details_layout)
        layout.setStretch(1, 4)  # Detalles toman más espacio

    def setAmount(self, amount: int):
        self.quantity_line_edit.setText(str(amount))
        self.order_entry.amount = amount
        self.total_label.setText(f"Total: ${self.product.price * self.order_entry.amount}")
        self.amount_changed_event.emit({"name": "amount_changed", "sender": self})
        

    def add_style(self):
        # Aplicar un borde al widget
        self.setStyleSheet("""
                QWidget{
                    background-color: white;
                    padding: 3px;       /* Espaciado interno */
                }
                """)