-- 1. Top 10 passengers:-
DELIMITER //
CREATE PROCEDURE GetTopPassengers()
BEGIN
    SELECT P.Passenger_ID, P.F_name, P.L_name, Total_Bookings
    FROM (
        SELECT B.Passenger_ID, COUNT(B.booking_ID) AS Total_Bookings
        FROM tickets B
        GROUP BY B.Passenger_ID
        ORDER BY Total_Bookings DESC
        LIMIT 10
    ) AS BookingCount
    JOIN passenger P ON BookingCount.Passenger_ID = P.Passenger_ID;
END //
DELIMITER ;



-- 2.CHECK PASSENGER ID

DELIMITER $$

CREATE PROCEDURE CheckPassengerID (
    IN input_passenger_id INT
)
BEGIN
    -- Check if Passenger ID exists and return the result
    SELECT EXISTS (
        SELECT 1
        FROM passenger
        WHERE Passenger_ID = input_passenger_id
    ) AS is_valid;
END $$

DELIMITER ;


-- 3.Top 10 airlines:-
DELIMITER //
CREATE PROCEDURE GetTopAirlines()
BEGIN
    SELECT Airline_Name, Total_Flights
    FROM (
        SELECT A.Airline_Name, COUNT(F.Flight_ID) AS Total_Flights
        FROM airline A
        JOIN flight F ON A.Airline_ID = F.Airline_ID
        GROUP BY A.Airline_Name
        ORDER BY Total_Flights DESC
        LIMIT 10
    ) AS TopAirlines;
END //
DELIMITER ;


-- 4. CHECK AVALIABLE FLIGHTS

DELIMITER //

CREATE PROCEDURE GetAvailableFlights(IN flight_date DATETIME, IN destination_city VARCHAR(255))
BEGIN
    SELECT F.Flight_ID, F.Departure_Time, F.Arrival_Time, A.City AS Destination
    FROM flight F
    JOIN airport A ON F.AP_ID = A.Airport_id
    WHERE DATE(F.Departure_Time) = DATE(flight_date) 
      AND A.City = destination_city
    ORDER BY F.Departure_Time ASC;
END //

DELIMITER ;

-- 5. BOOK TICKETS

DELIMITER //
CREATE PROCEDURE BookTicket(
    IN p_passenger_id INT,
    IN p_flight_instance_id INT
)
BEGIN
    DECLARE flight_id INT;
    DECLARE flight_date DATETIME;
    DECLARE airline_id INT;

    -- Fetch required details from the flight table
    SELECT Flight_ID, Departure_Time, AL_ID
    INTO flight_id, flight_date, airline_id
    FROM flight
    WHERE Flight_instance_id = p_flight_instance_id;

    -- Insert values into the tickets table
    INSERT INTO tickets(Flight_Date, booking_status, Flight_ID, Airline_ID, Passenger_ID)
    VALUES (flight_date, 'Confirmed', flight_id, airline_id, p_passenger_id);
END //

DELIMITER ;

-- 6. UPDATE GATE/RUNWAY NUMBER

DELIMITER //

CREATE PROCEDURE UpdateEmployeeGateRunway(
    IN p_employee_id INT,
    IN p_update_type VARCHAR(10),
    IN p_new_number INT
)
BEGIN
    DECLARE current_gate INT;
    DECLARE current_runway INT;

    -- Check if employee exists
    IF NOT EXISTS (SELECT 1 FROM employee WHERE Employee_ID = p_employee_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Employee not found.';
    END IF;

    -- Get current gate and runway numbers
    SELECT G_no, R_no INTO current_gate, current_runway
    FROM employee WHERE Employee_id = p_employee_id;

    -- Update Gate or Runway based on the update type
    IF p_update_type = 'gate' THEN
        -- Update Gate Number and set Runway Number to NULL
        UPDATE employee
        SET G_No = p_new_number, R_No = NULL
        WHERE Employee_ID = p_employee_id;
    ELSEIF p_update_type = 'runway' THEN
        -- Update Runway Number and set Gate Number to NULL
        UPDATE employee
        SET R_No = p_new_number, G_No = NULL
        WHERE Employee_ID = p_employee_id;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid update type.';
    END IF;

END //

DELIMITER ;
