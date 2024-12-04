from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem, QTableWidget, QTableWidgetItem, QFileDialog, QPushButton

from Product.create_order_manager import CustomWidget
from gui import Ui_MainWindow
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent


class AddProductManager:

    def __init__(self, parent):
        from window import Window
        self.parent: Window = parent

        self.load_items_from_database()

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
        # Leer los datos de los widgets
        product_name = self.parent.add_lineEditProductName.text().strip()
        product_price = self.parent.add_lineEditPrice.text().strip()
        product_description = self.parent.add_textEditDescription.toPlainText().strip()
        image_pixmap = self.parent.add_labelImagePreview.pixmap()

        # Validar que todos los campos están completos
        if not product_name or not product_price or not image_pixmap:
            print("Por favor, completa todos los campos antes de guardar.")
            return

        # Crear un nuevo QListWidgetItem
        item = QListWidgetItem(self.parent.crear_items_listWidget)

        # Crear un widget personalizado para el producto
        custom_widget = CustomWidget(self.image_path, product_name, float(product_price), product_description)
        item.setSizeHint(custom_widget.sizeHint())

        # Agregar el widget personalizado al QListWidget
        self.parent.crear_items_listWidget.setItemWidget(item, custom_widget)

        # Resetear los campos
        self.parent.add_lineEditProductName.clear()
        self.parent.add_lineEditPrice.clear()
        self.parent.add_textEditDescription.clear()
        self.parent.add_labelImagePreview.clear()
        print("Producto guardado y agregado a la lista.")


    def load_items_from_database(self):
        pass



