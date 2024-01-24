DELIMITER //
DROP PROCEDURE IF EXISTS deleteUserDocuments //

CREATE PROCEDURE deleteUserDocuments (IN ownerIn varchar(45))
    BEGIN
        DELETE FROM Documents
            WHERE owner = ownerIn;
    END //
DELIMITER ;