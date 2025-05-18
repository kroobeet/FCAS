from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from controllers.franchise import FranchiseController


class FranchiseTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db,
        self.controller = FranchiseController(db, self)
        self.current_franchise_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

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
        self.add_franchise_btn.clicked.connect(self.controller.add_franchise)
        buttons_layout.addWidget(self.add_franchise_btn)

        self.update_franchise_btn = QPushButton("Обновить")
        self.update_franchise_btn.clicked.connect(self.controller.update_franchise)
        buttons_layout.addWidget(self.update_franchise_btn)

        self.delete_franchise_btn = QPushButton("Удалить")
        self.delete_franchise_btn.clicked.connect(self.controller.delete_franchise)
        buttons_layout.addWidget(self.delete_franchise_btn)

        self.clear_franchise_btn = QPushButton("Очистить")
        self.clear_franchise_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_franchise_btn)

        # Таблица с франшизами
        self.franchise_table = QTableWidget()
        self.franchise_table.setColumnCount(5)
        self.franchise_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Родитель", "Телефон", "Активна"]
        )
        self.franchise_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.franchise_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.franchise_table.cellClicked.connect(self.on_table_click)
        layout.addWidget(self.franchise_table)

    def load_data(self):
        self.controller.load_franchises()
        self.controller.load_parent_franchises()

    def populate_table(self, franchises):
        """Заполнение таблицы данными"""
        self.franchise_table.setRowCount(0)
        for row_num, row_data in enumerate(franchises):
            self.franchise_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                self.franchise_table.setItem(row_num, col_num, item)

    def populate_parent_combo(self, parents):
        """Заполнение комбобокса родительскими франшизами"""
        self.franchise_parent.clear()
        self.franchise_parent.addItem("Нет родительской", None)
        for franchise_id, name in parents:
            self.franchise_parent.addItem(name, franchise_id)

    def on_table_click(self, row, column):
        """Обработка клика по таблице"""
        franchise_id = int(self.franchise_table.item(row, 0).text())
        franchise_name = self.franchise_table.item(row, 1).text()
        parent_name = self.franchise_table.item(row, 2).text()
        phone = self.franchise_table.item(row, 3).text()
        active = self.franchise_table.item(row, 4).text() == "True"

        self.current_franchise_id = franchise_id
        self.franchise_name.setText(franchise_name)

        # Устанавливаем родительскую франшизу
        parent_index = 0
        if parent_name:
            for i in range(1, self.franchise_parent.count()):
                if self.franchise_parent.itemText(i) == parent_name:
                    parent_index = i
                    break

        self.franchise_parent.setCurrentIndex(parent_index)

        self.franchise_phone.setText(phone)
        self.franchise_active.setChecked(active)

        # Получаем остальные данные
        self.controller.load_franchise_details(franchise_id)

        # Активируем кнопки
        self.update_franchise_btn.setEnabled(True)
        self.delete_franchise_btn.setEnabled(True)
        self.add_franchise_btn.setEnabled(False)

    def show_details(self, address, email):
        """Отображение дополнительных деталей франшизы"""
        self.franchise_address.setText(address if address else "")
        self.franchise_email.setText(email if email else "")

    def clear_form(self):
        """Очистка формы"""
        self.franchise_name.clear()
        self.franchise_parent.setCurrentIndex(0)
        self.franchise_address.clear()
        self.franchise_phone.clear()
        self.franchise_email.clear()
        self.franchise_active.setChecked(True)

        self.current_franchise_id = None
        self.update_franchise_btn.setEnabled(False)
        self.delete_franchise_btn.setEnabled(False)
        self.add_franchise_btn.setEnabled(True)

    def show_message(self, title, message, is_error=False):
        """Показать сообщение"""
        if is_error:
            QMessageBox.critical(self, title, message)
        else:
            QMessageBox.information(self, title, message)