from PySide6.QtWidgets import QMainWindow, QTabWidget
from models.database import Database
from views.tabs.franchise import FranchiseTab


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

        # Добавление статус бара
        self.statusBar().showMessage("Готово", 3000)

        # Загрузка данных
        self.franchise_tab.load_data()

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)
