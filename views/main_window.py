from PySide6.QtWidgets import QMainWindow, QTabWidget
from models.database import Database
from views.tabs.franchise import FranchiseTab
from views.tabs.location import LocationTab
from views.tabs.device import DeviceTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏢 FCAS - Franchise Control and Administration System")
        self.setGeometry(100, 100, 1200, 900)

        # Инициализация базы данных
        self.db = Database()
        if not self.db.connect("fcas", "postgres", "postgres", "localhost"):
            raise Exception("Не удалось подключиться к базе данных")

        # Создание вкладок
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # Современный стиль вкладок
        self.setCentralWidget(self.tabs)

        # Добавление вкладки франшиз
        self.franchise_tab = FranchiseTab(self.db)
        self.tabs.addTab(self.franchise_tab, "Франшизы")

        # Добавление вкладки локаций
        self.location_tab = LocationTab(self.db)
        self.tabs.addTab(self.location_tab, "Локации")

        # Добавление вкладки устройств
        self.device_tab = DeviceTab(self.db)
        self.tabs.addTab(self.device_tab, "Оборудование")

        # Добавление статус бара
        self.statusBar().showMessage("Готово", 3000)

        # Загрузка данных
        self.franchise_tab.load_data()
        self.location_tab.load_data()
        self.device_tab.load_data()

        # Подключаем сигналы
        self.franchise_tab.controller.data_changed.connect(self.refresh_all_tabs)
        self.location_tab.controller.data_changed.connect(self.refresh_all_tabs)
        self.device_tab.controller.data_changed.connect(self.refresh_all_tabs)

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

    def refresh_all_tabs(self):
        """Обновляет данные во всех вкладках"""
        self.franchise_tab.load_data()
        self.location_tab.load_data()
        self.device_tab.load_data()

