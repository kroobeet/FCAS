from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QCheckBox, QMessageBox,
    QGroupBox, QHeaderView
)
from PySide6.QtCore import Qt
from controllers.franchise import FranchiseController


class FranchiseTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.controller = FranchiseController(db, self)
        self.current_franchise_id = None
        self.init_ui()

        # Обработчик изменения размера
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        """Обработчик изменения размера окна"""
        super().resizeEvent(event)
        self.adjust_table_columns()

    def adjust_table_columns(self):
        """Автоматическая настройка ширины столбцов"""
        if self.franchise_table.rowCount() > 0:
            header = self.franchise_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Группа для формы
        form_group = QGroupBox("Данные франшизы")
        form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        main_layout.addWidget(form_group)

        form_layout = QHBoxLayout()
        form_group.setLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        left_form.setSpacing(10)
        form_layout.addLayout(left_form, 1)

        self.franchise_name = QLineEdit()
        self.franchise_name.setPlaceholderText("Введите название франшизы")
        left_form.addWidget(QLabel("Название франшизы:"))
        left_form.addWidget(self.franchise_name)

        self.franchise_parent_label = QLabel("Родительская франшиза:")
        left_form.addWidget(self.franchise_parent_label)

        self.franchise_parent = QComboBox()
        self.franchise_parent.addItem("Нет родительской", None)
        left_form.addWidget(self.franchise_parent)

        self.franchise_address = QLineEdit()
        self.franchise_address.setPlaceholderText("Введите адрес франшизы")
        left_form.addWidget(QLabel("Адрес:"))
        left_form.addWidget(self.franchise_address)

        # Правая часть формы
        right_form = QVBoxLayout()
        right_form.setSpacing(10)
        form_layout.addLayout(right_form, 1)

        self.franchise_phone = QLineEdit()
        self.franchise_phone.setPlaceholderText("Введите контактный телефон")
        right_form.addWidget(QLabel("Контактный телефон:"))
        right_form.addWidget(self.franchise_phone)

        self.franchise_email = QLineEdit()
        self.franchise_email.setPlaceholderText("Введите email")
        right_form.addWidget(QLabel("Email:"))
        right_form.addWidget(self.franchise_email)

        self.franchise_active = QCheckBox("✅ Активна")
        self.franchise_active.setChecked(True)
        right_form.addWidget(self.franchise_active)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        main_layout.addLayout(buttons_layout)

        self.add_franchise_btn = QPushButton("➕ Добавить")
        self.add_franchise_btn.clicked.connect(self.controller.add_franchise)
        buttons_layout.addWidget(self.add_franchise_btn)

        self.update_franchise_btn = QPushButton("🔄 Обновить")
        self.update_franchise_btn.setEnabled(False)
        self.update_franchise_btn.clicked.connect(self.controller.update_franchise)
        buttons_layout.addWidget(self.update_franchise_btn)

        self.delete_franchise_btn = QPushButton("🗑️ Удалить")
        self.delete_franchise_btn.setEnabled(False)
        self.delete_franchise_btn.clicked.connect(self.controller.delete_franchise)
        buttons_layout.addWidget(self.delete_franchise_btn)

        buttons_layout.addStretch(1)

        self.clear_franchise_btn = QPushButton("❌ Очистить")
        self.clear_franchise_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_franchise_btn)

        # Таблица с франшизами
        self.franchise_table = QTableWidget()
        self.franchise_table.setColumnCount(5)
        self.franchise_table.setHorizontalHeaderLabels(
            ["🔖 ID", "🏷️ Название", "👥 Родитель", "📞 Телефон", "✅ Активна"]
        )

        # Настройка таблицы
        self.franchise_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.franchise_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.franchise_table.setAlternatingRowColors(True)
        self.franchise_table.verticalHeader().hide()
        self.franchise_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.franchise_table.horizontalHeader().setHighlightSections(False)
        self.franchise_table.setSortingEnabled(True)
        self.franchise_table.cellClicked.connect(self.on_table_click)

        main_layout.addWidget(self.franchise_table)

    def load_data(self):
        self.controller.load_franchises()
        self.controller.load_parent_franchises()

    def populate_table(self, franchises):
        """Заполнение таблицы данными"""
        # Блокируем обновление таблицы во время заполнения
        self.franchise_table.setUpdatesEnabled(False)

        self.franchise_table.setRowCount(0)
        for row_num, row_data in enumerate(franchises):
            self.franchise_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)

                # Выравнивание текста по центру
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Особое оформление для колонки "Активна"
                if col_num == 4:
                    item.setText("Да" if data == True else "Нет")

                self.franchise_table.setItem(row_num, col_num, item)

        # Настраиваем растягивание столбцов
        header = self.franchise_table.horizontalHeader()

        # Первые два столбца растягиваем по содержимому
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Название

        # Остальные столбцы растягиваем пропорционально
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Родитель
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Телефон
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Активна

        # Включаем обновление и перерисовываем таблицу
        self.franchise_table.setUpdatesEnabled(True)
        self.franchise_table.viewport().update()

    def populate_parent_combo(self, parents):
        self.franchise_parent.clear()
        self.franchise_parent.addItem("Нет родительской", None)
        for franchise_id, name in parents:
            self.franchise_parent.addItem(name, franchise_id)

    def on_table_click(self, row, column):
        franchise_id = int(self.franchise_table.item(row, 0).text())
        franchise_name = self.franchise_table.item(row, 1).text()
        parent_name = self.franchise_table.item(row, 2).text()
        phone = self.franchise_table.item(row, 3).text()
        active = self.franchise_table.item(row, 4).text() == "Да"

        self.current_franchise_id = franchise_id
        self.franchise_name.setText(franchise_name)

        parent_index = 0
        if parent_name:
            for i in range(1, self.franchise_parent.count()):
                if self.franchise_parent.itemText(i) == parent_name:
                    parent_index = i
                    break

        self.franchise_parent.setCurrentIndex(parent_index)
        self.franchise_phone.setText(phone)
        self.franchise_active.setChecked(active)

        self.controller.load_franchise_details(franchise_id)

        self.update_franchise_btn.setEnabled(True)
        self.delete_franchise_btn.setEnabled(True)
        self.add_franchise_btn.setEnabled(False)

    def show_details(self, address, email):
        self.franchise_address.setText(address if address else "")
        self.franchise_email.setText(email if email else "")

    def clear_form(self):
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
        msg = QMessageBox(self)
        if is_error:
            msg.setWindowTitle(f"❌ {title}")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet("QLabel{ color: red; }")
        else:
            msg.setWindowTitle(f"✅ {title}")
            msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.exec()
