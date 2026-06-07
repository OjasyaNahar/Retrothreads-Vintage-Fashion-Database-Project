DELIMITER //
CREATE TRIGGER prevent_self_purchase
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE item_seller INT;
    
    -- Find the seller of the listing being purchased
    SELECT seller_id INTO item_seller FROM listing WHERE listing_id = NEW.listing_id;
    
    -- Abort if the buyer and seller are the same person
    IF NEW.buyer_id = item_seller THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Fraud Prevention: A seller cannot purchase their own listing.';
    END IF;
END; //
DELIMITER ;

