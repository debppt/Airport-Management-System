CREATE TABLE `airline` (
  `Airline_id` int unsigned NOT NULL AUTO_INCREMENT,
  `Airline_name` varchar(45) NOT NULL,
  `CEO` varchar(45) DEFAULT NULL,
  `IATA_code` varchar(3) NOT NULL,
  PRIMARY KEY (`Airline_id`),
  UNIQUE KEY `Airline_id_UNIQUE` (`Airline_id`),
  UNIQUE KEY `Airline_name_UNIQUE` (`Airline_name`),
  UNIQUE KEY `IATA_code_UNIQUE` (`IATA_code`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `airport` (
  `Airport_id` int unsigned NOT NULL,
  `Airport_Name` varchar(80) DEFAULT NULL,
  `City` varchar(45) NOT NULL,
  `Country` varchar(45) NOT NULL,
  `IATA_code` varchar(3) NOT NULL,
  PRIMARY KEY (`Airport_id`),
  UNIQUE KEY `Airport_id_UNIQUE` (`Airport_id`),
  UNIQUE KEY `IATA_code_UNIQUE` (`IATA_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `airport-airline` (
  `Airport_id` int unsigned NOT NULL,
  `Airline_id` int unsigned NOT NULL,
  PRIMARY KEY (`Airport_id`,`Airline_id`),
  KEY `fk_airline_id` (`Airline_id`),
  CONSTRAINT `fk_airline_id` FOREIGN KEY (`Airline_id`) REFERENCES `airline` (`Airline_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_airport_id` FOREIGN KEY (`Airport_id`) REFERENCES `airport` (`Airport_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `gate` (
  `Gate_id` int unsigned NOT NULL,
  `Gate_No` int unsigned NOT NULL,
  `Capacity` int unsigned NOT NULL,
  PRIMARY KEY (`Gate_id`),
  UNIQUE KEY `Gate_id_UNIQUE` (`Gate_id`),
  UNIQUE KEY `Gate_No_UNIQUE` (`Gate_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `passenger` (
  `Passenger_id` int unsigned NOT NULL AUTO_INCREMENT,
  `F_Name` varchar(45) NOT NULL,
  `L_Name` varchar(45) NOT NULL,
  `Gender` enum('Male','Female','Other') NOT NULL,
  `Nationality` varchar(45) NOT NULL,
  `Passport_No` int NOT NULL,
  PRIMARY KEY (`Passenger_id`),
  UNIQUE KEY `Passenger_id_UNIQUE` (`Passenger_id`),
  UNIQUE KEY `Passport_No_UNIQUE` (`Passport_No`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `passenger-contacts` (
  `Passenger_id` int unsigned NOT NULL,
  `Contact` bigint DEFAULT NULL,
  KEY `fk_pass_idx` (`Passenger_id`),
  CONSTRAINT `fk_pass` FOREIGN KEY (`Passenger_id`) REFERENCES `passenger` (`Passenger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `runway` (
  `Runway_id` int unsigned NOT NULL,
  `Runway_No` int unsigned NOT NULL,
  PRIMARY KEY (`Runway_id`),
  UNIQUE KEY `Runway_id_UNIQUE` (`Runway_id`),
  UNIQUE KEY `Runway_No_UNIQUE` (`Runway_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `baggage` (
  `P_id` int unsigned NOT NULL,
  `Baggage_No` int unsigned NOT NULL,
  `Baggage_weight` decimal(5,2) unsigned NOT NULL,
  `Status` enum('Checked_in','Lost','Delivered') NOT NULL,
  PRIMARY KEY (`P_id`,`Baggage_No`),
  CONSTRAINT `fk_p_id` FOREIGN KEY (`P_id`) REFERENCES `passenger` (`Passenger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `employee` (
  `Employee_id` int unsigned NOT NULL AUTO_INCREMENT,
  `F_Name` varchar(45) NOT NULL,
  `L_Name` varchar(45) DEFAULT NULL,
  `Salary` int unsigned NOT NULL,
  `G_No` int unsigned DEFAULT NULL,
  `R_No` int unsigned DEFAULT NULL,
  PRIMARY KEY (`Employee_id`),
  KEY `fk_g_no` (`G_No`),
  KEY `fk_r_no` (`R_No`),
  CONSTRAINT `fk_g_no` FOREIGN KEY (`G_No`) REFERENCES `gate` (`Gate_No`),
  CONSTRAINT `fk_r_no` FOREIGN KEY (`R_No`) REFERENCES `runway` (`Runway_No`),
  CONSTRAINT `employee_chk_1` CHECK ((((`G_No` is not null) and (`R_No` is null)) or ((`G_No` is null) and (`R_No` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `employee-contacts` (
  `Employee_id` int unsigned NOT NULL,
  `Contact` bigint NOT NULL,
  PRIMARY KEY (`Employee_id`),
  CONSTRAINT `fk_emp` FOREIGN KEY (`Employee_id`) REFERENCES `employee` (`Employee_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `flight` (
  `Flight_instance_id` int unsigned NOT NULL AUTO_INCREMENT,
  `Flight_id` int unsigned NOT NULL,
  `Arrival_time` datetime NOT NULL,
  `Departure_time` datetime NOT NULL,
  `Status` varchar(9) DEFAULT NULL,
  `Wait_Duration` time DEFAULT NULL,
  `AP_ID` int unsigned NOT NULL,
  `AL_ID` int unsigned NOT NULL,
  `Runway_N` int unsigned NOT NULL,
  `Gate_N` int unsigned NOT NULL,
  PRIMARY KEY (`Flight_instance_id`),
  UNIQUE KEY `Flight_id_UNIQUE` (`Flight_id`),
  UNIQUE KEY `Flight_instance_id_UNIQUE` (`Flight_instance_id`),
  KEY `fk_al_id` (`AL_ID`),
  KEY `fk_ap_id` (`AP_ID`),
  KEY `fk_gate_n` (`Gate_N`),
  KEY `fk_runway_n` (`Runway_N`),
  CONSTRAINT `fk_al_id` FOREIGN KEY (`AL_ID`) REFERENCES `airline` (`Airline_id`),
  CONSTRAINT `fk_ap_id` FOREIGN KEY (`AP_ID`) REFERENCES `airport` (`Airport_id`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_gate_n` FOREIGN KEY (`Gate_N`) REFERENCES `gate` (`Gate_No`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_runway_n` FOREIGN KEY (`Runway_N`) REFERENCES `runway` (`Runway_No`) ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tickets` (
  `Booking_id` int unsigned NOT NULL AUTO_INCREMENT,
  `Flight_Date` datetime NOT NULL,
  `Booking_Status` enum('Confirmed','Canceled') NOT NULL DEFAULT 'Confirmed',
  `Flight_id` int unsigned NOT NULL,
  `Airline_id` int unsigned NOT NULL,
  `Passenger_id` int unsigned NOT NULL,
  PRIMARY KEY (`Booking_id`),
  UNIQUE KEY `Booking_id_UNIQUE` (`Booking_id`),
  KEY `fk_flight_id_idx` (`Flight_id`),
  KEY `fk_airline_id_idx` (`Airline_id`),
  KEY `fk_t_pid_idx` (`Passenger_id`),
  CONSTRAINT `fk_flight_id` FOREIGN KEY (`Flight_id`) REFERENCES `flight` (`Flight_id`) ON UPDATE RESTRICT,
  CONSTRAINT `fk_t_pid` FOREIGN KEY (`Passenger_id`) REFERENCES `passenger` (`Passenger_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;