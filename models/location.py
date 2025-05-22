class LocationModel:
    def __init__(self, db):
        self.db = db

    def get_all_locations(self):
        query = """
            SELECT l.location_id, l.name, f.name as franchise_name,
                   l.address, l.room_number, l.is_active
            FROM location l
            JOIN franchise f ON l.franchise_id = f.franchise_id
            ORDER BY l.location_id
        """
        return self.db.execute_query(query, fetch=True)

    def get_franchises_for_locations(self):
        query = "SELECT franchise_id, name FROM franchise WHERE is_active = TRUE ORDER BY name"
        return self.db.execute_query(query, fetch=True)

    def add_location(self, franchise_id, name, address, room_number, is_active):
        query = """
            INSERT INTO location (franchise_id, name, address, room_number, is_active)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING location_id
        """
        return self.db.execute_query(query, (franchise_id, name, address, room_number, is_active), fetch=True)

    def update_location(self, location_id, franchise_id, name, address, room_number, is_active):
        query = """
            UPDATE location
            SET franchise_id = %s, name = %s, address = %s,
                room_number = %s, is_active = %s
            WHERE location_id = %s
        """
        return self.db.execute_query(query, (franchise_id, name, address, room_number, is_active, location_id))

    def delete_location(self, location_id):
        # Проверка на связанное оборудование
        device_check = """
            SELECT COUNT(*) FROM device
            WHERE location_id = %s
        """
        device_count = self.db.execute_query(device_check, (location_id,), fetch=True)[0][0]

        if device_count > 0:
            return "device_exists"

        # Удаление локации
        delete_query = "DELETE FROM location WHERE location_id = %s"
        return self.db.execute_query(delete_query, (location_id,))

    def get_location_details(self, location_id):
        query = """
            SELECT address, room_number
            FROM location
            WHERE location_id = %s
        """
        return self.db.execute_query(query, (location_id,), fetch=True)