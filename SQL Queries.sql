-- Create the database
CREATE DATABASE IF NOT EXISTS BloodBankDB;
USE BloodBankDB;

-- Create Admins table
CREATE TABLE IF NOT EXISTS Admins (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);

-- Create BloodBank table
CREATE TABLE IF NOT EXISTS BloodBank (
    Blood_Grp VARCHAR(5) NOT NULL PRIMARY KEY,
    units INT NOT NULL
);

-- Create Transactions table
CREATE TABLE IF NOT EXISTS Transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    blood_grp VARCHAR(5),
    units INT,
    action VARCHAR(10),
    date DATETIME,
    gender VARCHAR(10),
    contact_number VARCHAR(15),
    FOREIGN KEY (blood_grp) REFERENCES BloodBank(Blood_Grp)
);

-- Insert sample data into Admins table
INSERT INTO Admins (username, password) VALUES
('admin', 'admin123');

-- Insert sample data into BloodBank table
INSERT INTO BloodBank (Blood_Grp, units) VALUES
('A+', 10),
('B+', 15),
('AB+', 5),
('O+', 20),
('A-', 5),
('B-', 5),
('AB-', 3),
('O-', 10);

-- Sample transaction entries
INSERT INTO Transactions (name, blood_grp, units, action, date, gender, contact_number) VALUES
('John Doe', 'A+', 2, 'donate', NOW(), 'Male', '1234567890'),
('Jane Smith', 'O-', 1, 'request', NOW(), 'Female', '0987654321');
