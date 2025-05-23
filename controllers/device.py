from PySide6.QtCore import Signal, QObject
from models.device import DeviceModel


class DeviceController(QObject):
    data_changed = Signal()  # Сигнал об изменении данных

    def __init__(self, db, view):
        super().__init__()
        self.model = DeviceModel(db)
        self.view = view

    def load_devices(self):
        devices = self.model.get_all_devices()
        if devices:
            self.view.populate_table(devices)

    def load_device_types(self):
        device_types = self.model.get_device_types()
        if device_types:
            self.view.populate_device_type_combo(device_types)

    def load_franchises_for_devices(self):
        franchises = self.model.get_franchises_for_devices()
        if franchises:
            self.view.populate_franchise_combo(franchises)

    def load_locations_for_devices(self, franchise_id=None):
        locations = self.model.get_locations_for_devices(franchise_id)
        if locations:
            self.view.populate_location_combo(locations)

    def load_device_details(self, device_id):
        details = self.model.get_device_details(device_id)
        if details:
            purchase_price, notes, created_at, updated_at, device_type, franchise, location = details[0]
            self.view.show_details(purchase_price, notes, created_at, updated_at, device_type, franchise, location)

    def add_device(self):
        device_type_id = self.view.device_type.currentData()
        if not device_type_id:
            self.view.show_message("Ошибка", "Тип оборудования обязателен!", True)
            return

        franchise_id = self.view.device_franchise.currentData()
        if not franchise_id:
            self.view.show_message("Ошибка", "Франшиза обязательна", True)
            return

        location_id = self.view.device_location.currentData()
        if not location_id:
            self.view.show_message("Ошибка", "Локация обязательна", True)
            return

        inventory_number = self.view.device_inventory_number.text().strip()
        name = self.view.device_name.text().strip()
        status = self.view.device_status.currentText()
        purchase_date = self.view.device_purchase_date.date().toString("yyyy-MM-dd")
        warranty_expiry = self.view.device_warranty_expiry.date().toString("yyyy-MM-dd")
        purchase_price = self.view.device_purchase_price.value()
        notes = self.view.device_notes.toPlainText()

        result = self.model.add_device(
            device_type_id, franchise_id, location_id,
            inventory_number if inventory_number else None,
            name if name else None,
            status,
            purchase_date if purchase_date else None,
            warranty_expiry if warranty_expiry else None,
            purchase_price if purchase_price else None,
            notes if notes else None
        )

        if result:
            device_id = result[0][0]
            self.model.add_device_history(
                device_id, franchise_id, location_id, status,
                "Первоначальное добавление оборудования", "system"
            )
            self.view.show_message("Успех", f"Оборудование успешно добавлено с ID: {device_id}")
            self.data_changed.emit()
            self.view.clear_form()

    def update_device(self):
        if not self.view.current_device_id:
            return

        device_type_id = self.view.device_type.currentData()
        if not device_type_id:
            self.view.show_message("Ошибка", "Тип оборудования обязателен!", True)
            return

        franchise_id = self.view.device_franchise.currentData()
        if not franchise_id:
            self.view.show_message("Ошибка", "Франшиза обязательна!", True)
            return

        location_id = self.view.device_location.currentData()
        if not location_id:
            self.view.show_message("Ошибка", "Локация обязательна!", True)
            return

        inventory_number = self.view.device_inventory_number.text().strip()
        name = self.view.device_name.text().strip()
        status = self.view.device_status.currentText()
        purchase_date = self.view.device_purchase_date.date().toString("yyyy-MM-dd")
        warranty_expiry = self.view.device_warranty_expiry.date().toString("yyyy-MM-dd")
        purchase_price = self.view.device_purchase_price.value()
        notes = self.view.device_notes.toPlainText()

        result = self.model.update_device(
            self.view.current_device_id,
            device_type_id, franchise_id, location_id,
            inventory_number if inventory_number else None,
            name if name else None,
            status,
            purchase_date if purchase_date else None,
            warranty_expiry if warranty_expiry else None,
            purchase_price if purchase_price else None,
            notes if notes else None
        )

        if result:
            self.model.add_device_history(
                self.view.current_device_id, franchise_id, location_id, status,
                "Обновление данных оборудования", "system"
            )
            self.view.show_message("Успех", "Оборудование успешно обновлено")
            self.data_changed.emit()
            self.view.clear_form()

    def delete_device(self):
        if not self.view.current_device_id:
            return

        result = self.model.delete_device(self.view.current_device_id)

        if result == "components_exist":
            self.view.show_message("Ошибка", "Нельзя удалить оборудование, у которого есть компоненты!", True)
        elif result:
            self.view.show_message("Успех", "Оборудование успешно удалено")
            self.data_changed.emit()
            self.view.clear_form()
