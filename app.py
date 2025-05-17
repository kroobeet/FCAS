import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt


class FranchiseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FCAS")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к БД
        self.db_connection = self.connect_to_db()

        # Главный виджет
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Основной Layout
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Создаем вкладки
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Вкладка для франшиз
        self.franchise_tab = QWidget()
        self.tabs.addTab(self.franchise_tab, "Франшизы")
        self.setup_franchise_tab()

        # Вкладка для локаций
        self.location_tab = QWidget()
        self.tabs.addTab(self.location_tab, "Локации")
        self.setup_location_tab()

        # Загружаем начальные данные
        self.load_franchises()
        self.load_locations()