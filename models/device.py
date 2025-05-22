class DeviceModel:
    def __init__(self, db):
        self.db = db

    def get_all_devices(self):
        query = """
            SELECT d.device_id, dt.name as device_type, f.name as franchise, 
                   l.name as location, d.inventory_number, d.name as device_name,
                   d.status, d.purchase_date, d.warranty_expiry
            FROM device d
            JOIN device_type dt ON d.device_type_id = dt.device_type_id
            JOIN franchise f ON d.franchise_id = f.franchise_id
            JOIN location l ON d.location_id = l.location_id
            ORDER BY d.device_id
        """
        return self.db.execute_query(query, fetch=True)

    def get_device_types(self):
        query = "SELECT device_type_id, name FROM device_type ORDER BY name"
        return self.db.execute_query(query, fetch=True)

    def get_franchises_for_devices(self):
        query = "SELECT franchise_id, name FROM franchise WHERE is_active = TRUE ORDER BY name"
        return self.db.execute_query(query, fetch=True)

    def get_locations_for_devices(self, franchise_id=None):
        query = """
            SELECT location_id, name FROM location 
            WHERE is_active = TRUE
        """
        params = ()
        if franchise_id:
            query += " AND franchise_id = %s"
            params = (franchise_id,)
        query += " ORDER BY name"
        return self.db.execute_query(query, params, fetch=True)

    def add_device(self, device_type_id, franchise_id, location_id, inventory_number,
                  name, status, purchase_date, warranty_expiry, purchase_price, notes):
        query = """
            INSERT INTO device (
                device_type_id, franchise_id, location_id, inventory_number,
                name, status, purchase_date, warranty_expiry, purchase_price, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING device_id
        """
        params = (
            device_type_id, franchise_id, location_id, inventory_number,
            name, status, purchase_date, warranty_expiry, purchase_price, notes
        )
        return self.db.execute_query(query, params, fetch=True)

    def update_device(self, device_id, device_type_id, franchise_id, location_id,
                     inventory_number, name, status, purchase_date, warranty_expiry,
                     purchase_price, notes):
        query = """
            UPDATE device
            SET device_type_id = %s, franchise_id = %s, location_id = %s,
                inventory_number = %s, name = %s, status = %s,
                purchase_date = %s, warranty_expiry = %s, purchase_price = %s,
                notes = %s, updated_at = CURRENT_TIMESTAMP
            WHERE device_id = %s
        """
        params = (
            device_type_id, franchise_id, location_id, inventory_number,
            name, status, purchase_date, warranty_expiry, purchase_price,
            notes, device_id
        )
        return self.db.execute_query(query, params)

    def delete_device(self, device_id):
        # Проверка на связанные компоненты
        component_check = """
            SELECT COUNT(*) FROM component
            WHERE device_id = %s
        """
        component_count = self.db.execute_query(component_check, (device_id,), fetch=True)[0][0]

        if component_count > 0:
            return "components_exist"

        # Удаление устройства
        delete_query = "DELETE FROM device WHERE device_id = %s"
        return self.db.execute_query(delete_query, (device_id,))

    def get_device_details(self, device_id):
        query = """
            SELECT d.purchase_price, d.notes, d.created_at, d.updated_at,
                   dt.name as device_type, f.name as franchise, l.name as location
            FROM device d
            JOIN device_type dt ON d.device_type_id = dt.device_type_id
            JOIN franchise f ON d.franchise_id = f.franchise_id
            JOIN location l ON d.location_id = l.location_id
            WHERE d.device_id = %s
        """
        return self.db.execute_query(query, (device_id,), fetch=True)

    def add_device_history(self, device_id, franchise_id, location_id, status, notes, changed_by):
        query = """
            INSERT INTO device_history (
                device_id, franchise_id, location_id, status, notes, changed_by
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (device_id, franchise_id, location_id, status, notes, changed_by)
        return self.db.execute_query(query, params)