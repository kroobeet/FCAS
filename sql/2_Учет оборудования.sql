CREATE TABLE device_type (
    device_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE device (
    device_id SERIAL PRIMARY KEY,
    device_type_id INTEGER NOT NULL REFERENCES device_type(device_type_id),
    franchise_id INTEGER NOT NULL REFERENCES franchise(franchise_id),
    location_id INTEGER NOT NULL REFERENCES location(location_id),
    inventory_number VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('active', 'in_repair', 'decommissioned', 'lost')),
    purchase_date DATE,
    warranty_expiry DATE,
    purchase_price DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE device_history (
    history_id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES device(device_id),
    franchise_id INTEGER REFERENCES franchise(franchise_id),
    location_id INTEGER REFERENCES location(location_id),
    status VARCHAR(20),
    notes TEXT,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50)
);