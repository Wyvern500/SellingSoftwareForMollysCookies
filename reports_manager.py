import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
from datetime import datetime
from collections import defaultdict
import pandas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ReportsManager:

    def __init__(self, parent):
        from main import Window
        self.parent: Window = parent

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.parent.reportes_scrollArea.setWidget(self.canvas)
        
        self.parent.reportes_mostrar_info.pressed.connect(self.show_info)

    def get_dates_within_range(self, sdate, edate):
        return [sdate + datetime.timedelta(days=x) for x in range((edate-sdate).days)]

    def show_info(self):
        selected_date = self.parent.reportes_calendario.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        
        availbale_orders = self.parent.database_manager.get_records_by_fields("order", 
                                                                              {"date": f" > '{date_str} 00:00:00'"}, 
                                                                              "date", 
                                                                              literal=True)
        
        # Agrupar ventas por día
        sales_by_date = defaultdict(float)
        
        for _, _, sales, date in availbale_orders:
            # Limpiar comillas alrededor de las fechas si las hay
            date = date.strip("'")
            # Extraer solo la parte de la fecha (YYYY-MM-DD)
            day = date.split()[0]
            # Sumar las ventas por día
            sales_by_date[day] += sales
        
        # Preparar datos para la gráfica
        dates = sorted(sales_by_date.keys())  # Ordenar las fechas
        sales = [sales_by_date[day] for day in dates]
        
        # Limpiar la figura para evitar sobreescribir
        self.figure.clear()
        
        # Crear la gráfica en la figura
        ax = self.figure.add_subplot(111)
        ax.bar(dates, sales, color="skyblue")
        ax.set_title("Ventas por Día", fontsize=12)
        ax.set_xlabel("Días", fontsize=12)
        ax.set_ylabel("Total Ventas", fontsize=12)
        #ax.tick_params(axis="x", rotation=45)

        # Actualizar el canvas
        self.canvas.draw()
        
        """print(f"Orders: {self.parent.database_manager.get_all_data_from_table('order')}")
        
        
        print(f"Available Orders: {availbale_orders}")
        
        first_date = availbale_orders[0][3]
        last_date = availbale_orders[len(availbale_orders) - 1][3]
        
        print(f"First date: {first_date} Last date: {last_date}")
        
        first_date_datetime = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
        last_date_datetime = datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
        
        days = []
        
        print(f"Days between: {self.get_dates_within_range(first_date_datetime, last_date_datetime)}")
        
        print(f"Days: {(first_date_datetime - last_date_datetime).days}")
        
        print(self.parent.reportes_calendario.selectedDate())
        
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
        """
