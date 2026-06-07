DELIMITER //
CREATE TRIGGER auto_mark_listing_sold
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    -- If the new transaction is completed, take the item off the active market
    IF NEW.payment_status = 'completed' THEN
        UPDATE listing 
        SET status = 'sold' 
        WHERE listing_id = NEW.listing_id;
    END IF;
END; //
DELIMITER ;
