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
        self.setWindowTitle("FCAS - Franchise Control and Administration System")
        self.setGeometry(100, 100, 1000, 800)

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

        # Вкладка для типов устройств
        self.device_type_tab = QWidget()
        self.tabs.addTab(self.device_type_tab, "Типы устройств")
        self.setup_device_type_tab()

        # Вкладка для устройств
        self.device_tab = QWidget()
        self.tabs.addTab(self.device_tab, "Оборудование")
        self.setup_device_tab()

        # Вкладка для истории устройств
        self.device_history_tab = QWidget()
        self.tabs.addTab(self.device_history_tab, "История оборудования")
        self.setup_device_history_tab()

        # Вкладка для компонентов
        self.component_tab = QWidget()
        self.tabs.addTab(self.component_tab, "Компоненты")
        self.setup_component_tab()

        # Загружаем начальные данные
        self.load_initial_data()

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

    def load_initial_data(self):
        """Загрузка всех начальных данных"""
        self.load_franchises()
        self.load_locations()
        self.load_device_types()
        self.load_devices()
        self.load_device_history()
        self.load_component_types()
        self.load_components()

    # ===== Франшизы =====
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
                    self.device_franchise.addItem(name, franchise_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке франшиз:\n{str(e)}")

    def add_franchise(self):
        """Добавление новой франшизы"""
        name = self.franchise_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название франшизы обязательно!")
            return

        parent_id = self.franchise_parent.currentData()
        address = self.franchise_address.text().strip()
        phone = self.franchise_phone.text().strip()
        email = self.franchise_email.text().strip()
        is_active = self.franchise_active.isChecked()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO franchise (parent_id, name, address, contact_phone, email, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING franchise_id
                """, (parent_id, name, address if address else None,
                      phone if phone else None, email if email else None, is_active))
                franchise_id = cursor.fetchone()[0]
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", f"Франшиза успешно добавлена с ID: {franchise_id}")
                self.load_franchises()
                self.clear_franchise_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении франшизы:\n{str(e)}")

    def update_franchise(self):
        """Обновление существующей франшизы"""
        if not hasattr(self, 'current_franchise_id'):
            return

        name = self.franchise_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название франшизы обязательно!")
            return

        parent_id = self.franchise_parent.currentData()
        address = self.franchise_address.text().strip()
        phone = self.franchise_phone.text().strip()
        email = self.franchise_email.text().strip()
        is_active = self.franchise_active.isChecked()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE franchise
                    SET parent_id = %s, name = %s, address = %s,
                        contact_phone = %s, email = %s, is_active = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE franchise_id = %s
                """, (parent_id, name, address if address else None,
                      phone if phone else None, email if email else None,
                      is_active, self.current_franchise_id))
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", "Франшиза успешно обновлена")
                self.load_franchises()
                self.clear_franchise_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении франшизы:\n{str(e)}")

    def delete_franchise(self):
        """Удаление франшизы"""
        if not hasattr(self, 'current_franchise_id'):
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту франшизу?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    # Проверяем, есть ли дочерние франшизы
                    cursor.execute("""
                        SELECT COUNT(*) FROM franchise 
                        WHERE parent_id = %s
                    """, (self.current_franchise_id,))
                    child_count = cursor.fetchone()[0]

                    if child_count > 0:
                        QMessageBox.warning(
                            self, "Ошибка",
                            "Нельзя удалить франшизу, у которой есть дочерние франшизы!"
                        )
                        return

                    # Проверяем, есть ли связанные локации
                    cursor.execute("""
                        SELECT COUNT(*) FROM location 
                        WHERE franchise_id = %s
                    """, (self.current_franchise_id,))
                    location_count = cursor.fetchone()[0]

                    if location_count > 0:
                        QMessageBox.warning(
                            self, "Ошибка",
                            "Нельзя удалить франшизу, у которой есть локации!"
                        )
                        return

                    # Удаляем франшизу
                    cursor.execute("""
                        DELETE FROM franchise 
                        WHERE franchise_id = %s
                    """, (self.current_franchise_id,))
                    self.db_connection.commit()

                    QMessageBox.information(self, "Успех", "Франшиза успешно удалена")
                    self.load_franchises()
                    self.clear_franchise_form()

            except psycopg2.Error as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении франшизы:\n{str(e)}")

    def franchise_table_click(self, row, column):
        """Обработка клика по таблице франшиз"""
        franchise_id = int(self.franchise_table.item(row, 0).text())
        franchise_name = self.franchise_table.item(row, 1).text()
        parent_name = self.franchise_table.item(row, 2).text()
        phone = self.franchise_table.item(row, 3).text()
        active = self.franchise_table.item(row, 4).text() == "True"

        # Заполняем форму
        self.current_franchise_id = franchise_id
        self.franchise_name.setText(franchise_name)

        # Устанавливаем родительскую франшизу
        parent_index = 0  # По умолчанию "Нет родительской"
        if parent_name:
            for i in range(1, self.franchise_parent.count()):
                if self.franchise_parent.itemText(i) == parent_name:
                    parent_index = i
                    break
        self.franchise_parent.setCurrentIndex(parent_index)

        self.franchise_phone.setText(phone)
        self.franchise_active.setChecked(active)

        # Получаем остальные данные из БД
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT address, email
                    FROM franchise
                    WHERE franchise_id = %s
                """, (franchise_id,))
                address, email = cursor.fetchone()
                self.franchise_address.setText(address if address else "")
                self.franchise_email.setText(email if email else "")

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных франшизы:\n{str(e)}")

        # Активируем кнопки
        self.update_franchise_btn.setEnabled(True)
        self.delete_franchise_btn.setEnabled(True)
        self.add_franchise_btn.setEnabled(False)

    def clear_franchise_form(self):
        """Очистка формы франшизы"""
        self.franchise_name.clear()
        self.franchise_parent.setCurrentIndex(0)
        self.franchise_address.clear()
        self.franchise_phone.clear()
        self.franchise_email.clear()
        self.franchise_active.setChecked(True)

        if hasattr(self, 'current_franchise_id'):
            del self.current_franchise_id

        self.update_franchise_btn.setEnabled(False)
        self.delete_franchise_btn.setEnabled(False)
        self.add_franchise_btn.setEnabled(True)

    # ===== Локации =====
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
        buttons_layout.addWidget(self.clear_location_btn)

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

    def load_locations(self):
        """Загрузка списка локаций из БД"""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT l.location_id, f.name as franchise_name, 
                           l.name, l.address, l.is_active
                    FROM location l
                    JOIN franchise f ON l.franchise_id = f.franchise_id
                    ORDER BY l.location_id
                """)
                locations = cursor.fetchall()

                # Очищаем таблицу
                self.location_table.setRowCount(0)

                # Заполняем таблицу
                for row_num, row_data in enumerate(locations):
                    self.location_table.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data) if data is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                        self.location_table.setItem(row_num, col_num, item)

                # Обновляем комбобокс для устройств
                self.device_location.clear()
                self.device_location.addItem("Не указана", None)
                cursor.execute("SELECT location_id, name FROM location ORDER BY name")
                for location_id, name in cursor.fetchall():
                    self.device_location.addItem(name, location_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке локаций:\n{str(e)}")

    def location_table_click(self, row, column):
        """Обработка клика по таблице локаций"""
        location_id = int(self.location_table.item(row, 0).text())
        franchise_name = self.location_table.item(row, 1).text()
        location_name = self.location_table.item(row, 2).text()
        address = self.location_table.item(row, 3).text()
        active = self.location_table.item(row, 4).text() == "True"

        # Заполняем форму
        self.current_location_id = location_id

        # Устанавливаем франшизу
        franchise_index = 0
        for i in range(self.location_franchise.count()):
            if self.location_franchise.itemText(i) == franchise_name:
                franchise_index = i
                break
        self.location_franchise.setCurrentIndex(franchise_index)

        self.location_name.setText(location_name)
        self.location_address.setText(address if address else "")
        self.location_active.setChecked(active)

        # Получаем номер помещения из БД
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT room_number
                    FROM location
                    WHERE location_id = %s
                """, (location_id,))
                room_number = cursor.fetchone()[0]
                self.location_room.setText(room_number if room_number else "")

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных локации:\n{str(e)}")

        # Активируем кнопки
        self.update_location_btn.setEnabled(True)
        self.delete_location_btn.setEnabled(True)
        self.add_location_btn.setEnabled(False)

    def add_location(self):
        """Добавление новой локации"""
        franchise_id = self.location_franchise.currentData()
        if not franchise_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать франшизу!")
            return

        name = self.location_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название локации обязательно!")
            return

        address = self.location_address.text().strip()
        room_number = self.location_room.text().strip()
        is_active = self.location_active.isChecked()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO location (franchise_id, name, address, room_number, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING location_id
                """, (franchise_id, name, address if address else None,
                      room_number if room_number else None, is_active))
                location_id = cursor.fetchone()[0]
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", f"Локация успешно добавлена с ID: {location_id}")
                self.load_locations()
                self.clear_location_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении локации:\n{str(e)}")

    def update_location(self):
        """Обновление существующей локации"""
        if not hasattr(self, 'current_location_id'):
            return

        franchise_id = self.location_franchise.currentData()
        if not franchise_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать франшизу!")
            return

        name = self.location_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название локации обязательно!")
            return

        address = self.location_address.text().strip()
        room_number = self.location_room.text().strip()
        is_active = self.location_active.isChecked()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE location
                    SET franchise_id = %s, name = %s, address = %s,
                        room_number = %s, is_active = %s
                    WHERE location_id = %s
                """, (franchise_id, name, address if address else None,
                      room_number if room_number else None, is_active,
                      self.current_location_id))
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", "Локация успешно обновлена")
                self.load_locations()
                self.clear_location_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении локации:\n{str(e)}")

    def delete_location(self):
        """Удаление локации"""
        if not hasattr(self, 'current_location_id'):
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту локацию?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM location 
                        WHERE location_id = %s
                    """, (self.current_location_id,))
                    self.db_connection.commit()

                    QMessageBox.information(self, "Успех", "Локация успешно удалена")
                    self.load_locations()
                    self.clear_location_form()

            except psycopg2.Error as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении локации:\n{str(e)}")

    def clear_location_form(self):
        """Очистка формы локации"""
        self.location_franchise.setCurrentIndex(0)
        self.location_name.clear()
        self.location_address.clear()
        self.location_room.clear()
        self.location_active.setChecked(True)

        if hasattr(self, 'current_location_id'):
            del self.current_location_id

        self.update_location_btn.setEnabled(False)
        self.delete_location_btn.setEnabled(False)
        self.add_location_btn.setEnabled(True)

    # ===== Типы устройств =====
    def setup_device_type_tab(self):
        """Настройка вкладки типов устройств"""
        layout = QVBoxLayout()
        self.device_type_tab.setLayout(layout)

        # Форма для добавления/редактирования
        form_layout = QVBoxLayout()
        layout.addLayout(form_layout)

        self.device_type_name = QLineEdit()
        form_layout.addWidget(QLabel("Название типа:"))
        form_layout.addWidget(self.device_type_name)

        self.device_type_description = QLineEdit()
        form_layout.addWidget(QLabel("Описание:"))
        form_layout.addWidget(self.device_type_description)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.add_device_type_btn = QPushButton("Добавить")
        self.add_device_type_btn.clicked.connect(self.add_device_type)
        buttons_layout.addWidget(self.add_device_type_btn)

        self.update_device_type_btn = QPushButton("Обновить")
        self.update_device_type_btn.setEnabled(False)
        self.update_device_type_btn.clicked.connect(self.update_device_type)
        buttons_layout.addWidget(self.update_device_type_btn)

        self.delete_device_type_btn = QPushButton("Удалить")
        self.delete_device_type_btn.setEnabled(False)
        self.delete_device_type_btn.clicked.connect(self.delete_device_type)
        buttons_layout.addWidget(self.delete_device_type_btn)

        self.clear_device_type_btn = QPushButton("Очистить")
        self.clear_device_type_btn.clicked.connect(self.clear_device_type_form)
        buttons_layout.addWidget(self.clear_device_type_btn)

        # Таблица с типами устройств
        self.device_type_table = QTableWidget()
        self.device_type_table.setColumnCount(3)
        self.device_type_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Описание"]
        )
        self.device_type_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.device_type_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.device_type_table.cellClicked.connect(self.device_type_table_click)
        layout.addWidget(self.device_type_table)

    def load_device_types(self):
        """Загрузка списка типов устройств из БД"""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT device_type_id, name, description FROM device_type ORDER BY name")
                device_types = cursor.fetchall()

                # Очищаем таблицу
                self.device_type_table.setRowCount(0)

                # Заполняем таблицу
                for row_num, row_data in enumerate(device_types):
                    self.device_type_table.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data) if data is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                        self.device_type_table.setItem(row_num, col_num, item)

                # Обновляем комбобокс для устройств
                self.device_type.clear()
                cursor.execute("SELECT device_type_id, name FROM device_type ORDER BY name")
                for device_type_id, name in cursor.fetchall():
                    self.device_type.addItem(name, device_type_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке типов устройств:\n{str(e)}")

    def device_type_table_click(self, row, column):
        """Обработка клика по таблице типов устройств"""
        device_type_id = int(self.device_type_table.item(row, 0).text())
        name = self.device_type_table.item(row, 1).text()
        description = self.device_type_table.item(row, 2).text()

        # Заполняем форму
        self.current_device_type_id = device_type_id
        self.device_type_name.setText(name)
        self.device_type_description.setText(description if description else "")

        # Активируем кнопки
        self.update_device_type_btn.setEnabled(True)
        self.delete_device_type_btn.setEnabled(True)
        self.add_device_type_btn.setEnabled(False)

    def add_device_type(self):
        """Добавление нового типа устройства"""
        name = self.device_type_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название типа обязательно!")
            return

        description = self.device_type_description.text().strip()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO device_type (name, description)
                    VALUES (%s, %s)
                    RETURNING device_type_id
                """, (name, description if description else None))
                device_type_id = cursor.fetchone()[0]
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", f"Тип устройства успешно добавлен с ID: {device_type_id}")
                self.load_device_types()
                self.clear_device_type_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении типа устройства:\n{str(e)}")

    def update_device_type(self):
        """Обновление существующего типа устройства"""
        if not hasattr(self, 'current_device_type_id'):
            return

        name = self.device_type_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название типа обязательно!")
            return

        description = self.device_type_description.text().strip()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE device_type
                    SET name = %s, description = %s
                    WHERE device_type_id = %s
                """, (name, description if description else None, self.current_device_type_id))
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", "Тип устройства успешно обновлен")
                self.load_device_types()
                self.clear_device_type_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении типа устройства:\n{str(e)}")

    def delete_device_type(self):
        """Удаление типа устройства"""
        if not hasattr(self, 'current_device_type_id'):
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот тип устройства?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    # Проверяем, есть ли связанные устройства
                    cursor.execute("""
                        SELECT COUNT(*) FROM device 
                        WHERE device_type_id = %s
                    """, (self.current_device_type_id,))
                    device_count = cursor.fetchone()[0]

                    if device_count > 0:
                        QMessageBox.warning(
                            self, "Ошибка",
                            "Нельзя удалить тип устройства, у которого есть устройства!"
                        )
                        return

                    cursor.execute("""
                        DELETE FROM device_type 
                        WHERE device_type_id = %s
                    """, (self.current_device_type_id,))
                    self.db_connection.commit()

                    QMessageBox.information(self, "Успех", "Тип устройства успешно удален")
                    self.load_device_types()
                    self.clear_device_type_form()

            except psycopg2.Error as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении типа устройства:\n{str(e)}")

    def clear_device_type_form(self):
        """Очистка формы типа устройства"""
        self.device_type_name.clear()
        self.device_type_description.clear()

        if hasattr(self, 'current_device_type_id'):
            del self.current_device_type_id

        self.update_device_type_btn.setEnabled(False)
        self.delete_device_type_btn.setEnabled(False)
        self.add_device_type_btn.setEnabled(True)

    # ===== Устройства =====
    def setup_device_tab(self):
        """Настройка вкладки устройств"""
        layout = QVBoxLayout()
        self.device_tab.setLayout(layout)

        # Форма для добавления/редактирования
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        form_layout.addLayout(left_form)

        self.device_type = QComboBox()
        left_form.addWidget(QLabel("Тип устройства:"))
        left_form.addWidget(self.device_type)

        self.device_franchise = QComboBox()
        left_form.addWidget(QLabel("Франшиза:"))
        left_form.addWidget(self.device_franchise)

        self.device_location = QComboBox()
        left_form.addWidget(QLabel("Локация:"))
        left_form.addWidget(self.device_location)

        self.device_inventory = QLineEdit()
        left_form.addWidget(QLabel("Инвентарный номер:"))
        left_form.addWidget(self.device_inventory)

        self.device_name = QLineEdit()
        left_form.addWidget(QLabel("Название:"))
        left_form.addWidget(self.device_name)

        # Правая часть формы
        right_form = QVBoxLayout()
        form_layout.addLayout(right_form)

        self.device_status = QComboBox()
        self.device_status.addItems(["active", "in_repair", "decommissioned", "lost"])
        right_form.addWidget(QLabel("Статус:"))
        right_form.addWidget(self.device_status)

        self.device_purchase_date = QDateEdit()
        self.device_purchase_date.setCalendarPopup(True)
        self.device_purchase_date.setDate(QDate.currentDate())
        right_form.addWidget(QLabel("Дата покупки:"))
        right_form.addWidget(self.device_purchase_date)

        self.device_warranty = QDateEdit()
        self.device_warranty.setCalendarPopup(True)
        self.device_warranty.setDate(QDate.currentDate().addYears(1))
        right_form.addWidget(QLabel("Дата окончания гарантии:"))
        right_form.addWidget(self.device_warranty)

        self.device_price = QLineEdit()
        self.device_price.setValidator(QDoubleValidator(0, 9999999, 2))
        right_form.addWidget(QLabel("Цена покупки:"))
        right_form.addWidget(self.device_price)

        self.device_notes = QLineEdit()
        right_form.addWidget(QLabel("Примечания:"))
        right_form.addWidget(self.device_notes)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.add_device_btn = QPushButton("Добавить")
        self.add_device_btn.clicked.connect(self.add_device)
        buttons_layout.addWidget(self.add_device_btn)

        self.update_device_btn = QPushButton("Обновить")
        self.update_device_btn.setEnabled(False)
        self.update_device_btn.clicked.connect(self.update_device)
        buttons_layout.addWidget(self.update_device_btn)

        self.delete_device_btn = QPushButton("Удалить")
        self.delete_device_btn.setEnabled(False)
        self.delete_device_btn.clicked.connect(self.delete_device)
        buttons_layout.addWidget(self.delete_device_btn)

        self.clear_device_btn = QPushButton("Очистить")
        self.clear_device_btn.clicked.connect(self.clear_device_form)
        buttons_layout.addWidget(self.clear_device_btn)

        # Таблица с устройствами
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(8)
        self.device_table.setHorizontalHeaderLabels(
            ["ID", "Тип", "Франшиза", "Локация", "Инв.№", "Название", "Статус", "Цена"]
        )
        self.device_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.device_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.device_table.cellClicked.connect(self.device_table_click)
        layout.addWidget(self.device_table)

    def load_devices(self):
        """Загрузка списка устройств из БД"""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.device_id, dt.name as device_type, f.name as franchise_name,
                           l.name as location_name, d.inventory_number, d.name,
                           d.status, d.purchase_price
                    FROM device d
                    JOIN device_type dt ON d.device_type_id = dt.device_type_id
                    JOIN franchise f ON d.franchise_id = f.franchise_id
                    LEFT JOIN location l ON d.location_id = l.location_id
                    ORDER BY d.device_id
                """)
                devices = cursor.fetchall()

                # Очищаем таблицу
                self.device_table.setRowCount(0)

                # Заполняем таблицу
                for row_num, row_data in enumerate(devices):
                    self.device_table.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data) if data is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                        self.device_table.setItem(row_num, col_num, item)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке устройств:\n{str(e)}")

    def device_table_click(self, row, column):
        """Обработка клика по таблице устройств"""
        device_id = int(self.device_table.item(row, 0).text())
        device_type = self.device_table.item(row, 1).text()
        franchise_name = self.device_table.item(row, 2).text()
        location_name = self.device_table.item(row, 3).text()
        inventory_number = self.device_table.item(row, 4).text()
        name = self.device_table.item(row, 5).text()
        status = self.device_table.item(row, 6).text()
        price = self.device_table.item(row, 7).text()

        # Заполняем форму
        self.current_device_id = device_id

        # Устанавливаем тип устройства
        type_index = 0
        for i in range(self.device_type.count()):
            if self.device_type.itemText(i) == device_type:
                type_index = i
                break
        self.device_type.setCurrentIndex(type_index)

        # Устанавливаем франшизу
        franchise_index = 0
        for i in range(self.device_franchise.count()):
            if self.device_franchise.itemText(i) == franchise_name:
                franchise_index = i
                break
        self.device_franchise.setCurrentIndex(franchise_index)

        # Устанавливаем локацию
        location_index = 0  # По умолчанию "Не указана"
        if location_name:
            for i in range(1, self.device_location.count()):
                if self.device_location.itemText(i) == location_name:
                    location_index = i
                    break
        self.device_location.setCurrentIndex(location_index)

        self.device_inventory.setText(inventory_number)
        self.device_name.setText(name)
        self.device_status.setCurrentText(status)

        if price:
            self.device_price.setText(str(price))
        else:
            self.device_price.clear()

        # Получаем остальные данные из БД
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT purchase_date, warranty_expiry, notes
                    FROM device
                    WHERE device_id = %s
                """, (device_id,))
                purchase_date, warranty_expiry, notes = cursor.fetchone()

                if purchase_date:
                    self.device_purchase_date.setDate(QDate.fromString(purchase_date, "yyyy-MM-dd"))
                if warranty_expiry:
                    self.device_warranty.setDate(QDate.fromString(warranty_expiry, "yyyy-MM-dd"))
                self.device_notes.setText(notes if notes else "")

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных устройства:\n{str(e)}")

        # Активируем кнопки
        self.update_device_btn.setEnabled(True)
        self.delete_device_btn.setEnabled(True)
        self.add_device_btn.setEnabled(False)

    def add_device(self):
        """Добавление нового устройства"""
        device_type_id = self.device_type.currentData()
        if not device_type_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать тип устройства!")
            return

        franchise_id = self.device_franchise.currentData()
        if not franchise_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать франшизу!")
            return

        inventory_number = self.device_inventory.text().strip()
        if not inventory_number:
            QMessageBox.warning(self, "Ошибка", "Инвентарный номер обязателен!")
            return

        name = self.device_name.text().strip()
        status = self.device_status.currentText()
        purchase_date = self.device_purchase_date.date().toString("yyyy-MM-dd")
        warranty_expiry = self.device_warranty.date().toString("yyyy-MM-dd")
        price = self.device_price.text().strip()
        notes = self.device_notes.text().strip()
        location_id = self.device_location.currentData()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO device (
                        device_type_id, franchise_id, location_id,
                        inventory_number, name, status, purchase_date,
                        warranty_expiry, purchase_price, notes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING device_id
                """, (
                    device_type_id, franchise_id, location_id,
                    inventory_number, name if name else None, status,
                    purchase_date, warranty_expiry,
                    float(price) if price else None,
                    notes if notes else None
                ))
                device_id = cursor.fetchone()[0]
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", f"Устройство успешно добавлено с ID: {device_id}")
                self.load_devices()
                self.clear_device_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении устройства:\n{str(e)}")

    def update_device(self):
        """Обновление существующего устройства"""
        if not hasattr(self, 'current_device_id'):
            return

        device_type_id = self.device_type.currentData()
        if not device_type_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать тип устройства!")
            return

        franchise_id = self.device_franchise.currentData()
        if not franchise_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать франшизу!")
            return

        inventory_number = self.device_inventory.text().strip()
        if not inventory_number:
            QMessageBox.warning(self, "Ошибка", "Инвентарный номер обязателен!")
            return

        name = self.device_name.text().strip()
        status = self.device_status.currentText()
        purchase_date = self.device_purchase_date.date().toString("yyyy-MM-dd")
        warranty_expiry = self.device_warranty.date().toString("yyyy-MM-dd")
        price = self.device_price.text().strip()
        notes = self.device_notes.text().strip()
        location_id = self.device_location.currentData()

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE device
                    SET device_type_id = %s, franchise_id = %s, location_id = %s,
                        inventory_number = %s, name = %s, status = %s,
                        purchase_date = %s, warranty_expiry = %s,
                        purchase_price = %s, notes = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE device_id = %s
                """, (
                    device_type_id, franchise_id, location_id,
                    inventory_number, name if name else None, status,
                    purchase_date, warranty_expiry,
                    float(price) if price else None,
                    notes if notes else None,
                    self.current_device_id
                ))
                self.db_connection.commit()

                QMessageBox.information(self, "Успех", "Устройство успешно обновлено")
                self.load_devices()
                self.clear_device_form()

        except psycopg2.Error as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении устройства:\n{str(e)}")

    def delete_device(self):
        """Удаление устройства"""
        if not hasattr(self, 'current_device_id'):
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить это устройство?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM device 
                        WHERE device_id = %s
                    """, (self.current_device_id,))
                    self.db_connection.commit()

                    QMessageBox.information(self, "Успех", "Устройство успешно удалено")
                    self.load_devices()
                    self.clear_device_form()

            except psycopg2.Error as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении устройства:\n{str(e)}")

    def clear_device_form(self):
        """Очистка формы устройства"""
        self.device_type.setCurrentIndex(0)
        self.device_franchise.setCurrentIndex(0)
        self.device_location.setCurrentIndex(0)
        self.device_inventory.clear()
        self.device_name.clear()
        self.device_status.setCurrentIndex(0)
        self.device_purchase_date.setDate(QDate.currentDate())
        self.device_warranty.setDate(QDate.currentDate().addYears(1))
        self.device_price.clear()
        self.device_notes.clear()

        if hasattr(self, 'current_device_id'):
            del self.current_device_id

        self.update_device_btn.setEnabled(False)
        self.delete_device_btn.setEnabled(False)
        self.add_device_btn.setEnabled(True)

    # ===== История устройств =====
    def setup_device_history_tab(self):
        """Настройка вкладки истории устройств"""
        layout = QVBoxLayout()
        self.device_history_tab.setLayout(layout)

        # Фильтры
        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        self.history_device = QComboBox()
        filter_layout.addWidget(QLabel("Устройство:"))
        filter_layout.addWidget(self.history_device)

        self.history_status = QComboBox()
        self.history_status.addItem("Все статусы", None)
        self.history_status.addItems(["active", "in_repair", "decommissioned", "lost"])
        filter_layout.addWidget(QLabel("Статус:"))
        filter_layout.addWidget(self.history_status)

        filter_btn = QPushButton("Применить фильтры")
        filter_btn.clicked.connect(self.load_device_history)
        filter_layout.addWidget(filter_btn)

        # Таблица с историей
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(
            ["ID", "Дата", "Устройство", "Франшиза", "Локация", "Статус"]
        )
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.history_table)

    def load_device_history(self):
        """Загрузка истории устройств из БД"""
        device_id = self.history_device.currentData()
        status = self.history_status.currentData()

        try:
            with self.db_connection.cursor() as cursor:
                query = """
                    SELECT h.history_id, h.changed_at, d.name as device_name,
                           f.name as franchise_name, l.name as location_name, h.status
                    FROM device_history h
                    JOIN device d ON h.device_id = d.device_id
                    LEFT JOIN franchise f ON h.franchise_id = f.franchise_id
                    LEFT JOIN location l ON h.location_id = l.location_id
                """
                params = []

                where_clauses = []
                if device_id:
                    where_clauses.append("h.device_id = %s")
                    params.append(device_id)
                if status:
                    where_clauses.append("h.status = %s")
                    params.append(status)

                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)

                query += " ORDER BY h.changed_at DESC"

                cursor.execute(query, params)
                history = cursor.fetchall()

                # Очищаем таблицу
                self.history_table.setRowCount(0)

                # Заполняем таблицу
                for row_num, row_data in enumerate(history):
                    self.history_table.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data) if data is not None else "")
                        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                        self.history_table.setItem(row_num, col_num, item)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке истории устройств:\n{str(e)}")

    # ===== Компоненты =====
    def setup_component_tab(self):
        """Настройка вкладки компонентов"""
        layout = QVBoxLayout()
        self.component_tab.setLayout(layout)

        # Фильтры
        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        self.component_device = QComboBox()
        filter_layout.addWidget(QLabel("Устройство:"))
        filter_layout.addWidget(self.component_device)

        self.component_type = QComboBox()
        filter_layout.addWidget(QLabel("Тип компонента:"))
        filter_layout.addWidget(self.component_type)

        filter_btn = QPushButton("Применить фильтры")
        filter_btn.clicked.connect(self.load_components)
        filter_layout.addWidget(filter_btn)

        # Форма для добавления/редактирования
        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        # Левая часть формы
        left_form = QVBoxLayout()
        form_layout.addLayout(left_form)

        self.component_selected_device = QComboBox()
        left_form.addWidget(QLabel("Устройство:"))
        left_form.addWidget(self.component_selected_device)

        self.component_selected_type = QComboBox()
        left_form.addWidget(QLabel("Тип компонента:"))
        left_form.addWidget(self.component_selected_type)

        self.component_model = QLineEdit()
        left_form.addWidget(QLabel("Модель:"))
        left_form.addWidget(self.component_model)

        # Правая часть формы
        right_form = QVBoxLayout()
        form_layout.addLayout(right_form)

        self.component_installed_date = QDateEdit()
        self.component_installed_date.setCalendarPopup(True)
        self.component_installed_date.setDate(QDate.currentDate())
        right_form.addWidget(QLabel("Дата установки:"))
        right_form.addWidget(self.component_installed_date)

        self.component_notes = QLineEdit()
        right_form.addWidget(QLabel("Примечания:"))
        right_form.addWidget(self.component_notes)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.add_component_btn = QPushButton("Добавить")
        self.add_component_btn.clicked.connect(self.add_component)
        buttons_layout.addWidget(self.add_component_btn)

        self.update_component_btn = QPushButton("Обновить")
        self.update_component_btn.setEnabled(False)
        self.update_component_btn.clicked.connect(self.update_component)
        buttons_layout.addWidget(self.update_component_btn)

        self.delete_component_btn = QPushButton("Удалить")
        self.delete_component_btn.setEnabled(False)
        self.delete_component_btn.clicked.connect(self.delete_component)
        buttons_layout.addWidget(self.delete_component_btn)

        self.clear_component_btn = QPushButton("Очистить")
        self.clear_component_btn.clicked.connect(self.clear_component_form)
        buttons_layout.addWidget(self.clear_component_btn)

        # Таблица с компонентами
        self.component_table = QTableWidget()
        self.component_table.setColumnCount(6)
        self.component_table.setHorizontalHeaderLabels(
            ["ID", "Устройство", "Тип", "Модель", "Дата установки", "Примечания"]
        )
        self.component_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.component_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.component_table.cellClicked.connect(self.component_table_click)
        layout.addWidget(self.component_table)

    def load_component_types(self):
        """Загрузка списка типов компонентов из БД"""
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT component_type_id, name FROM component_type ORDER BY name")
                component_types = cursor.fetchall()

                # Обновляем комбобоксы
                self.component_type.clear()
                self.component_type.addItem("Все типы", None)
                self.component_selected_type.clear()

                for component_type_id, name in cursor.fetchall():
                    self.component_type.addItem(name, component_type_id)
                    self.component_selected_type.addItem(name, component_type_id)

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке типов компонентов:\n{str(e)}")

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.db_connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FranchiseApp()
    window.show()
    sys.exit(app.exec())