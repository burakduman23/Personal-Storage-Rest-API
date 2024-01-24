DELIMITER //
DROP PROCEDURE IF EXISTS deleteDocument //

CREATE PROCEDURE deleteDocument (IN ownerIN varchar(45), IN doc_nameIN varchar(45))
    BEGIN   
        DELETE FROM Documents
            WHERE owner = ownerIn and doc_name = doc_nameIN;
    END //
DELIMITER ;