-- ============================================
-- Event Management System - Seed Data
-- ============================================

USE event_management;

-- Admin (password: admin123)
INSERT INTO Admin (Username, Password) VALUES
('admin', 'pbkdf2:sha256:1000000$salt$a6e514f06d5a5e1b0e9f2c3d4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b');

-- Organizers
INSERT INTO Organizer (Name, Contact, Email) VALUES
('Eventify Productions', '9876543210', 'eventify@demo.com'),
('Grand Celebrations', '9123456780', 'grand@demo.com'),
('StarLight Events', '9988776655', 'starlight@demo.com');

-- Venues
INSERT INTO Venue (Name, Address, Capacity, Availability) VALUES
('Royal Grand Palace', '123 Main Street, Bangalore', 500, 'Available'),
('Sunset Convention Center', '456 Lake Road, Mumbai', 1000, 'Available'),
('Crystal Ballroom', '789 Park Avenue, Delhi', 300, 'Available'),
('The Garden Terrace', '101 Green Lane, Hyderabad', 200, 'Available');

-- Events
INSERT INTO Event (Event_Name, Date, Time, Location, Type, Description, Price, O_ID, V_ID) VALUES
('Royal Wedding Gala', '2026-07-15', '18:00:00', 'Royal Grand Palace', 'Wedding',
 'An exquisite wedding celebration with grand decor, live music, and gourmet dining.', 50000.00, 1, 1),
('Tech Summit 2026', '2026-08-10', '09:00:00', 'Sunset Convention Center', 'Corporate',
 'Annual technology summit featuring keynote speakers, workshops, and networking.', 5000.00, 2, 2),
('Summer Music Festival', '2026-07-20', '16:00:00', 'The Garden Terrace', 'Concert',
 'Live performances by top artists with food stalls and fun activities.', 2500.00, 3, 4),
('Corporate Annual Meet', '2026-09-05', '10:00:00', 'Crystal Ballroom', 'Corporate',
 'Annual corporate meeting with presentations, awards, and team building.', 8000.00, 2, 3),
('Birthday Bash Deluxe', '2026-06-25', '19:00:00', 'Crystal Ballroom', 'Birthday',
 'A spectacular birthday celebration with themed decor and entertainment.', 15000.00, 1, 3),
('Charity Fundraiser Gala', '2026-10-12', '17:00:00', 'Sunset Convention Center', 'Social',
 'An elegant evening dedicated to raising funds for education and healthcare.', 3000.00, 3, 2),
('Diwali Night Celebration', '2026-11-01', '18:30:00', 'The Garden Terrace', 'Festival',
 'A grand Diwali celebration with fireworks, rangoli competition, traditional dance, and delicious festive food.', 2000.00, 1, 4),
('New Year Eve Bash 2027', '2026-12-31', '20:00:00', 'Sunset Convention Center', 'Social',
 'Ring in the new year with live DJ, dance floor, midnight countdown, and gourmet dinner buffet.', 7500.00, 3, 2),
('Startup Pitch Day', '2026-08-25', '09:30:00', 'Crystal Ballroom', 'Corporate',
 'An exciting event where startups pitch their ideas to top investors. Networking lunch included.', 3500.00, 2, 3),
('Classical Music Night', '2026-09-15', '19:00:00', 'Crystal Ballroom', 'Concert',
 'An enchanting evening of Indian classical music featuring renowned sitar and tabla artists.', 1500.00, 3, 3),
('Dream Wedding Expo', '2026-07-05', '10:00:00', 'Royal Grand Palace', 'Wedding',
 'Explore the latest wedding trends, meet top vendors, and plan your dream wedding all in one place.', 1000.00, 1, 1),
('Kids Carnival Fun Day', '2026-08-15', '11:00:00', 'The Garden Terrace', 'Festival',
 'A fun-filled day for kids with games, magic shows, face painting, bouncy castles, and cotton candy.', 800.00, 2, 4),
('Annual Sports Meet', '2026-09-20', '07:00:00', 'The Garden Terrace', 'Social',
 'A day of athletic competitions, team sports, and outdoor activities. Trophies and medals for winners.', 500.00, 1, 4),
('Bollywood Dance Night', '2026-10-25', '19:30:00', 'Sunset Convention Center', 'Concert',
 'Dance the night away with Bollywood hits performed live. Celebrity guest appearance and dance battles.', 4000.00, 3, 2),
('Business Leadership Summit', '2026-11-15', '09:00:00', 'Royal Grand Palace', 'Corporate',
 'A two-day leadership summit featuring keynote talks by Fortune 500 CEOs and interactive workshops.', 12000.00, 2, 1),
