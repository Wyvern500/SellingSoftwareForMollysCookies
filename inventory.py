from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidgetItem, QFileDialog
from PyQt6.QtGui import QPixmap


class InventoryManager:

    def __init__(self, parent):
        from main import Window
        self.parent: Window = parent

        self.add_style()

        # Coneccting signals
        self.parent.inv_crear_ingrediente.pressed.connect(self.create_ingredient)
        self.parent.inv_elegir_imagen_button.pressed.connect(self.load_product_image)

        self.image_path = None

        self.load_items_from_database()

    def load_items_from_database(self):
        data = self.parent.database_manager.get_all_data_from_table("ingredient")
        for entry in data:
            item = QListWidgetItem(self.parent.inv_products_list_widget)  # Crear un QListWidgetItem
            widget = ProductItemWidget(
                Ingredient(entry[1], entry[2], entry[3], entry[4], entry[6], entry[5])
            )

            item.setSizeHint(widget.sizeHint())  # Ajustar el tamaño del widget
            self.parent.inv_products_list_widget.addItem(item)  # Agregar el item al QListWidget
            self.parent.inv_products_list_widget.setItemWidget(item, widget)  # Asignar el widget al item

    def add_style(self):
        self.parent.inv_products_list_widget.setStyleSheet("""
            QListWidget {
                background-color: white;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid gray;
                border-radius: 3px;
                padding: 5px;
                margin: 1px;  /* Espaciado entre items */
            }
            QListWidget::item:selected {
                background-color: lightblue;  /* Color de fondo al seleccionar */
                border: 1px solid blue;
            }
        """)

    def create_ingredient(self):
        name: str = self.parent.inv_name_line_edit.text()
        amount: int = self.parent.inv_cantidad_spin_box.value()
        #expiration_date: str = self.parent.inv_caducidad_date_edit.dateTime().toString("dd/MM/yyyy")
        cost: float = self.parent.inv_precio_double_spin_box.value()
        description: str = self.parent.inv_descripcion_item.toPlainText()
        image_path: str = self.image_path
        product_type: str = self.parent.inv_tipo_producto_combo_box.currentText()

        ingredient: Ingredient = Ingredient(name, amount, cost, description, image_path, product_type)

        item = QListWidgetItem(self.parent.inv_products_list_widget)  # Crear un QListWidgetItem
        widget = ProductItemWidget(ingredient)

        item.setSizeHint(widget.sizeHint())  # Ajustar el tamaño del widget
        self.parent.inv_products_list_widget.addItem(item)  # Agregar el item al QListWidget
        self.parent.inv_products_list_widget.setItemWidget(item, widget)  # Asignar el widget al item

        self.parent.database_manager.insert_data("ingredient", {"name": name, "amount": amount, "price": cost,
                                     "description":description, "product_type":product_type, "image_path": image_path} )

        print(ingredient)

    def load_product_image(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if dialog.exec():
            file_name = dialog.selectedFiles()
            self.set_ingredient_image(file_name[0])

    def set_ingredient_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(image_path)
        self.parent.inv_imagen_ingrediente.setPixmap(pixmap)

class Ingredient:

    def __init__(self, name: str, amount: int, price: float, description: str, image_path: str,
                 product_type: str):
        self.name = name
        self.amount = amount
        self.price = price
        self.description = description
        self.product_type = product_type
        self.image_path = image_path

    def __str__(self):
        return f"Name: {self.name} Amount: {self.amount} Price: {self.price} Description: {self.description} Product Type: {self.product_type} Image Path: {self.image_path}"


class ProductItemWidget(QWidget):

    def __init__(self, ingredient, parent=None):
        super().__init__(parent)

        self.ingredient = ingredient

        self.setToolTip(self.ingredient.description)

        # Agregando estilo a los items
        self.add_style()

        # Layout principal
        layout = QHBoxLayout(self)

        # Imagen a la izquierda
        self.image_label = QLabel(self)

        image = QPixmap(self.ingredient.image_path)
        if image.isNull():
            image = QPixmap("imagenes/image_not_found.png")

        self.image_label.setPixmap(image.scaled(64, 64))
        layout.addWidget(self.image_label)

        # Ajustar el espacio ocupado por la imagen
        layout.setStretch(0, 1)  # Imagen toma menos espacio

        # Detalles a la derecha de la imagen
        details_layout = QVBoxLayout()

        self.name_label = QLabel(f"Producto: {self.ingredient.name}")
        self.quantity_label = QLabel(f"Cantidad: {self.ingredient.amount}")
        self.price_label = QLabel(f"Precio: ${self.ingredient.price}")
        self.unity_type = QLabel(f"Tipo de producto: {self.ingredient.product_type}")
        #self.total_label = QLabel(f"Total: ${price * quantity:.2f}")

        details_layout.addWidget(self.name_label)
        details_layout.addWidget(self.quantity_label)
        details_layout.addWidget(self.price_label)
        details_layout.addWidget(self.unity_type)
        #details_layout.addWidget(self.total_label)

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