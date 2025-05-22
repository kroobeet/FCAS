from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QObject

from models.location import LocationModel


class LocationController(QObject):
    data_changed = Signal()  # Сигнал об изменении данных

    def __init__(self, db, view):
        super().__init__()
        self.model = LocationModel(db)
        self.view = view

    def load_locations(self):
        locations = self.model.get_all_locations()
        if locations is not False:
            self.view.populate_table(locations)
        else:
            self.view.show_message("Ошибка", "Не удалось загрузить список локаций", is_error=True)

    def load_franchises_for_locations(self):
        franchises = self.model.get_franchises_for_locations()
        if franchises is not False:
            self.view.populate_franchise_combo(franchises)
        else:
            self.view.show_message("Ошибка", "Не удалось загрузить список франшиз", is_error=True)

    def load_location_details(self, location_id):
        details = self.model.get_location_details(location_id)
        if details is not False and details:
            self.view.show_details(details[0][0], details[0][1])

    def add_location(self):
        name = self.view.location_name.text().strip()
        if not name:
            self.view.show_message("Ошибка", "Название локации обязательно для заполнения", is_error=True)
            return

        franchise_id = self.view.location_franchise.currentData()
        if not franchise_id:
            self.view.show_message("Ошибка", "Необходимо выбрать франшизу", is_error=True)
            return

        address = self.view.location_address.text().strip()
        room_number = self.view.location_room_number.text().strip()
        is_active = self.view.location_active.isChecked()

        result = self.model.add_location(franchise_id, name, address, room_number, is_active)
        if result is not False:
            self.view.show_message("Успех", "Локация успешно добавлена")
            self.data_changed.emit()
            self.view.clear_form()
        else:
            self.view.show_message("Ошибка", "Не удалось добавить локацию", is_error=True)

    def update_location(self):
        if not self.view.current_location_id:
            return

        name = self.view.location_name.text().strip()
        if not name:
            self.view.show_message("Ошибка", "Название локации обязательно для заполнения", is_error=True)
            return

        franchise_id = self.view.location_franchise.currentData()
        if not franchise_id:
            self.view.show_message("Ошибка", "Необходимо выбрать франшизу", is_error=True)
            return

        address = self.view.location_address.text().strip()
        room_number = self.view.location_room_number.text().strip()
        is_active = self.view.location_active.isChecked()

        result = self.model.update_location(
            self.view.current_location_id,
            franchise_id, name, address, room_number, is_active
        )

        if result is not False:
            self.view.show_message("Успех", "Локация успешно обновлена")
            self.data_changed.emit()
        else:
            self.view.show_message("Ошибка", "Не удалось обновить локацию", is_error=True)

    def delete_location(self):
        if not self.view.current_location_id:
            return

        confirm = QMessageBox.question(
            self.view,
            "Подтверждение",
            "Вы уверены, что хотите удалить эту локацию?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.No:
            return

        result = self.model.delete_location(self.view.current_location_id)
        if result == "device_exists":
            self.view.show_message(
                "Ошибка",
                "Нельзя удалить локацию, к которой привязано оборудование",
                is_error=True
            )
        elif result is not False:
            self.view.show_message("Успех", "Локация успешно удалена")
            self.data_changed.emit()
            self.view.clear_form()
        else:
            self.view.show_message("Ошибка", "Не удалось удалить локацию", is_error=True)