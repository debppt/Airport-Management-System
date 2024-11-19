
-- 1. validating gate runway update
DELIMITER //
CREATE TRIGGER validate_gate_runway_update
BEFORE UPDATE ON employee
FOR EACH ROW
BEGIN
    -- Validate the Gate Number if updated
    IF NEW.G_No IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM gate WHERE gate_no = NEW.G_No) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid Gate Number. The gate does not exist.';
        END IF;
    END IF;

    -- Validate the Runway Number if updated
    IF NEW.R_No IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM runway WHERE runway_no = NEW.R_No) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid Runway Number. The runway does not exist.';
        END IF;
    END IF;

    -- Ensure only one of Gate or Runway is set
    IF NEW.G_No IS NOT NULL AND NEW.R_No IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Both Gate and Runway numbers cannot be updated simultaneously.';
    END IF;
END //

DELIMITER ;
