-- Setup local PostgreSQL database for Inventory Management System
-- Run this script as a PostgreSQL superuser (usually postgres)

-- Create user if not exists (you may need to run this manually)
-- CREATE USER postgres WITH PASSWORD 'rapid';

-- Create database
CREATE DATABASE IF NOT EXISTS inventory;

-- Connect to the inventory database
\c inventory;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create categories table (legacy)
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create items table (legacy)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100) UNIQUE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    reorder_level INTEGER DEFAULT 0,
    location VARCHAR(255),
    supplier VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create suppliers table (updated schema)
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    email VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255),
    address_line1 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    tax_id VARCHAR(100),
    payment_terms VARCHAR(255),
    credit_limit DECIMAL(15, 2),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create locations table
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    type VARCHAR(20) NOT NULL DEFAULT 'warehouse' CHECK (type IN ('warehouse', 'store', 'office', 'other')),
    address TEXT,
    contact_person VARCHAR(255),
    contact_phone VARCHAR(50),
    capacity INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100) NOT NULL UNIQUE,
    barcode VARCHAR(100),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    specifications JSONB,
    cost_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    selling_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    unit VARCHAR(50) NOT NULL DEFAULT 'piece',
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_featured BOOLEAN NOT NULL DEFAULT false,
    dimensions VARCHAR(100),
    weight DECIMAL(8, 2),
    supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create inventory_items table
CREATE TABLE IF NOT EXISTS inventory_items (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    reserved_quantity INTEGER NOT NULL DEFAULT 0,
    available_quantity INTEGER GENERATED ALWAYS AS (quantity - reserved_quantity) STORED,
    reorder_level INTEGER NOT NULL DEFAULT 0,
    reorder_quantity INTEGER NOT NULL DEFAULT 0,
    max_stock_level INTEGER,
    storage_location VARCHAR(255),
    storage_zone VARCHAR(100),
    unit_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_value DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * unit_cost) STORED,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, location_id)
);

-- Create purchase_orders table
CREATE TABLE IF NOT EXISTS purchase_orders (
    id SERIAL PRIMARY KEY,
    po_number VARCHAR(100) NOT NULL UNIQUE,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE RESTRICT,
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'ordered', 'received', 'cancelled')),
    total_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(15, 2) DEFAULT 0.00,
    shipping_amount DECIMAL(15, 2) DEFAULT 0.00,
    discount_amount DECIMAL(15, 2) DEFAULT 0.00,
    notes TEXT,
    terms_conditions TEXT,
    approved_by VARCHAR(255),
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create purchase_order_items table
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 0,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_price DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    received_quantity INTEGER NOT NULL DEFAULT 0,
    remaining_quantity INTEGER GENERATED ALWAYS AS (quantity - received_quantity) STORED,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create stock_alerts table
CREATE TABLE IF NOT EXISTS stock_alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(20) NOT NULL CHECK (alert_type IN ('low_stock', 'out_of_stock', 'expiring_soon', 'overstock')),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'acknowledged', 'resolved')),
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    location_id INTEGER REFERENCES locations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    current_quantity INTEGER NOT NULL DEFAULT 0,
    threshold_quantity INTEGER NOT NULL DEFAULT 0,
    is_email_sent BOOLEAN NOT NULL DEFAULT false,
    is_sms_sent BOOLEAN NOT NULL DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    resolution_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_categories_updated_at 
    BEFORE UPDATE ON categories 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_items_updated_at 
    BEFORE UPDATE ON items 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_suppliers_updated_at 
    BEFORE UPDATE ON suppliers 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_locations_updated_at 
    BEFORE UPDATE ON locations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_inventory_items_updated_at 
    BEFORE UPDATE ON inventory_items 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_purchase_orders_updated_at 
    BEFORE UPDATE ON purchase_orders 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_purchase_order_items_updated_at 
    BEFORE UPDATE ON purchase_order_items 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stock_alerts_updated_at 
    BEFORE UPDATE ON stock_alerts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Electronic devices and components'),
    ('Clothing', 'Apparel and accessories'),
    ('Books', 'Books and publications'),
    ('Home & Garden', 'Home improvement and garden supplies'),
    ('Sports', 'Sports equipment and accessories')
ON CONFLICT (name) DO NOTHING;

