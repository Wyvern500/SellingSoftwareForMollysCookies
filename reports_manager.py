import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import datetime
import pandas

class ReportsManager:

    def __init__(self, parent):
        from main import Window
        self.parent: Window = parent

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.parent.reportes_graphic_container.addWidget(self.canvas)
        
        self.parent.reportes_mostrar_info.pressed.connect(self.show_info)

    def show_info(self):
        selected_date = self.parent.reportes_calendario.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        
        print(f"Orders: {self.parent.database_manager.get_all_data_from_table('order')}")
        
        availbale_orders = self.parent.database_manager.get_records_by_fields("order", 
                                                                              {"date": f" > '{date_str} 00:00:00'"}, 
                                                                              "date", 
                                                                              literal=True)
        print(f"Available Orders: {availbale_orders}")
        
        first_date = availbale_orders[0][3]
        last_date = availbale_orders[len(availbale_orders) - 1][3]
        
        print(f"First date: {first_date} Last date: {last_date}")
        
        first_date_datetime = datetime.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
        last_date_datetime = datetime.datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
        
        days = []
        
        print(f"Days between: {pandas.date_range(first_date_datetime,last_date_datetime - datetime.timedelta(days = 1), freq='d')}")
        
        print(f"Days: {(first_date_datetime - last_date_datetime).days}")
        
        print(self.parent.reportes_calendario.selectedDate())
        
        """Generar datos ficticios de ventas y graficarlos según la fecha seleccionada."""
        
        # Generar datos ficticios de ventas (puedes reemplazar esto con datos reales)
        days_in_month = selected_date.daysInMonth()
        sales_data = [random.randint(50, 200) for _ in range(days_in_month)]
        days = list(range(1, days_in_month + 1))

        # Actualizar la etiqueta de información
        #self.info_label.setText(f"Ventas de galletas para el mes: {selected_date.toString('MMMM yyyy')}")

        # Limpiar y actualizar la gráfica
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(days, sales_data, marker="o", linestyle="-", color="blue")
        ax.set_title(f"Ventas de Galletas - {selected_date.toString('MMMM yyyy')}")
        ax.set_xlabel("Día del mes")
        ax.set_ylabel("Ventas (unidades)")
        ax.grid(True)

        # Actualizar el lienzo
        self.canvas.draw()
