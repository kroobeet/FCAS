-- Типы устройств
INSERT INTO device_type (name, description) VALUES 
('Desktop', 'Стационарный компьютер'),
('Laptop', 'Ноутбук'),
('Server', 'Сервер'),
('Printer', 'Принтер');

-- Типы компонентов
INSERT INTO component_type (name, description) VALUES 
('CPU', 'Процессор'),
('RAM', 'Оперативная память'),
('HDD', 'Жесткий диск'),
('SSD', 'Твердотельный накопитель'),
('GPU', 'Видеокарта');

-- Категории характеристик
INSERT INTO spec_category (name, description) VALUES 
('Performance', 'Производительность'),
('Storage', 'Хранилище данных'),
('Display', 'Дисплей'),
('Network', 'Сетевое оборудование');

-- Атрибуты характеристик
INSERT INTO spec_attribute (spec_category_id, name, data_type, unit, is_required) VALUES 
(1, 'CPU Cores', 'integer', 'cores', TRUE),
(1, 'CPU Speed', 'decimal', 'GHz', TRUE),
(2, 'RAM Size', 'integer', 'GB', TRUE),
(2, 'Storage Size', 'integer', 'GB', TRUE),
(3, 'Screen Size', 'decimal', 'inches', FALSE),
(4, 'Network Speed', 'integer', 'Mbps', FALSE);