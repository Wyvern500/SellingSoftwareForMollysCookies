from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem, QFileDialog, QWidget, QLabel, QHBoxLayout, QVBoxLayout

from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent

from simple_manager import AbstractTabManager
import error_utils


class AddProductManager(AbstractTabManager):

    def __init__(self, parent):
        from window import Window
        self.parent: Window = parent

        self.parent.add_searchImageButton.clicked.connect(self.open_image)

        self.image_path = None

        # Habilitar arrastrar y soltar en add_labelDropImage
        self.parent.add_labelDropImage.setAcceptDrops(True)
        self.parent.add_labelDropImage.dragEnterEvent = self.drag_enter_event
        self.parent.add_labelDropImage.dropEvent = self.drop_event
        

        # Conectar el botón "Guardar Cambios"
        self.parent.add_saveChangesButton.clicked.connect(self.save_changes)

    def drag_enter_event(self, event: QDragEnterEvent):
        """Permitir que se arrastre un archivo válido al widget."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        """Manejar el archivo soltado y mostrarlo en el área de vista previa."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.display_image(file_path)
                break

    def open_image(self):
        """Abrir un cuadro de diálogo para seleccionar una imagen."""
        file_dialog = QFileDialog(self.parent)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.display_image(file_path)

    def display_image(self, file_path):
        """Mostrar una imagen en el área de vista previa."""
        self.image_path = file_path
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.parent.add_labelImagePreview.size(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
            self.parent.add_labelImagePreview.setPixmap(scaled_pixmap)
            self.parent.add_labelImagePreview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Guardar la ruta de la imagen en un atributo para su posterior uso
            self.parent.current_image_path = file_path

    def save_changes(self):
        product_name = self.parent.add_lineEditProductName.text().strip()
        
        data = self.parent.database_manager.get_records_by_field("product", "name", product_name)
        
        if len(data) == 0:
            
            # Leer los datos de los widgets
            product_price = self.parent.add_lineEditPrice.text().strip()
            product_description = self.parent.add_textEditDescription.toPlainText().strip()
            image_pixmap = self.parent.add_labelImagePreview.pixmap()

            # Validar que todos los campos están completos
            if not product_name or not product_price or not image_pixmap or not error_utils.isfloat(product_price):
                print("Por favor, completa todos los campos antes de guardar.")
                return

            # Crear un nuevo QListWidgetItem
            item = QListWidgetItem(self.parent.crear_items_listWidget)

            # Crear un widget personalizado para el producto
            product = Product(product_name, float(product_price), product_description,
                            self.image_path)
            custom_widget = ProductItemWidget(product)
            item.setSizeHint(custom_widget.sizeHint())

            # Agregar el widget personalizado al QListWidget
            self.parent.crear_items_listWidget.setItemWidget(item, custom_widget)

            # Agregar el producto a la base de datos
            self.parent.database_manager.insert_data("product", product.serialize())

            # Resetear los campos
            self.parent.add_lineEditProductName.clear()
            self.parent.add_lineEditPrice.clear()
            self.parent.add_textEditDescription.clear()
            self.parent.add_labelImagePreview.clear()
            print("Producto guardado y agregado a la lista.")
        else:
            # Leer los datos de los widgets
            product_price = self.parent.add_lineEditPrice.text().strip()
            product_description = self.parent.add_textEditDescription.toPlainText().strip()
            image_pixmap = self.parent.add_labelImagePreview.pixmap()
            
            # Validar que todos los campos están completos
            if not product_name or not product_price or not image_pixmap:
                print("Por favor, completa todos los campos antes de guardar.")
                return
            
            self.parent.database_manager.update_record_by_id("product", {"name": product_name, "price": float(product_price), "description": product_description, "image_path": self.image_path}, 
                                                             {"idproduct": data[0][0]})


def deserialize(data):
    if type(data) is dict:
        return Product(data["name"], data["price"], data["description"], data["image_path"])
    elif type(data) is tuple:
        return Product(data[1], data[2], data[3], data[4])


class Product:

    def __init__(self, name: str, price: float, description: str, image_path: str):
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path

    def serialize(self):
        return {"name": self.name, "price": self.price, "description": self.description
            , "image_path": self.image_path}


class ProductItemWidget(QWidget):
    def __init__(self, product: Product, parent=None):
        super().__init__(parent)

        self.product: Product = product

        # Crear QLabel para la imagen
        self.image_label = QLabel()
        pixmap = QPixmap(product.image_path)

        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen desde {product.image_path}")
        else:
            # Escalar la imagen a un tamaño fijo (por ejemplo, 50x50)
            self.image_label.setPixmap(pixmap.scaled(50, 50))

        self.image_label.setFixedSize(50, 50)  # Fija el tamaño para evitar deformaciones

        # Crear QLabel para el nombre del producto
        self.name_label = QLabel(product.name)
        self.name_label.setStyleSheet("background-color: transparent; color: black; font-weight: bold;")

        # Crear QLabel para el precio del producto
        self.price_label = QLabel(f"${product.price:.2f}")
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
