DELIMITER //
DROP PROCEDURE IF EXISTS addUser //

CREATE PROCEDURE addUser( usernameIn varchar(45), nameIn varchar(45), lastnameIn varchar(45), passwordIn varchar(45), emailIn varchar(45))
    BEGIN 
        INSERT INTO Users(username, name, lastname, password, email) VALUES (usernameIn, nameIn, lastnameIn, passwordIn, emailIn);
    END //
DELIMITER ;
