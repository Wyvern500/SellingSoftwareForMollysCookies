import sys

from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QWidget, QLabel, QSpinBox, QHBoxLayout, QListWidgetItem
)

from archivo import Ui_MainWindow


# Creamos una clase que será el contenedor personalizado
class CustomWidget(QWidget):
    def _init_(self, label_text1, label_text2, parent=None):
        super()._init_(parent)

        # Creación de los widgets hijos
        label1 = QLabel(label_text1)
        spinbox = QSpinBox()
        label2 = QLabel(label_text2)

        # Layout horizontal para los widgets
        layout = QHBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(spinbox)
        layout.addWidget(label2)

        # Asignamos el layout al widget
        self.setLayout(layout)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        for i in range(10):
            item = QListWidgetItem(self.items)

            # Creación del widget personalizado
            custom_widget = CustomWidget(f"Item {i}", "Info")

            # Asignamos el tamaño del widget al item de la lista
            item.setSizeHint(custom_widget.sizeHint())

            # Agregamos el widget personalizado a la lista
            self.items.setItemWidget(item, custom_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())