-- Insert sample suppliers (updated with new address fields)
INSERT INTO suppliers (name, code, description, email, phone, website, address_line1, city, state, postal_code, country, tax_id, payment_terms, credit_limit, is_active) VALUES
    ('Dell Inc.', 'DELL001', 'Computer hardware manufacturer', 'orders@dell.com', '+1-800-999-3355', 'https://www.dell.com', 'One Dell Way', 'Round Rock', 'TX', '78682', 'USA', 'TX123456789', 'Net 30', 50000.00, true),
    ('Apple Inc.', 'APPLE001', 'Consumer electronics company', 'supplier@apple.com', '+1-800-275-2273', 'https://www.apple.com', '1 Apple Park Way', 'Cupertino', 'CA', '95014', 'USA', 'CA987654321', 'Net 45', 100000.00, true),
    ('Nike Inc.', 'NIKE001', 'Athletic footwear and apparel', 'supply@nike.com', '+1-800-344-6453', 'https://www.nike.com', 'One Bowerman Drive', 'Beaverton', 'OR', '97005', 'USA', 'OR456789123', 'Net 30', 75000.00, true),
    ('O''Reilly Media', 'OREILLY001', 'Technical books and publications', 'orders@oreilly.com', '+1-800-998-9938', 'https://www.oreilly.com', '1005 Gravenstein Highway North', 'Sebastopol', 'CA', '95472', 'USA', 'CA789123456', 'Net 30', 25000.00, true),
    ('Home Depot', 'HOMEDEPOT001', 'Home improvement retailer', 'supplier@homedepot.com', '+1-800-466-3337', 'https://www.homedepot.com', '2455 Paces Ferry Road', 'Atlanta', 'GA', '30339', 'USA', 'GA321654987', 'Net 30', 100000.00, true),
    ('Spalding', 'SPALDING001', 'Sports equipment manufacturer', 'orders@spalding.com', '+1-800-558-5234', 'https://www.spalding.com', '1850 Gateway Boulevard', 'Springfield', 'MA', '01101', 'USA', 'MA147258369', 'Net 30', 50000.00, true)
ON CONFLICT (code) DO NOTHING;

-- Insert sample locations
INSERT INTO locations (name, code, description, type, address, contact_person, contact_phone, capacity, status) VALUES
    ('Main Warehouse', 'WH-MAIN', 'Primary storage facility', 'warehouse', '123 Industrial Blvd, City, State 12345', 'John Smith', '+1-555-123-4567', 10000, 'active'),
    ('Downtown Store', 'ST-DOWNTOWN', 'Retail store in downtown area', 'store', '456 Main Street, City, State 12345', 'Jane Doe', '+1-555-234-5678', 2000, 'active'),
    ('North Warehouse', 'WH-NORTH', 'Secondary storage facility', 'warehouse', '789 North Road, City, State 12345', 'Bob Johnson', '+1-555-345-6789', 8000, 'active'),
    ('Office Storage', 'OFF-STORAGE', 'Small storage at office location', 'office', '321 Office Park, City, State 12345', 'Alice Brown', '+1-555-456-7890', 500, 'active')
ON CONFLICT (code) DO NOTHING;

-- Insert sample products
INSERT INTO products (name, description, sku, barcode, category_id, specifications, cost_price, selling_price, unit, is_active, is_featured, dimensions, weight, supplier_id) VALUES
    ('Laptop Dell XPS 13', '13-inch premium laptop with Intel i7 processor', 'LAP-DELL-XPS13', '1234567890123', 1, '{"processor": "Intel i7-1250U", "ram": "16GB", "storage": "512GB SSD", "display": "13.4" 4K"}', 1100.00, 1299.99, 'piece', true, true, '11.6" x 7.8" x 0.6"', 2.8, 1),
    ('iPhone 15 Pro', 'Latest iPhone with A17 Pro chip and titanium design', 'PHONE-IPHONE15PRO', '2345678901234', 1, '{"processor": "A17 Pro", "storage": "256GB", "camera": "48MP", "display": "6.1" Super Retina XDR"}', 850.00, 999.99, 'piece', true, true, '5.8" x 2.8" x 0.3"', 0.4, 2),
    ('Nike Air Max 270', 'Comfortable running shoes with Air Max technology', 'SHOE-NIKE-AM270', '3456789012345', 2, '{"material": "Mesh and synthetic", "sole": "Rubber", "closure": "Lace-up", "style": "Running"}', 80.00, 129.99, 'pair', true, false, '12" x 4" x 4"', 1.2, 3),
    ('Python Programming Book', 'Comprehensive guide to Python programming language', 'BOOK-PYTHON-PROG', '4567890123456', 3, '{"pages": "544", "format": "Paperback", "language": "English", "isbn": "978-0-596-15810-1"}', 35.00, 49.99, 'piece', true, false, '9.2" x 7.4" x 1.2"', 1.8, 4),
    ('Garden Hose 50ft', 'Heavy-duty garden hose for outdoor use', 'GARDEN-HOSE-50FT', '5678901234567', 4, '{"length": "50 feet", "diameter": "5/8 inch", "material": "Rubber", "pressure": "150 PSI"}', 25.00, 39.99, 'piece', true, false, '50" x 0.625"', 8.5, 5),
    ('Basketball Official Size', 'Official size basketball for indoor/outdoor use', 'SPORT-BASKETBALL', '6789012345678', 5, '{"size": "Official (29.5")", "material": "Composite leather", "type": "Indoor/Outdoor", "weight": "22 oz"}', 18.00, 29.99, 'piece', true, false, '29.5" circumference', 1.4, 6)
