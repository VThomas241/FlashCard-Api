from sqlalchemy import DDL
from typing import List

class Trigger:
    '''
    Wrapper class for DDL Trigger Queries
    :param trigger: DDL query containing the trigger.
    '''
    triggers: List[DDL] = []

    def __init__(self,trigger:DDL):
        Trigger.triggers.append(trigger)

card_creation_new_trigger = Trigger(DDL('''
    CREATE TRIGGER card_creation_new_trigger
    AFTER INSERT ON card
    FOR EACH ROW
	WHEN (NEW.status = "new")
		BEGIN
			UPDATE deck
				SET new = new + 1
				WHERE id = NEW.deck_id;
		END;
'''))

card_creation_learning_trigger = Trigger(DDL('''
    CREATE TRIGGER card_creation_learning_trigger
    AFTER INSERT ON card
    FOR EACH ROW
	WHEN (NEW.status = "learning")
		BEGIN
			UPDATE deck
				SET learning = learning + 1
				WHERE id = NEW.deck_id;
		END;
'''))

card_creation_review_trigger = Trigger(DDL('''
    CREATE TRIGGER card_creation_review_trigger
    AFTER INSERT ON card
    FOR EACH ROW
	WHEN (NEW.status = "review")
		BEGIN
			UPDATE deck
				SET review = review + 1
				WHERE id = NEW.deck_id;
		END;
'''))

card_update_new_trigger__OLD = Trigger(DDL('''
CREATE TRIGGER card_update_new_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "new")
		BEGIN
			UPDATE deck SET new = new - 1 WHERE id = NEW.deck_id;
		END;
'''))

card_update_learning_trigger__OLD = Trigger(DDL('''
CREATE TRIGGER card_update_learning_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning - 1 WHERE id = NEW.deck_id ;
		END;
'''))

card_update_review_trigger__OLD = Trigger(DDL('''
CREATE TRIGGER card_update_review_old_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (OLD.status = "review")
		BEGIN
			UPDATE deck SET review = review - 1 WHERE id = NEW.deck_id ;
		END;
'''))

card_update_new_trigger__NEW = Trigger(DDL('''
CREATE TRIGGER card_update_new_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "new")
		BEGIN
			UPDATE deck SET new = new + 1 WHERE id = NEW.deck_id;
		END;
'''))

card_update_learning_trigger__NEW = Trigger(DDL('''
CREATE TRIGGER card_update_learning_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning + 1 WHERE id = NEW.deck_id ;
		END;
'''))

card_update_review_trigger__NEW = Trigger(DDL('''
CREATE TRIGGER card_update_review_new_trigger
	AFTER UPDATE ON card
	FOR EACH ROW
	WHEN (NEW.status = "review")
		BEGIN
			UPDATE deck SET review = review + 1 WHERE id = NEW.deck_id ;
		END;
'''))

card_delete_new_trigger = Trigger(DDL('''
CREATE TRIGGER card_delete_new_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "new")
		BEGIN
			UPDATE deck SET new = new - 1 WHERE id = OLD.deck_id;
		END;
'''))

card_delete_learning_trigger = Trigger(DDL('''
CREATE TRIGGER card_delete_learning_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "learning")
		BEGIN 
			UPDATE deck SET learning = learning-1 WHERE id = OLD.deck_id ;
		END;
'''))

card_delete_review_trigger = Trigger(DDL('''
CREATE TRIGGER card_delete_review_trigger
	AFTER DELETE ON card
	FOR EACH ROW
	WHEN (OLD.status = "review")
		BEGIN
			UPDATE deck SET review = review-1 WHERE id = OLD.deck_id ;
		END;
'''))