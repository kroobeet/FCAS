CREATE INDEX idx_device_franchise ON device(franchise_id);
CREATE INDEX idx_device_location ON device(location_id);
CREATE INDEX idx_device_status ON device(status);
CREATE INDEX idx_device_history_device ON device_history(device_id);
CREATE INDEX idx_component_device ON component(device_id);
CREATE INDEX idx_device_spec_device ON device_spec(device_id);
CREATE INDEX idx_device_spec_attribute ON device_spec(spec_attribute_id);