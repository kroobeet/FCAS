from models.franchise import FranchiseModel


class FranchiseController:
    def __init__(self, db, view):
        self.model = FranchiseModel(db)
        self.view = view

    def load_franchises(self):
        franchises = self.model.get_all_franchises()
        if franchises:
            self.view.populate_table(franchises)

    def load_parent_franchises(self):
        parents = self.model.get_franchise_parents()
        if parents:
            self.view.populate_parent_combo(parents)

    def load_franchise_details(self, franchise_id):
        details = self.model.get_franchise_details(franchise_id)
        if details:
            address, email = details[0]
            self.view.show_details(address, email)

    def add_franchise(self):
        name = self.view.franchise_name.text().strip()
        if not name:
            self.view.show_message("Ошибка", "Название франшизы обязательно!", True)
            return

        parent_id = self.view.franchise_parent.currentData()
        address = self.view.franchise_address.text().strip()
        phone = self.view.franchise_phone.text().strip()
        email = self.view.franchise_email.text().strip()
        is_active = self.view.franchise_active.isChecked()

        result = self.model.add_franchise(
            name, parent_id,
            address if address else None,
            phone if phone else None,
            email if email else None,
            is_active
        )

        if result:
            franchise_id = result[0][0]
            self.view.show_message("Успех", f"Франшиза успешно добавлена с ID: {franchise_id}")
            self.load_franchises()
            self.load_parent_franchises()
            self.view.clear_form()

    def update_franchise(self):
        if not self.view.current_franchise_id:
            return

        name = self.view.franchise_name.text().strip()
        if not name:
            self.view.show_message("Ошибка", "Название франшизы обязательно!", True)
            return

        parent_id = self.view.franchise_parent.currentData()
        address = self.view.franchise_address.text().strip()
        phone = self.view.franchise_phone.text().strip()
        email = self.view.franchise_email.text().strip()
        is_active = self.view.franchise_active.isChecked()

        result = self.model.update_franchise(
            self.view.current_franchise_id,
            name, parent_id,
            address if address else None,
            phone if phone else None,
            email if email else None,
            is_active
        )

        if result:
            self.view.show_message("Успех", "Франшиза успешно обновлена")
            self.load_franchises()
            self.load_parent_franchises()
            self.view.clear_form()

    def delete_franchise(self):
        if not self.view.current_franchise_id:
            return

        result = self.model.delete_franchise(self.view.current_franchise_id)

        if result == "child_exists":
            self.view.show_message("Ошибка", "Нельзя удалить франшизу, у которой есть дочерние франшизы!", True)
        elif result == "location_exists":
            self.view.show_message("Ошибка", "Нельзя удалить франшизу, у которой есть локации!", True)
        elif result:
            self.view.show_message("Успех", "Франшиза успешно удалена")
            self.load_franchises()
            self.load_parent_franchises()
            self.view.clear_form()
