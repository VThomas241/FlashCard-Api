DROP TRIGGER IF EXISTS card_creation_deck_update_trigger;
DROP TRIGGER IF EXISTS card_update_new_old_trigger;
DROP TRIGGER IF EXISTS card_update_learning_old_trigger;
DROP TRIGGER IF EXISTS card_update_review_old_trigger;
DROP TRIGGER IF EXISTS card_update_new_new_trigger;
DROP TRIGGER IF EXISTS card_update_learning_new_trigger;
DROP TRIGGER IF EXISTS card_update_review_new_trigger;
DROP TRIGGER IF EXISTS card_delete_new_trigger;
DROP TRIGGER IF EXISTS card_delete_learning_trigger;
DROP TRIGGER IF EXISTS card_delete_review_trigger;

CREATE TRIGGER card_creation_deck_update_trigger
    AFTER INSERT ON card
    FOR EACH ROW
    BEGIN
        UPDATE deck
            SET new = new + 1
            WHERE id = NEW.deck_id;
    END;

CREATE TRIGGER card_update_new_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "new")
		BEGIN
			UPDATE deck SET new = new - 1 WHERE id = NEW.deck_id;
		END;
		
CREATE TRIGGER card_update_learning_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning-1 WHERE id = NEW.deck_id ;
		END;
		
CREATE TRIGGER card_update_review_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "review")
		BEGIN
			UPDATE deck SET review = review-1 WHERE id = NEW.deck_id ;
		END;
		
CREATE TRIGGER card_update_new_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "new")
		BEGIN
			UPDATE deck SET new = new+1 WHERE id = NEW.deck_id;
		END;
		
CREATE TRIGGER card_update_learning_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning+1 WHERE id = NEW.deck_id ;
		END;
		
CREATE TRIGGER card_update_review_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "review")
		BEGIN
			UPDATE deck SET review = review+1 WHERE id = NEW.deck_id ;
		END;
CREATE TRIGGER card_delete_new_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "new")
		BEGIN
			UPDATE deck SET new = new - 1 WHERE id = NEW.deck_id;
		END;
		
CREATE TRIGGER card_delete_learning_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning-1 WHERE id = NEW.deck_id ;
		END;
		
CREATE TRIGGER card_delete_review_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "review")
		BEGIN
			UPDATE deck SET review = review-1 WHERE id = NEW.deck_id ;
		END;