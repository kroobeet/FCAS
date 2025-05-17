CREATE OR REPLACE FUNCTION update_device_history()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.franchise_id IS DISTINCT FROM NEW.franchise_id OR 
       OLD.location_id IS DISTINCT FROM NEW.location_id OR
       OLD.status IS DISTINCT FROM NEW.status THEN
       
        INSERT INTO device_history (
            device_id, franchise_id, location_id, status, changed_at
        ) VALUES (
            NEW.device_id, NEW.franchise_id, NEW.location_id, NEW.status, CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_device_update
AFTER UPDATE ON device
FOR EACH ROW
EXECUTE FUNCTION update_device_history();