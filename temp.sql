
INSERT INTO airline (Airline_name, CEO, IATA_code)
VALUES
('Air India', 'Campbell Wilson', 'AI'),
('IndiGo', 'Pieter Elbers', '6E'),
('SpiceJet', 'Ajay Singh', 'SG'),
('Vistara', 'Vinod Kannan', 'UK');

INSERT INTO airport (Airport_id, Airport_Name, City, Country, IATA_code)
VALUES
(1, 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India', 'BOM'),
(2, 'Indira Gandhi International Airport', 'Delhi', 'India', 'DEL'),
(3, 'Kempegowda International Airport', 'Bangalore', 'India', 'BLR'),
(4, 'Netaji Subhas Chandra Bose International Airport', 'Kolkata', 'India', 'CCU'),
(5, 'Chennai International Airport', 'Chennai', 'India', 'MAA'),
(6, 'Rajiv Gandhi International Airport', 'Hyderabad', 'India', 'HYD'),
(7, 'Sardar Vallabhbhai Patel International Airport', 'Ahmedabad', 'India', 'AMD'),
(8, 'Cochin International Airport', 'Kochi', 'India', 'COK'),
(9, 'Pune International Airport', 'Pune', 'India', 'PNQ'),
(10, 'Goa International Airport', 'Goa', 'India', 'GOI'),
(11, 'Trivandrum International Airport', 'Thiruvananthapuram', 'India', 'TRV'),
(12, 'Jaipur International Airport', 'Jaipur', 'India', 'JAI');

INSERT INTO `airport-airline` (Airport_id, Airline_id)
VALUES
(1, 1),  -- Air India at Mumbai
(1, 2),  -- IndiGo at Mumbai
(1, 3),  -- SpiceJet at Mumbai
(2, 1),  -- Air India at Delhi
(2, 2),  -- IndiGo at Delhi
(3, 1),  -- Air India at Bangalore
(3, 4),  -- GoAir at Bangalore
(4, 3),  -- SpiceJet at Kolkata
(5, 1),  -- Air India at Chennai
(6, 4),  -- GoAir at Hyderabad
(7, 2),  -- IndiGo at Ahmedabad
(8, 3),  -- SpiceJet at Kochi
(9, 2),  -- IndiGo at Pune
(10, 3), -- SpiceJet at Goa
(11, 4), -- GoAir at Trivandrum
(12, 1); -- Air India at Jaipur

INSERT INTO passenger (Passenger_id, F_Name, L_Name, Gender, Nationality, Passport_No)
VALUES
(1, 'Aarav', 'Kapoor', 'Male', 'Indian', 123456789),
(2, 'Sanya', 'Sharma', 'Female', 'Indian', 987654321),
(3, 'Ishaan', 'Singh', 'Male', 'Indian', 345678912),
(4, 'Meera', 'Ahuja', 'Female', 'Indian', 876543219),
(5, 'Rahul', 'Jain', 'Male', 'Indian', 456789123),
(6, 'Puja', 'Thakur', 'Female', 'Indian', 567891234),
(7, 'Viraj', 'Reddy', 'Male', 'Indian', 678912345),
(8, 'Neelam', 'Joshi', 'Female', 'Indian', 789123456),
(9, 'Rohan', 'Gupta', 'Male', 'Indian', 891234567),
(10, 'Ananya', 'Verma', 'Female', 'Indian', 912345678);

INSERT INTO baggage (P_id, Baggage_No, Baggage_weight, Status)
VALUES
(1, 1, 23.50, 'Checked_in'),
(2, 2, 20.75, 'Lost'),
(3, 3, 25.00, 'Delivered'),
(4, 4, 22.30, 'Checked_in'),
(5, 5, 19.80, 'Delivered'),
(6, 6, 21.45, 'Checked_in'),
(7, 7, 24.60, 'Lost'),
(8, 8, 23.75, 'Checked_in'),
(9, 9, 20.90, 'Delivered'),
(10, 10, 22.15, 'Checked_in');

INSERT INTO gate (Gate_id, Gate_No, Capacity)
VALUES
(1, 101, 200),
(2, 102, 150),
(3, 103, 180),
(4, 104, 190),
(5, 105, 220),
(6, 106, 170),
(7, 107, 160),
(8, 108, 140),
(9, 109, 180),
(10, 110, 130),
(11, 111, 150),
(12, 112, 170),
(13, 113, 140),
(14, 114, 160),
(15, 115, 120),
(16, 116, 180),
(17, 117, 210),
(18, 118, 190),
(19, 119, 220),
(20, 120, 200);

INSERT INTO runway (Runway_id, Runway_No)
VALUES
(1, 25),
(2, 26),
(3, 27),
(4, 28);

INSERT INTO employee (Employee_id, F_Name, L_Name, Salary, G_No, R_No)
VALUES
(1, 'Raj', 'Sharma', 50000, 101, NULL),
(2, 'Amit', 'Kumar', 45000, 102, NULL),
(3, 'Rita', 'Mehta', 48000, 103, NULL),
(4, 'Suman', 'Singh', 47000, 104, NULL),
(5, 'Anil', 'Chopra', 52000, 105, NULL),
(6, 'Divya', 'Rao', 46000, NULL, 25),
(7, 'Neha', 'Mishra', 50000, NULL, 26),
(8, 'Rakesh', 'Verma', 53000, NULL, 27),
(9, 'Pooja', 'Gupta', 49000, NULL, 28),
(10, 'Suresh', 'Patel', 47000, 106, NULL),
(11, 'Kiran', 'Joshi', 51000, 107, NULL),
(12, 'Nisha', 'Yadav', 48000, 108, NULL),
(13, 'Rohit', 'Ahuja', 52000, NULL, 25),
(14, 'Naveen', 'Bajaj', 45000, NULL, 26),
(15, 'Meena', 'Shah', 47000, NULL, 27),
(16, 'Aditya', 'Reddy', 49000, 109, NULL),
(17, 'Siddharth', 'Desai', 50000, 110, NULL),
(18, 'Kavita', 'Pandey', 46000, NULL, 28),
(19, 'Jitendra', 'Nair', 52000, 111, NULL),
(20, 'Manish', 'Garg', 53000, 112, NULL);

INSERT INTO `employee-contacts` (Employee_id, Contact)
VALUES
(1, 9876543210),
(2, 9876543211),
(3, 9876543212),
(4, 9876543213),
(5, 9876543214),
(6, 9876543215),
(7, 9876543216),
(8, 9876543217),
(9, 9876543218),
(10, 9876543219),
(11, 9876543220),
(12, 9876543221),
(13, 9876543222),
(14, 9876543223),
(15, 9876543224),
(16, 9876543225),
(17, 9876543226),
(18, 9876543227),
(19, 9876543228),
(20, 9876543229);

INSERT INTO `passenger-contacts` (Passenger_id, Contact)
VALUES
(1, 9876543210),
(2, 9876543211),
(3, 9876543212),
(4, 9876543213),
(5, 9876543214),
(6, 9876543215),
(7, 9876543216),
(8, 9876543217),
(9, 9876543218),
(10, 9876543219);

INSERT INTO flight (Flight_instance_id, Flight_id, Arrival_time, Departure_time, Status, Wait_Duration, AP_ID, AL_ID, Runway_N, Gate_N)
VALUES
(1, 1001, '2024-11-20 10:30:00', '2024-11-20 12:00:00', 'On Time', '00:30:00', 1, 1, 101, 1),
(2, 1002, '2024-11-20 14:00:00', '2024-11-20 16:30:00', 'Delayed', '00:45:00', 2, 2, 102, 2),
(3, 1003, '2024-11-21 11:30:00', '2024-11-21 13:30:00', 'On Time', '00:20:00', 3, 3, 103, 3),
(4, 1004, '2024-11-22 17:00:00', '2024-11-22 19:00:00', 'Cancelled', NULL, 4, 4, 104, 4),
(5, 1005, '2024-11-23 09:30:00', '2024-11-23 11:45:00', 'On Time', '00:15:00', 5, 1, 105, 5),
(6, 1006, '2024-11-24 08:00:00', '2024-11-24 10:30:00', 'On Time', '00:20:00', 6, 2, 106, 6),
(7, 1007, '2024-11-24 13:45:00', '2024-11-24 16:00:00', 'On Time', '00:25:00', 7, 3, 107, 7),
(8, 1008, '2024-11-25 07:00:00', '2024-11-25 09:30:00', 'Delayed', '00:50:00', 8, 4, 108, 8),
(9, 1009, '2024-11-26 16:00:00', '2024-11-26 18:30:00', 'On Time', '00:40:00', 9, 1, 109, 9),
(10, 1010, '2024-11-27 12:30:00', '2024-11-27 14:45:00', 'On Time', '00:20:00', 10, 2, 110, 10),
(11, 1011, '2024-11-28 11:00:00', '2024-11-28 13:30:00', 'On Time', '00:25:00', 11, 3, 111, 11),
(12, 1012, '2024-11-29 10:00:00', '2024-11-29 12:30:00', 'Delayed', '00:35:00', 12, 4, 112, 12),
(13, 1013, '2024-11-30 14:00:00', '2024-11-30 16:15:00', 'On Time', '00:30:00', 13, 1, 113, 13),
(14, 1014, '2024-12-01 09:45:00', '2024-12-01 12:10:00', 'Cancelled', NULL, 14, 2, 114, 14),
(15, 1015, '2024-12-02 08:00:00', '2024-12-02 10:30:00', 'On Time', '00:25:00', 15, 3, 115, 15),
(16, 1016, '2024-12-03 13:30:00', '2024-12-03 15:50:00', 'Delayed', '00:40:00', 16, 4, 116, 16),
(17, 1017, '2024-12-04 07:15:00', '2024-12-04 09:45:00', 'On Time', '00:20:00', 17, 1, 117, 17),
(18, 1018, '2024-12-05 11:30:00', '2024-12-05 14:00:00', 'On Time', '00:30:00', 18, 2, 118, 18),
(19, 1019, '2024-12-06 06:00:00', '2024-12-06 08:25:00', 'On Time', '00:35:00', 19, 3, 119, 19),
(20, 1020, '2024-12-07 12:45:00', '2024-12-07 15:10:00', 'Delayed', '00:45:00', 20, 4, 120, 20),
(21, 1021, '2024-12-08 09:00:00', '2024-12-08 11:30:00', 'On Time', '00:20:00', 21, 1, 121, 21),
(22, 1022, '2024-12-09 13:00:00', '2024-12-09 15:20:00', 'On Time', '00:30:00', 22, 2, 122, 22),
(23, 1023, '2024-12-10 08:15:00', '2024-12-10 10:50:00', 'Cancelled', NULL, 23, 3, 123, 23),
(24, 1024, '2024-12-11 10:00:00', '2024-12-11 12:30:00', 'Delayed', '00:50:00', 24, 4, 124, 24),
(25, 1025, '2024-12-12 06:30:00', '2024-12-12 08:50:00', 'On Time', '00:25:00', 25, 1, 125, 25),
(26, 1026, '2024-12-13 11:45:00', '2024-12-13 14:10:00', 'On Time', '00:35:00', 26, 2, 126, 26),
(27, 1027, '2024-12-14 07:00:00', '2024-12-14 09:30:00', 'Delayed', '00:40:00', 27, 3, 127, 27),
(28, 1028, '2024-12-15 14:30:00', '2024-12-15 16:50:00', 'On Time', '00:20:00', 28, 4, 128, 28),
(29, 1029, '2024-12-16 10:45:00', '2024-12-16 13:15:00', 'On Time', '00:30:00', 29, 1, 129, 29),
(30, 1030, '2024-12-17 08:30:00', '2024-12-17 11:00:00', 'On Time', '00:25:00', 30, 2, 130, 30),
(31, 1031, '2024-12-18 09:15:00', '2024-12-18 11:50:00', 'Cancelled', NULL, 31, 3, 131, 31),
(32, 1032, '2024-12-19 06:45:00', '2024-12-19 09:10:00', 'Delayed', '00:45:00', 32, 4, 132, 32),
(33, 1033, '2024-12-20 10:30:00', '2024-12-20 12:50:00', 'On Time', '00:35:00', 33, 1, 133, 33),
(34, 1034, '2024-12-21 07:45:00', '2024-12-21 10:15:00', 'On Time', '00:25:00', 34, 2, 134, 34),
(35, 1035, '2024-12-22 08:30:00', '2024-12-22 11:00:00', 'Delayed', '00:40:00', 35, 3, 135, 35),
(36, 1036, '2024-12-23 14:15:00', '2024-12-23 16:40:00', 'On Time', '00:30:00', 36, 4, 136, 36),
(37, 1037, '2024-12-24 11:00:00', '2024-12-24 13:30:00', 'On Time', '00:20:00', 37, 1, 137, 37),
(38, 1038, '2024-12-25 08:15:00', '2024-12-25 10:45:00', 'On Time', '00:25:00', 38, 2, 138, 38),
(39, 1039, '2024-12-26 12:45:00', '2024-12-26 15:10:00', 'Cancelled', NULL, 39, 3, 139, 39),
(40, 1040, '2024-12-27 06:30:00', '2024-12-27 08:50:00', 'Delayed', '00:50:00', 40, 4, 140, 40),
(41, 1041, '2024-12-28 13:00:00', '2024-12-28 15:20:00', 'On Time', '00:30:00', 41, 1, 141, 41),
(42, 1042, '2024-12-29 09:30:00', '2024-12-29 12:00:00', 'On Time', '00:20:00', 42, 2, 142, 42),
(43, 1043, '2024-12-30 10:45:00', '2024-12-30 13:10:00', 'On Time', '00:25:00', 43, 3, 143, 43),
(44, 1044, '2024-12-31 08:00:00', '2024-12-31 10:30:00', 'Delayed', '00:40:00', 44, 4, 144, 44),
(45, 1045, '2025-01-01 06:45:00', '2025-01-01 09:10:00', 'Cancelled', NULL, 45, 1, 145, 45),
(46, 1046, '2025-01-02 11:30:00', '2025-01-02 14:00:00', 'On Time', '00:30:00', 46, 2, 146, 46),
(47, 1047, '2025-01-03 07:00:00', '2025-01-03 09:30:00', 'On Time', '00:20:00', 47, 3, 147, 47),
(48, 1048, '2025-01-04 09:45:00', '2025-01-04 12:10:00', 'Delayed', '00:45:00', 48, 4, 148, 48),
(49, 1049, '2025-01-05 12:30:00', '2025-01-05 14:50:00', 'On Time', '00:35:00', 49, 1, 149, 49),
(50, 1050, '2025-01-06 10:00:00', '2025-01-06 12:30:00', 'On Time', '00:25:00', 50, 2, 150, 50);


-- Inserting sample records into the tickets table
INSERT INTO `tickets` (`Seat_No`, `Booking_Date`, `Booking_Status`, `Flight_id`, `Airline_id`, `Passenger_id`, `ticketscol`)
VALUES
(1, '2024-11-18 10:00:00', 'Confirmed', 1001, 1, 1, 'TICKET1234'),
(2, '2024-11-18 11:00:00', 'Confirmed', 1002, 2, 2, 'TICKET1235'),
(3, '2024-11-18 12:00:00', 'Canceled', 1003, 3, 3, 'TICKET1236'),
(4, '2024-11-19 14:00:00', 'Confirmed', 1004, 1, 4, 'TICKET1237'),
(5, '2024-11-19 15:00:00', 'Confirmed', 1005, 2, 5, 'TICKET1238');