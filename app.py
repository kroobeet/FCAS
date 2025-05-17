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

    def setup_location_tab(self):
        """Настройка вкладки локаций"""
        layout = QVBoxLayout()
        self.location_tab.setLayout(layout)

        # Форма для добавления/редактирования
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        form_layout.addLayout(left_form)

        self.location_franchise = QComboBox()
        left_form.addWidget(QLabel("Франшиза:"))
        left_form.addWidget(self.location_franchise)

        self.location_name = QLineEdit()
        left_form.addWidget(QLabel("Название локации:"))
        left_form.addWidget(self.location_name)

        # Правая часть формы
        right_form = QVBoxLayout()
        form_layout.addLayout(right_form)

        self.location_address = QLineEdit()
        right_form.addWidget(QLabel("Адрес:"))
        right_form.addWidget(self.location_address)

        self.location_room = QLineEdit()
        right_form.addWidget(QLabel("Номер помещения:"))
        right_form.addWidget(self.location_room)

        self.location_active = QCheckBox("Активна")
        self.location_active.setChecked(True)
        right_form.addWidget(self.location_active)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.add_location_btn = QPushButton("Добавить")
        self.add_location_btn.clicked.connect(self.add_location)
        buttons_layout.addWidget(self.add_location_btn)

        self.update_location_btn = QPushButton("Обновить")
        self.update_location_btn.setEnabled(False)
        self.update_location_btn.clicked.connect(self.update_location)
        buttons_layout.addWidget(self.update_location_btn)

        self.delete_location_btn = QPushButton("Удалить")
        self.delete_location_btn.setEnabled(False)
        self.delete_location_btn.clicked.connect(self.delete_location)
        buttons_layout.addWidget(self.delete_location_btn)

        self.clear_location_btn = QPushButton("Очистить")
        self.clear_location_btn.clicked.connect(self.clear_location_form)

        # Таблица с локациями
        self.location_table = QTableWidget()
        self.location_table.setColumnCount(5)
        self.location_table.setHorizontalHeaderLabels(
            ["ID", "Франшиза", "Название", "Адрес", "Активна"]
        )
        self.location_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.location_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.location_table.cellClicked.connect(self.location_table_click)
        layout.addWidget(self.location_table)

    def load_franchises(self):
        """Загрузка списка франшиз из БД"""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT f.franchise_id, f.name, p.name as parent_name,
                           f.contact_phone, f.is_active
                    FROM franchise f 
                    LEFT JOIN franchise p ON f.parent_id = p.franchise_id
                    ORDER BY f.franchise_id
                """)
                franchises = cursor.fetchall()

                # Очищаем таблицу
                self.franchise_table.setRowCount(0)

                # Заполняем таблицу
                for row_num, row_data in enumerate(franchises):
                    self.franchise_table.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data) if data is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                        self.franchise_table.setItem(row_num, col_num, item)

                # Обновляем комбобоксы
                self.franchise_parent.clear()
                self.franchise_parent.addItem("Нет родительской", None)
                self.location_franchise.clear()

                cursor.execute("SELECT franchise_id, name FROM franchise ORDER BY name")
                for franchise_id, name in cursor.fetchall():
                    self.franchise_parent.addItem(name, franchise_id)
                    self.location_franchise.addItem(name, franchise_id)
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке франшиз:\n{str(e)}")