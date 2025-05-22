from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QCheckBox, QMessageBox,
    QGroupBox, QHeaderView
)
from PySide6.QtCore import Qt
from controllers.location import LocationController


class LocationTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.controller = LocationController(db, self)
        self.current_location_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Группа для формы
        form_group = QGroupBox("Данные локации")
        form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        main_layout.addWidget(form_group)

        form_layout = QHBoxLayout()
        form_group.setLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        left_form.setSpacing(10)
        form_layout.addLayout(left_form, 1)

        self.location_name = QLineEdit()
        self.location_name.setPlaceholderText("Введите название локации")
        left_form.addWidget(QLabel("Название локации:"))
        left_form.addWidget(self.location_name)

        self.location_franchise_label = QLabel("Франшиза:")
        left_form.addWidget(self.location_franchise_label)

        self.location_franchise = QComboBox()
        left_form.addWidget(self.location_franchise)

        self.location_address = QLineEdit()
        self.location_address.setPlaceholderText("Введите адрес локации")
        left_form.addWidget(QLabel("Адрес:"))
        left_form.addWidget(self.location_address)

        # Правая часть формы
        right_form = QVBoxLayout()
        right_form.setSpacing(10)
        form_layout.addLayout(right_form, 1)

        self.location_room_number = QLineEdit()
        self.location_room_number.setPlaceholderText("Введите номер помещения")
        right_form.addWidget(QLabel("Номер помещения:"))
        right_form.addWidget(self.location_room_number)

        self.location_active = QCheckBox("✅ Активна")
        self.location_active.setChecked(True)
        right_form.addWidget(self.location_active)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        main_layout.addLayout(buttons_layout)

        self.add_location_btn = QPushButton("➕ Добавить")
        self.add_location_btn.clicked.connect(self.controller.add_location)
        buttons_layout.addWidget(self.add_location_btn)

        self.update_location_btn = QPushButton("🔄 Обновить")
        self.update_location_btn.setEnabled(False)
        self.update_location_btn.clicked.connect(self.controller.update_location)
        buttons_layout.addWidget(self.update_location_btn)

        self.delete_location_btn = QPushButton("🗑️ Удалить")
        self.delete_location_btn.setEnabled(False)
        self.delete_location_btn.clicked.connect(self.controller.delete_location)
        buttons_layout.addWidget(self.delete_location_btn)

        buttons_layout.addStretch(1)

        self.clear_location_btn = QPushButton("❌ Очистить")
        self.clear_location_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_location_btn)

        # Таблица с локациями
        self.location_table = QTableWidget()
        self.location_table.setColumnCount(6)
        self.location_table.setHorizontalHeaderLabels(
            ["🔖 ID", "🏷️ Название", "🏢 Франшиза", "📍 Адрес", "🚪 Помещение", "✅ Активна"]
        )

        # Настройка таблицы
        self.location_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.location_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.location_table.setAlternatingRowColors(True)
        self.location_table.verticalHeader().hide()
        self.location_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.location_table.horizontalHeader().setHighlightSections(False)
        self.location_table.setSortingEnabled(True)
        self.location_table.cellClicked.connect(self.on_table_click)

        main_layout.addWidget(self.location_table)

    def load_data(self):
        self.controller.load_locations()
        self.controller.load_franchises_for_locations()

    def populate_table(self, locations):
        self.location_table.setUpdatesEnabled(False)
        self.location_table.setRowCount(0)

        for row_num, row_data in enumerate(locations):
            self.location_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if col_num == 5:  # Колонка "Активна"
                    item.setText("Да" if data is True else "Нет")

                self.location_table.setItem(row_num, col_num, item)

        header = self.location_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Название
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Франшиза
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Адрес
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Помещение
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Активна

        self.location_table.setUpdatesEnabled(True)
        self.location_table.viewport().update()

    def populate_franchise_combo(self, franchises):
        self.location_franchise.clear()
        for franchise_id, name in franchises:
            self.location_franchise.addItem(name, franchise_id)

    def on_table_click(self, row, column):
        location_id = int(self.location_table.item(row, 0).text())
        location_name = self.location_table.item(row, 1).text()
        franchise_name = self.location_table.item(row, 2).text()
        address = self.location_table.item(row, 3).text()
        room_number = self.location_table.item(row, 4).text()
        active = self.location_table.item(row, 5).text() == "Да"

        self.current_location_id = location_id
        self.location_name.setText(location_name)

        # Находим индекс франшизы в комбобоксе
        franchise_index = 0
        for i in range(self.location_franchise.count()):
            if self.location_franchise.itemText(i) == franchise_name:
                franchise_index = i
                break

        self.location_franchise.setCurrentIndex(franchise_index)
        self.location_address.setText(address)
        self.location_room_number.setText(room_number)
        self.location_active.setChecked(active)

        self.controller.load_location_details(location_id)

        self.update_location_btn.setEnabled(True)
        self.delete_location_btn.setEnabled(True)
        self.add_location_btn.setEnabled(False)

    def show_details(self, address, room_number):
        self.location_address.setText(address if address else "")
        self.location_room_number.setText(room_number if room_number else "")

    def clear_form(self):
        self.location_name.clear()
        if self.location_franchise.count() > 0:
            self.location_franchise.setCurrentIndex(0)
        self.location_address.clear()
        self.location_room_number.clear()
        self.location_active.setChecked(True)

        self.current_location_id = None
        self.update_location_btn.setEnabled(False)
        self.delete_location_btn.setEnabled(False)
        self.add_location_btn.setEnabled(True)

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