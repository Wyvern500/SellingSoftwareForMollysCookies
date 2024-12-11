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

        # Inicializamos la lista de productos seleccionados
        self.selected_products = {}

        self.database_manager = DataBaseManager()
        self.create_order_manager = CreateOrderManager(self)
        self.order_manager = OrderManager(self)
        self.add_product_manager = AddProductManager(self)
        # Esta clase la usare para manejar el inventario
        self.inventoryManager = InventoryManager(self)
        self.reportsManager = ReportsManager(self)
