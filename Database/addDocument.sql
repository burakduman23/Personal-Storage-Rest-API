DELIMITER //
DROP PROCEDURE IF EXISTS addDocument //

CREATE PROCEDURE addDocument(doc_nameIn varchar(45), ownerIn varchar(45))
    BEGIN 
        INSERT INTO Documents(doc_name, owner) VALUES (doc_nameIN, ownerIn);
    END //
DELIMITER ;