('Christmas Winter Gala', '2026-12-24', '18:00:00', 'Crystal Ballroom', 'Festival',
 'A magical Christmas celebration with carol singing, Secret Santa, snow theme decor, and plum cake.', 3500.00, 1, 3),
('College Farewell Party', '2026-06-30', '17:00:00', 'The Garden Terrace', 'Social',
 'A heartfelt farewell party with performances, awards, photo booth, and a grand dinner.', 1200.00, 3, 4);

-- Staff
INSERT INTO Staff (Name, Role, Salary, Contact) VALUES
('Rahul Sharma', 'Event Coordinator', 45000.00, '9876501234'),
('Priya Patel', 'Decorator', 35000.00, '9876502345'),
('Amit Kumar', 'Sound Engineer', 40000.00, '9876503456'),
('Sneha Reddy', 'Catering Manager', 38000.00, '9876504567'),
('Vikram Singh', 'Security Head', 42000.00, '9876505678');

-- Assign Staff to Events
INSERT INTO Event_Staff (E_ID, S_ID) VALUES
(1, 1), (1, 2), (1, 4),
(2, 1), (2, 3),
(3, 3), (3, 5),
(4, 1), (4, 4),
(5, 2), (5, 4),
(6, 1), (6, 5);

-- Customers (password for all: password123)
INSERT INTO Customer (Name, Phone, Email, Address, Password) VALUES
('Anusha', '9876512345', 'anusha@example.com', 'Bantakal, Udupi', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Navya', '9876523456', 'navya@example.com', 'Manipal, Udupi', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Ananya', '9876534567', 'ananya@example.com', 'Mangalore, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Chandana', '9876545678', 'chandana@example.com', 'Bangalore, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Dhanya', '9876556789', 'dhanya@example.com', 'Hubli, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Anvita', '9876567890', 'anvita@example.com', 'Mysore, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Anagha', '9876578901', 'anagha@example.com', 'Shimoga, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Deekshita', '9876589012', 'deekshita@example.com', 'Dharwad, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Ankita', '9876590123', 'ankita@example.com', 'Belgaum, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123'),
('Bhoomika', '9876501234', 'bhoomika@example.com', 'Davangere, Karnataka', 'pbkdf2:sha256:1000000$placeholder$abc123');

-- Bookings (mix of Confirmed, Pending, Cancelled)
INSERT INTO Booking (C_ID, E_ID, Date, Amount, Status) VALUES
(1, 1, '2026-05-20 10:30:00', 50000.00, 'Confirmed'),
(1, 3, '2026-05-22 14:00:00', 2500.00, 'Confirmed'),
(1, 7, '2026-05-25 09:15:00', 2000.00, 'Pending'),
(2, 2, '2026-05-18 11:00:00', 5000.00, 'Confirmed'),
(2, 5, '2026-05-21 16:30:00', 15000.00, 'Confirmed'),
(2, 8, '2026-05-26 12:00:00', 7500.00, 'Pending'),
(3, 1, '2026-05-19 09:00:00', 50000.00, 'Confirmed'),
(3, 4, '2026-05-23 10:45:00', 8000.00, 'Cancelled'),
(3, 10, '2026-05-27 15:30:00', 1500.00, 'Pending'),
(4, 3, '2026-05-20 13:00:00', 2500.00, 'Confirmed'),
(4, 6, '2026-05-24 11:30:00', 3000.00, 'Confirmed'),
(4, 9, '2026-05-26 08:00:00', 3500.00, 'Pending'),
(5, 2, '2026-05-17 10:00:00', 5000.00, 'Confirmed'),
(5, 11, '2026-05-22 14:30:00', 1000.00, 'Confirmed'),
(5, 14, '2026-05-28 17:00:00', 4000.00, 'Pending');

-- Payments (for Confirmed bookings)
INSERT INTO Payment (B_ID, Amount, Date, Mode) VALUES
(1, 50000.00, '2026-05-20 10:35:00', 'UPI'),
(2, 2500.00, '2026-05-22 14:10:00', 'Card'),
(4, 5000.00, '2026-05-18 11:15:00', 'Net Banking'),
(5, 15000.00, '2026-05-21 16:45:00', 'UPI'),
(7, 50000.00, '2026-05-19 09:20:00', 'Card'),
(10, 2500.00, '2026-05-20 13:15:00', 'Cash'),
(11, 3000.00, '2026-05-24 11:45:00', 'UPI'),
(13, 5000.00, '2026-05-17 10:20:00', 'Net Banking'),
(14, 1000.00, '2026-05-22 14:45:00', 'UPI');