ON CONFLICT (sku) DO NOTHING;

-- Insert sample inventory items
INSERT INTO inventory_items (product_id, location_id, quantity, reserved_quantity, reorder_level, reorder_quantity, max_stock_level, storage_location, storage_zone, unit_cost, status, notes) VALUES
    (1, 1, 15, 2, 5, 10, 50, 'Aisle A, Shelf 1', 'Zone A', 1100.00, 'active', 'Premium laptops section'),
    (1, 2, 8, 1, 3, 5, 20, 'Electronics section', 'Zone B', 1100.00, 'active', 'Display models available'),
    (2, 1, 25, 5, 10, 20, 100, 'Aisle B, Shelf 2', 'Zone A', 850.00, 'active', 'Latest iPhone models'),
    (2, 2, 12, 3, 5, 10, 30, 'Mobile section', 'Zone B', 850.00, 'active', 'Popular item'),
    (3, 1, 50, 8, 15, 30, 200, 'Aisle C, Shelf 1', 'Zone C', 80.00, 'active', 'Athletic footwear'),
    (3, 2, 20, 2, 8, 15, 50, 'Shoes section', 'Zone B', 80.00, 'active', 'Running shoes display'),
    (4, 1, 30, 3, 10, 20, 100, 'Aisle D, Shelf 1', 'Zone D', 35.00, 'active', 'Technical books'),
    (5, 1, 20, 0, 8, 15, 50, 'Aisle E, Shelf 3', 'Zone E', 25.00, 'active', 'Garden supplies'),
    (6, 1, 35, 5, 12, 25, 100, 'Aisle F, Shelf 2', 'Zone F', 18.00, 'active', 'Sports equipment')
ON CONFLICT (product_id, location_id) DO NOTHING;

-- Insert sample purchase orders
INSERT INTO purchase_orders (po_number, supplier_id, order_date, expected_delivery_date, status, total_amount, tax_amount, shipping_amount, discount_amount, notes, terms_conditions) VALUES
    ('PO-2024-001', 1, '2024-01-15', '2024-01-30', 'ordered', 5500.00, 440.00, 100.00, 0.00, 'Laptop order for Q1', 'Net 30, FOB Destination'),
    ('PO-2024-002', 2, '2024-01-20', '2024-02-05', 'draft', 3000.00, 240.00, 50.00, 100.00, 'iPhone order for retail', 'Net 45, FOB Origin'),
    ('PO-2024-003', 3, '2024-01-25', '2024-02-10', 'received', 4000.00, 320.00, 75.00, 0.00, 'Nike shoes order', 'Net 30, FOB Destination')
ON CONFLICT (po_number) DO NOTHING;

-- Insert sample purchase order items
INSERT INTO purchase_order_items (purchase_order_id, product_id, quantity, unit_price, notes) VALUES
    (1, 1, 5, 1100.00, 'Dell XPS 13 laptops'),
    (2, 2, 3, 850.00, 'iPhone 15 Pro units'),
    (3, 3, 50, 80.00, 'Nike Air Max 270 shoes')
ON CONFLICT DO NOTHING;

