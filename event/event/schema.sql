-- ============================================
-- Event Management System - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS event_management;
USE event_management;

-- ----------------------------
-- Table: Admin
-- ----------------------------
CREATE TABLE IF NOT EXISTS Admin (
    A_ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL
);

-- ----------------------------
-- Table: Customer
-- ----------------------------
CREATE TABLE IF NOT EXISTS Customer (
    C_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(150) NOT NULL UNIQUE,
    Address TEXT,
    Password VARCHAR(255) NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Table: Organizer
-- ----------------------------
CREATE TABLE IF NOT EXISTS Organizer (
    O_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    Contact VARCHAR(20),
    Email VARCHAR(150)
);

-- ----------------------------
-- Table: Venue
-- ----------------------------
CREATE TABLE IF NOT EXISTS Venue (
    V_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Address TEXT,
    Capacity INT,
    Availability ENUM('Available', 'Booked', 'Maintenance') DEFAULT 'Available'
);

-- ----------------------------
-- Table: Event
-- ----------------------------
CREATE TABLE IF NOT EXISTS Event (
    E_ID INT AUTO_INCREMENT PRIMARY KEY,
    Event_Name VARCHAR(250) NOT NULL,
    Date DATE,
    Time TIME,
    Location VARCHAR(250),
    Type VARCHAR(100),
    Description TEXT,
    Image VARCHAR(500) DEFAULT NULL,
    Price DECIMAL(10,2) DEFAULT 0.00,
    O_ID INT,
    V_ID INT,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (O_ID) REFERENCES Organizer(O_ID) ON DELETE SET NULL,
    FOREIGN KEY (V_ID) REFERENCES Venue(V_ID) ON DELETE SET NULL
);

-- ----------------------------
-- Table: Staff
-- ----------------------------
CREATE TABLE IF NOT EXISTS Staff (
    S_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    Role VARCHAR(100),
    Salary DECIMAL(10,2),
    Contact VARCHAR(20)
);

-- ----------------------------
-- Table: Booking
-- ----------------------------
CREATE TABLE IF NOT EXISTS Booking (
    B_ID INT AUTO_INCREMENT PRIMARY KEY,
    C_ID INT,
    E_ID INT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Amount DECIMAL(10,2),
    Status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (C_ID) REFERENCES Customer(C_ID) ON DELETE CASCADE,
    FOREIGN KEY (E_ID) REFERENCES Event(E_ID) ON DELETE CASCADE
);

-- ----------------------------
-- Table: Payment
-- ----------------------------
CREATE TABLE IF NOT EXISTS Payment (
    P_ID INT AUTO_INCREMENT PRIMARY KEY,
    B_ID INT,
    Amount DECIMAL(10,2),
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Mode ENUM('Cash', 'Card', 'UPI', 'Net Banking') DEFAULT 'Cash',
    FOREIGN KEY (B_ID) REFERENCES Booking(B_ID) ON DELETE CASCADE
);

-- ----------------------------
-- Table: Event_Staff (Many-to-Many)
-- ----------------------------
CREATE TABLE IF NOT EXISTS Event_Staff (
    E_ID INT,
    S_ID INT,
    PRIMARY KEY (E_ID, S_ID),
    FOREIGN KEY (E_ID) REFERENCES Event(E_ID) ON DELETE CASCADE,
    FOREIGN KEY (S_ID) REFERENCES Staff(S_ID) ON DELETE CASCADE
);
