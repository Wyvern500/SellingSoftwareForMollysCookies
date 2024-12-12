from PyQt6.QtWidgets import QMessageBox


def show_error_message(message: str):
    # Crear una instancia de QMessageBox
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)  # Icono de error
    msg_box.setWindowTitle("Error")        # Título del cuadro de diálogo
    msg_box.setText(message)               # Mensaje a mostrar
    msg_box.exec()