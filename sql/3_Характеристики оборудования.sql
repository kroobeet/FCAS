CREATE TABLE component_type (
    component_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE component (
    component_id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES device(device_id),
    component_type_id INTEGER NOT NULL REFERENCES component_type(component_type_id),
    model VARCHAR(100),
    specifications JSONB,
    installed_date DATE,
    notes TEXT
);

CREATE TABLE spec_category (
    spec_category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE spec_attribute (
    spec_attribute_id SERIAL PRIMARY KEY,
    spec_category_id INTEGER REFERENCES spec_category(spec_category_id),
    name VARCHAR(50) NOT NULL,
    data_type VARCHAR(20) NOT NULL CHECK (data_type IN ('string', 'integer', 'decimal', 'boolean', 'date')),
    unit VARCHAR(20),
    is_required BOOLEAN DEFAULT FALSE
);

CREATE TABLE device_spec (
    device_spec_id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES device(device_id),
    spec_attribute_id INTEGER NOT NULL REFERENCES spec_attribute(spec_attribute_id),
    value_string VARCHAR(255),
    value_integer INTEGER,
    value_decimal DECIMAL(10,2),
    value_boolean BOOLEAN,
    value_date DATE,
    UNIQUE (device_id, spec_attribute_id)
);