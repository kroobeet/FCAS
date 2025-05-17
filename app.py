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

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке локаций:\n{str(e)}")

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

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.db_connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FranchiseApp()
    window.show()
    sys.exit(app.exec())