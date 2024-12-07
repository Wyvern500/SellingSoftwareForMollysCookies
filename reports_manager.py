import matplotlib.pyplot as plt


class ReportsManager:

    def __init__(self, parent):
        from main import Window
        self.parent: Window = parent

        self.parent.reportes_mostrar_info.pressed.connect(self.show_info)

    def show_info(self):
        print(self.parent.reportes_calendario.selectedDate())
