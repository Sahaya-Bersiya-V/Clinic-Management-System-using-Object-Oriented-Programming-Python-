-- Update Users Table
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Update Staff Table
ALTER TABLE staff ADD COLUMN specialization VARCHAR(100);
ALTER TABLE staff ADD COLUMN shift_start TIME;
ALTER TABLE staff ADD COLUMN shift_end TIME;

-- Update Patients Table
ALTER TABLE patients ADD COLUMN blood_group VARCHAR(5);
ALTER TABLE patients ADD COLUMN address TEXT;

-- Update Medicines Table
ALTER TABLE medicines ADD COLUMN expiry_date DATE;
ALTER TABLE medicines ADD COLUMN batch_no VARCHAR(50);
ALTER TABLE medicines ADD COLUMN min_stock_level INT DEFAULT 10;

-- Create Lab Tests Catalog
CREATE TABLE IF NOT EXISTS lab_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    normal_range VARCHAR(100)
);

-- Create Lab Requests (Linking Appointments/Patients to Tests)
CREATE TABLE IF NOT EXISTS lab_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    patient_id INT,
    test_id INT,
    technician_id INT,
    status VARCHAR(20) DEFAULT 'Pending', -- Pending, Completed
    result TEXT,
    report_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (test_id) REFERENCES lab_tests(test_id),
    FOREIGN KEY (technician_id) REFERENCES staff(staff_id)
);

-- Create Bills Table
CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_id INT,
    total_amount DECIMAL(10, 2),
    discount DECIMAL(10, 2) DEFAULT 0.0,
    final_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'Unpaid', -- Unpaid, Paid
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

-- Create Prescriptions Table (Structured)
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    medicine_id INT,
    dosage VARCHAR(100),
    duration VARCHAR(50),
    quantity INT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);

-- Insert some default Lab Tests
INSERT INTO lab_tests (test_name, cost, normal_range) VALUES 
('Blood Count (CBC)', 500.00, '4.5-5.5 M/uL'),
('X-Ray', 1000.00, 'N/A'),
('Urinalysis', 300.00, 'Negative'),
('MRI Scan', 5000.00, 'N/A');
