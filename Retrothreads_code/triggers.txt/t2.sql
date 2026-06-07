CREATE TRIGGER initialize_garment_approval 
AFTER INSERT ON GARMENT
REFERENCING NEW ROW AS nrow
FOR EACH ROW
BEGIN ATOMIC
    INSERT INTO APPROVAL (entity_type, entity_id, approval_status)
    VALUES ('GARMENT', nrow.garment_id, 'Pending');
END;

