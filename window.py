from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from gui import Ui_MainWindow
from Product.add_product_manager import AddProductManager
from Order.create_order_manager import CreateOrderManager
from Order.order_manager import OrderManager
from database_manager import DataBaseManager
from inventory import InventoryManager
from reports_manager import ReportsManager


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.crear_orden_orderList_tableWidget.itemChanged.connect(self.onItemChanged)


        # Inicializamos la lista de productos seleccionados
        self.selected_products = {}

        self.database_manager = DataBaseManager()
        self.create_order_manager = CreateOrderManager(self)
        self.order_manager = OrderManager(self)
        self.add_product_manager = AddProductManager(self)
        # Esta clase la usare para manejar el inventario
        self.inventoryManager = InventoryManager(self)
        self.reportsManager = ReportsManager(self)

    def onItemChanged(self, item):
        for itemRow in self.get_rows_for_item(item):

            print(itemRow.text())
        print(f"Widgets: {self.get_rows_for_item(item)}")

    # Extrae las columnas en las que se encuentra un item
    def get_rows_for_item(self, item) -> list[QTableWidgetItem]:
        item_row = self.crear_orden_orderList_tableWidget.row(item)
        return self.get_widgets_in_row(item_row)

    # Función para obtener todos los widgets en una fila específica
    def get_widgets_in_row(self, row) -> list[QTableWidgetItem]:
        widgets = []
        for column in range(self.crear_orden_orderList_tableWidget.columnCount()):
            widget = self.crear_orden_orderList_tableWidget.item(row, column)
            if widget:
                widgets.append(widget)
        return widgets




