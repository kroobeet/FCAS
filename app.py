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

    def connect_to_db(self):
        """Установка соединения с PostgreSQL"""
        try:
            conn = psycopg2.connect(
                dbname="fcas",
                user="postgres",
                password="postgres",
                host="localhost"
            )
            return conn
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться к БД:\n{str(e)}")
            sys.exit(1)

    def setup_franchise_tab(self):
        """Настройка вкладки франшиз"""
        layout = QVBoxLayout()
        self.franchise_tab.setLayout(layout)

        # Форма для добавления/редактирования
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        form_layout.addLayout(left_form)

        self.franchise_name = QLineEdit()
        left_form.addWidget(QLabel("Название франшизы:"))
        left_form.addWidget(self.franchise_name)

        self.franchise_parent = QComboBox()
        self.franchise_parent.addItem("Нет родительской", None)
        left_form.addWidget(QLabel("Родительская франшиза:"))
        left_form.addWidget(self.franchise_parent)

        self.franchise_address = QLineEdit()
        left_form.addWidget(QLabel("Адрес:"))
        left_form.addWidget(self.franchise_address)

        # Правая часть формы
        right_form = QVBoxLayout()
        form_layout.addLayout(right_form)

        self.franchise_phone = QLineEdit()
        right_form.addWidget(QLabel("Контактный телефон:"))
        right_form.addWidget(self.franchise_phone)

        self.franchise_email = QLineEdit()
        right_form.addWidget(QLabel("Email:"))
        right_form.addWidget(self.franchise_email)

        self.franchise_active = QCheckBox("Активна")
        self.franchise_active.setChecked(True)
        right_form.addWidget(self.franchise_active)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.add_franchise_btn = QPushButton("Добавить")
        self.add_franchise_btn.clicked.connect(self.add_franchise)
        buttons_layout.addWidget(self.add_franchise_btn)

        self.update_franchise_btn = QPushButton("Обновить")
        self.update_franchise_btn.setEnabled(False)
        self.update_franchise_btn.clicked.connect(self.update_franchise)
        buttons_layout.addWidget(self.update_franchise_btn)

        self.delete_franchise_btn = QPushButton("Удалить")
        self.delete_franchise_btn.setEnabled(False)
        self.delete_franchise_btn.clicked.connect(self.delete_franchise)
        buttons_layout.addWidget(self.delete_franchise_btn)

        self.clear_franchise_btn = QPushButton("Очистить")
        self.clear_franchise_btn.clicked.connect(self.clear_franchise_form)
        buttons_layout.addWidget(self.clear_franchise_btn)

        # Таблица с франшизами
        self.franchise_table = QTableWidget()
        self.franchise_table.setColumnCount(5)
        self.franchise_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Родитель", "Телефон", "Активна"]
        )
        self.franchise_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.franchise_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.franchise_table.cellClicked.connect(self.franchise_table_click)
        layout.addWidget(self.franchise_table)