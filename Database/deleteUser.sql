DELIMITER //
DROP PROCEDURE IF EXISTS deleteUser //

CREATE PROCEDURE deleteUser (IN usernameIn varchar(45))
    BEGIN
        DELETE FROM Documents
            WHERE owner = usernameIn;
        DELETE FROM Users
            WHERE username = usernameIn;
    END //
DELIMITER ;