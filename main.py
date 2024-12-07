import sys
from PyQt6.QtWidgets import QApplication
from window import Window


# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()  # Instanciamos la ventana principal
    win.show()  # Mostramos la ventana
    sys.exit(app.exec())  # Ejecutamos la aplicación
