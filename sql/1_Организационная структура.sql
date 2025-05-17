CREATE TABLE franchise (
    franchise_id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES franchise(franchise_id),
    name VARCHAR(100) NOT NULL,
    address TEXT,
    contact_phone VARCHAR(20),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE location (
    location_id SERIAL PRIMARY KEY,
    franchise_id INTEGER NOT NULL REFERENCES franchise(franchise_id),
    name VARCHAR(100) NOT NULL,
    address TEXT,
    room_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);