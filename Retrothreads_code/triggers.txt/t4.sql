DELIMITER //
CREATE TRIGGER set_transaction_price
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE item_price DECIMAL(10,2);
    
    -- If the app didn't specify a final price, fetch it from the listing
    IF NEW.final_price IS NULL THEN
        SELECT price INTO item_price FROM listing WHERE listing_id = NEW.listing_id;
        SET NEW.final_price = item_price;
    END IF;
END; //
DELIMITER ;