-- Insert sample stock alerts
INSERT INTO stock_alerts (alert_type, status, product_id, location_id, title, message, severity, current_quantity, threshold_quantity, is_email_sent, is_sms_sent) VALUES
    ('low_stock', 'active', 1, 2, 'Low Stock Alert - Dell XPS 13', 'Dell XPS 13 stock is running low at Downtown Store', 'medium', 8, 10, false, false),
    ('out_of_stock', 'active', 4, 2, 'Out of Stock Alert - Python Book', 'Python Programming Book is out of stock at Downtown Store', 'high', 0, 5, false, false),
    ('low_stock', 'acknowledged', 5, 1, 'Low Stock Alert - Garden Hose', 'Garden Hose stock is below reorder level at Main Warehouse', 'medium', 20, 25, true, false)
ON CONFLICT DO NOTHING;

-- Insert sample items (legacy)
INSERT INTO items (name, description, sku, category_id, quantity, unit_price, reorder_level, location, supplier) VALUES
    ('Laptop Dell XPS 13', '13-inch premium laptop with Intel i7', 'LAP-DELL-XPS13-LEGACY', 1, 15, 1299.99, 5, 'Warehouse A - Shelf 1', 'Dell Inc.'),
    ('iPhone 15 Pro', 'Latest iPhone with A17 Pro chip', 'PHONE-IPHONE15PRO-LEGACY', 1, 25, 999.99, 10, 'Warehouse A - Shelf 2', 'Apple Inc.'),
    ('Nike Air Max 270', 'Comfortable running shoes', 'SHOE-NIKE-AM270-LEGACY', 2, 50, 129.99, 15, 'Warehouse B - Shelf 1', 'Nike Inc.'),
    ('Python Programming Book', 'Learn Python programming language', 'BOOK-PYTHON-PROG-LEGACY', 3, 30, 49.99, 10, 'Warehouse C - Shelf 1', 'O''Reilly Media'),
    ('Garden Hose 50ft', 'Heavy-duty garden hose', 'GARDEN-HOSE-50FT-LEGACY', 4, 20, 39.99, 8, 'Warehouse B - Shelf 3', 'Home Depot'),
    ('Basketball', 'Official size basketball', 'SPORT-BASKETBALL-LEGACY', 5, 35, 29.99, 12, 'Warehouse B - Shelf 2', 'Spalding')
ON CONFLICT (sku) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_items_category_id ON items(category_id);
CREATE INDEX IF NOT EXISTS idx_items_sku ON items(sku);
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);

-- New indexes for enhanced system
CREATE INDEX IF NOT EXISTS idx_suppliers_code ON suppliers(code);
CREATE INDEX IF NOT EXISTS idx_suppliers_is_active ON suppliers(is_active);
CREATE INDEX IF NOT EXISTS idx_locations_code ON locations(code);
CREATE INDEX IF NOT EXISTS idx_locations_type ON locations(type);
CREATE INDEX IF NOT EXISTS idx_locations_status ON locations(status);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_supplier_id ON products(supplier_id);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_inventory_items_product_id ON inventory_items(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_items_location_id ON inventory_items(location_id);
CREATE INDEX IF NOT EXISTS idx_inventory_items_status ON inventory_items(status);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_po_number ON purchase_orders(po_number);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_supplier_id ON purchase_orders(supplier_id);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX IF NOT EXISTS idx_purchase_order_items_purchase_order_id ON purchase_order_items(purchase_order_id);
CREATE INDEX IF NOT EXISTS idx_purchase_order_items_product_id ON purchase_order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_alerts_product_id ON stock_alerts(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_alerts_location_id ON stock_alerts(location_id);
CREATE INDEX IF NOT EXISTS idx_stock_alerts_status ON stock_alerts(status);
CREATE INDEX IF NOT EXISTS idx_stock_alerts_alert_type ON stock_alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_stock_alerts_severity ON stock_alerts(severity);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Display summary
SELECT 'Database setup completed successfully!' as status;
SELECT COUNT(*) as categories_count FROM categories;
SELECT COUNT(*) as suppliers_count FROM suppliers;
SELECT COUNT(*) as locations_count FROM locations;
SELECT COUNT(*) as products_count FROM products;
SELECT COUNT(*) as inventory_items_count FROM inventory_items;
SELECT COUNT(*) as purchase_orders_count FROM purchase_orders;
SELECT COUNT(*) as stock_alerts_count FROM stock_alerts;
