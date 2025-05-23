from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QCheckBox, QMessageBox,
    QGroupBox, QHeaderView, QDateEdit, QDoubleSpinBox,
    QTextEdit, QFormLayout
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QPalette, QColor
from controllers.device import DeviceController


class DeviceTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.controller = DeviceController(db, self)
        self.current_device_id = None
        self.locations_count = 0
        self.init_ui()
        self.setup_styles()

    def setup_styles(self):
        # Настройка палитры для календаря
        calendar_palette = QPalette()
        calendar_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        calendar_palette.setColor(QPalette.ColorRole.Base, QColor(53, 53, 53))
        calendar_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(58, 58, 58))
        calendar_palette.setColor(QPalette.ColorRole.Text, QColor(224, 224, 224))
        calendar_palette.setColor(QPalette.ColorRole.Button, QColor(64, 64, 64))
        calendar_palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 224, 224))
        calendar_palette.setColor(QPalette.ColorRole.Highlight, QColor(45, 93, 131))
        calendar_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        # Применяем палитру к виджетам даты
        self.device_purchase_date.setPalette(calendar_palette)
        self.device_warranty_expiry.setPalette(calendar_palette)
        self.device_purchase_price.setPalette(calendar_palette)

        # Получаем доступ к внутреннему календарю и применяем стили
        for date_edit in [self.device_purchase_date, self.device_warranty_expiry]:
            calendar = date_edit.calendarWidget()
            calendar.setPalette(calendar_palette)
            calendar.setStyleSheet("""
                QCalendarWidget QAbstractItemView:enabled {
                    color: #e0e0e0;
                    background-color: #353535;
                    selection-background-color: #2d5d83;
                    selection-color: white;
                }
                QCalendarWidget QToolButton {
                    color: #e0e0e0;
                    background-color: #404040;
                }
            """)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # Форма данных
        self.create_form_group()

        # Кнопки управления
        self.create_buttons_layout()

        # Таблица оборудования
        self.create_table()

    def create_form_group(self):
        form_group = QGroupBox("Данные оборудования")
        main_layout = self.layout()
        main_layout.addWidget(form_group)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(15)
        form_group.setLayout(form_layout)

        # Первый ряд
        self.device_type = QComboBox()
        self.device_franchise = QComboBox()
        self.device_franchise.addItem("Нет франшизы", None)
        self.device_franchise.currentIndexChanged.connect(self.on_franchise_changed)

        row1_layout = QHBoxLayout()
        row1_layout.addWidget(QLabel("Тип:"))
        row1_layout.addWidget(self.device_type)
        row1_layout.addSpacing(15)
        row1_layout.addWidget(QLabel("Франшиза:"))
        row1_layout.addWidget(self.device_franchise)
        form_layout.addRow(row1_layout)

        # Второй ряд - локация с счетчиком
        location_container = QWidget()
        location_layout = QHBoxLayout(location_container)
        location_layout.setContentsMargins(0, 0, 0, 0)

        self.location_label = QLabel("Локация:")
        location_layout.addWidget(self.location_label)

        self.device_location = QComboBox()
        self.device_location.addItem("Нет доступных локаций", None)
        self.device_location.setEnabled(False)
        location_layout.addWidget(self.device_location, 1)

        self.locations_count_label = QLabel("(0)")
        location_layout.addWidget(self.locations_count_label)

        form_layout.addRow(location_container)

        # Инвентарный номер
        self.device_inventory_number = QLineEdit()
        self.device_inventory_number.setPlaceholderText("Инвентарный номер")
        form_layout.addRow(QLabel("Инв. номер:"), self.device_inventory_number)

        # Третий ряд
        self.device_name = QLineEdit()
        self.device_name.setPlaceholderText("Название оборудования")
        self.device_status = QComboBox()
        self.device_status.addItems(["active", "in_repair", "decommissioned", "lost"])

        row3_layout = QHBoxLayout()
        row3_layout.addWidget(QLabel("Название:"))
        row3_layout.addWidget(self.device_name)
        row3_layout.addSpacing(15)
        row3_layout.addWidget(QLabel("Статус:"))
        row3_layout.addWidget(self.device_status)
        form_layout.addRow(row3_layout)

        # Четвертый ряд (даты)
        self.device_purchase_date = QDateEdit()
        self.device_purchase_date.setCalendarPopup(True)
        self.device_purchase_date.setDate(QDate.currentDate())
        self.device_warranty_expiry = QDateEdit()
        self.device_warranty_expiry.setCalendarPopup(True)
        self.device_warranty_expiry.setDate(QDate.currentDate().addYears(1))

        row4_layout = QHBoxLayout()
        row4_layout.addWidget(QLabel("Дата покупки:"))
        row4_layout.addWidget(self.device_purchase_date)
        row4_layout.addSpacing(15)
        row4_layout.addWidget(QLabel("Гарантия до:"))
        row4_layout.addWidget(self.device_warranty_expiry)
        form_layout.addRow(row4_layout)

        # Пятый ряд (цена)
        self.device_purchase_price = QDoubleSpinBox()
        self.device_purchase_price.setPrefix("₽ ")
        self.device_purchase_price.setRange(0, 9999999.99)
        self.device_purchase_price.setDecimals(2)

        form_layout.addRow(QLabel("Цена покупки:"), self.device_purchase_price)

        # Примечания
        self.device_notes = QTextEdit()
        self.device_notes.setPlaceholderText("Примечания...")
        form_layout.addRow(QLabel("Примечания:"), self.device_notes)

    def create_buttons_layout(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.layout().addLayout(buttons_layout)

        self.add_device_btn = QPushButton("➕ Добавить")
        self.add_device_btn.clicked.connect(self.controller.add_device)
        buttons_layout.addWidget(self.add_device_btn)

        self.update_device_btn = QPushButton("🔄 Обновить")
        self.update_device_btn.setEnabled(False)
        self.update_device_btn.clicked.connect(self.controller.update_device)
        buttons_layout.addWidget(self.update_device_btn)

        self.delete_device_btn = QPushButton("🗑️ Удалить")
        self.delete_device_btn.setEnabled(False)
        self.delete_device_btn.clicked.connect(self.controller.delete_device)
        buttons_layout.addWidget(self.delete_device_btn)

        buttons_layout.addStretch()

        self.clear_device_btn = QPushButton("❌ Очистить")
        self.clear_device_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.clear_device_btn)

    def create_table(self):
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(9)
        self.device_table.setHorizontalHeaderLabels(
            ["🔖 ID", "📦 Тип", "🏢 Франшиза", "📍 Локация", "🏷️ Инв. номер",
             "🖥️ Название", "🔄 Статус", "🛒 Дата покупки", "📅 Гарантия"]
        )

        # Настройка таблицы
        self.device_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.device_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.device_table.setAlternatingRowColors(True)
        self.device_table.verticalHeader().hide()
        self.device_table.horizontalHeader().setHighlightSections(False)
        self.device_table.setSortingEnabled(True)
        self.device_table.cellClicked.connect(self.on_table_click)

        # Настройка растягивания столбцов
        header = self.device_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Тип
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Франшиза
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Локация
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Инв. номер
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Название
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Статус
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Дата покупки
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)  # Гарантия

        self.layout().addWidget(self.device_table)

    def load_data(self):
        self.controller.load_devices()
        self.controller.load_device_types()
        self.controller.load_franchises_for_devices()

    def populate_table(self, devices):
        self.device_table.setUpdatesEnabled(False)
        self.device_table.setRowCount(0)

        for row_num, row_data in enumerate(devices):
            self.device_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.device_table.setItem(row_num, col_num, item)

        self.device_table.setUpdatesEnabled(True)

    def populate_device_type_combo(self, device_types):
        self.device_type.clear()
        for device_type_id, name in device_types:
            self.device_type.addItem(name, device_type_id)

    def populate_franchise_combo(self, franchises):
        self.device_franchise.clear()
        self.device_franchise.addItem("Нет франшизы", None)
        for franchise_id, name in franchises:
            self.device_franchise.addItem(name, franchise_id)

    def populate_location_combo(self, locations):
        """Заполнить комбобокс локаций с учетом их наличия"""
        self.device_location.clear()
        self.locations_count = len(locations)

        if self.locations_count > 0:
            self.device_location.addItem("Выберите локацию...", None)
            for location_id, name in locations:
                self.device_location.addItem(name, location_id)
            self.device_location.setEnabled(True)
            self.locations_count_label.setText(f"({self.locations_count})")
        else:
            self._reset_location_combobox()

        # Всегда сбрасываем выбор при обновлении списка
        self.device_location.setCurrentIndex(0)

    def on_franchise_changed(self, index):
        if index >= 0:
            franchise_id = self.device_franchise.currentData()
            if franchise_id:  # Если выбрана конкретная франшиза
                # Сначала сбрасываем текущий выбор локации
                self.device_location.clear()
                self.device_location.addItem("Загрузка локаций...", None)
                self.device_location.setEnabled(False)
                self.locations_count_label.setText("(...)")

                # Затем загружаем локации для выбранной франшизы
                self.controller.load_locations_for_devices(franchise_id)
            else:  # Если выбрано "Нет франшизы"
                self._reset_location_combobox()

    def _reset_location_combobox(self):
        """Сбросить комбобокс локаций в исходное состояние"""
        self.device_location.clear()
        self.device_location.addItem("Нет доступных локаций", None)
        self.device_location.setEnabled(False)
        self.locations_count_label.setText("(0)")
        self.device_location.setCurrentIndex(0)

    def on_table_click(self, row, column):
        device_id = int(self.device_table.item(row, 0).text())
        device_type = self.device_table.item(row, 1).text()
        franchise = self.device_table.item(row, 2).text()
        location = self.device_table.item(row, 3).text()
        inventory_number = self.device_table.item(row, 4).text()
        device_name = self.device_table.item(row, 5).text()
        status = self.device_table.item(row, 6).text()
        purchase_date = self.device_table.item(row, 7).text()
        warranty_expiry = self.device_table.item(row, 8).text()

        self.current_device_id = device_id

        # Установка типа оборудования
        for i in range(self.device_type.count()):
            if self.device_type.itemText(i) == device_type:
                self.device_type.setCurrentIndex(i)
                break

        # Установка франшизы (это автоматически загрузит соответствующие локации)
        franchise_index = 0
        if franchise:
            for i in range(1, self.device_franchise.count()):
                if self.device_franchise.itemText(i) == franchise:
                    franchise_index = i
                    break
        self.device_franchise.setCurrentIndex(franchise_index)

        # После загрузки локаций устанавливаем выбранную
        if location:
            QTimer.singleShot(100, lambda: self._select_location(location))

        self.device_inventory_number.setText(inventory_number)
        self.device_name.setText(device_name)
        self.device_status.setCurrentText(status)
        self.device_purchase_date.setDate(QDate.fromString(purchase_date, "yyyy-MM-dd"))
        self.device_warranty_expiry.setDate(QDate.fromString(warranty_expiry, "yyyy-MM-dd"))

        self.controller.load_device_details(device_id)

        self.update_device_btn.setEnabled(True)
        self.delete_device_btn.setEnabled(True)
        self.add_device_btn.setEnabled(False)

    def _select_location(self, location_name):
        """Вспомогательный метод для выбора локации после загрузки"""
        if self.device_location.isEnabled():
            for i in range(1, self.device_location.count()):
                if self.device_location.itemText(i) == location_name:
                    self.device_location.setCurrentIndex(i)
                    break
            else:
                self.device_location.setCurrentIndex(0)
        else:
            self.device_location.setCurrentIndex(0)

    def show_details(self, purchase_price, notes, created_at, updated_at, device_type, franchise, location):
        self.device_purchase_price.setValue(purchase_price if purchase_price else 0)
        self.device_notes.setPlainText(notes if notes else "")

    def clear_form(self):
        if self.device_type.count() > 0:
            self.device_type.setCurrentIndex(0)
        if self.device_franchise.count() > 0:
            self.device_franchise.setCurrentIndex(0)
        self.device_location.clear()
        self.device_location.addItem("Нет доступных локаций", None)
        self.device_location.setEnabled(False)
        self.locations_count_label.setText("(0)")

        self.device_inventory_number.clear()
        self.device_name.clear()
        self.device_status.setCurrentIndex(0)
        self.device_purchase_date.setDate(QDate.currentDate())
        self.device_warranty_expiry.setDate(QDate.currentDate().addYears(1))
        self.device_purchase_price.setValue(0)
        self.device_notes.clear()

        self.current_device_id = None
        self.update_device_btn.setEnabled(False)
        self.delete_device_btn.setEnabled(False)
        self.add_device_btn.setEnabled(True)

    def show_message(self, title, message, is_error=False):
        msg = QMessageBox(self)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #353535;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
            }
        """)

        if is_error:
            msg.setWindowTitle(f"❌ {title}")
            msg.setIcon(QMessageBox.Icon.Critical)
        else:
            msg.setWindowTitle(f"✅ {title}")
            msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.exec()