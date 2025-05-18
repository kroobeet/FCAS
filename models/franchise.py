class FranchiseModel:
    def __init__(self, db):
        self.db = db

    def get_all_franchises(self):
        query = """
            SELECT f.franchise_id, f.name, p.name as parent_name,
                   f.contact_phone, f.is_active
            FROM franchise f 
            LEFT JOIN franchise p ON f.parent_id = p.franchise_id
            ORDER BY f.franchise_id
        """
        return self.db.execute_query(query, fetch=True)

    def get_franchise_parents(self):
        query = "SELECT franchise_id, name FROM franchise ORDER BY name"
        return self.db.execute_query(query, fetch=True)

    def add_franchise(self, name, parent_id, address, phone, email, is_active):
        query = """
            INSERT INTO franchise (parent_id, name, address, contact_phone, email, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING franchise_id
        """

        return self.db.execute_query(query, (parent_id, name, address, phone, email, is_active), fetch=True)

    def update_franchise(self, franchise_id, name, parent_id, address, phone, email, is_active):
        query = """
            UPDATE franchise
            SET parent_id = %s, name = %s, address = %s,
                contact_phone = %s, email = %s, is_active = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE franchise_id = %s
        """

        return self.db.execute_query(query, (parent_id, name, address, phone, email, is_active, franchise_id))

    def delete_franchise(self, franchise_id):
        # Проверка на дочерние франшизы
        child_check = """
            SELECT COUNT(*) FROM franchise
            WHERE parent_id = %s
        """
        child_count = self.db.execute_query(child_check, (franchise_id,), fetch=True)[0][0]

        if child_count > 0:
            return "child_exists"

        # Проверка на связанные локации
        location_check = """
            SELECT COUNT(*) FROM location
            WHERE franchise_id = %s
        """
        location_count = self.db.execute_query(location_check, (franchise_id,), fetch=True)[0][0]

        if location_count > 0:
            return "location_exists"

        # Удаление франшизы
        delete_query = "DELETE FROM franchise WHERE franchise_id = %s"
        return self.db.execute_query(delete_query, (franchise_id,))

    def get_franchise_details(self, franchise_id):
        query = """
            SELECT address, email
            FROM franchise
            WHERE franchise_id = %s
        """
        return self.db.execute_query(query, (franchise_id,), fetch=True)
