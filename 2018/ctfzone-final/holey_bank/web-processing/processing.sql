CREATE DATABASE Processing;

USE Processing;

CREATE TABLE `Bank` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `bin` INT UNIQUE NOT NULL,
  `bik` INT UNIQUE NOT NULL,
  `name` TEXT NOT NULL,
  `vat` INT NOT NULL,
  `commission` FLOAT NOT NULL,
  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Bank_Accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `client` INT UNIQUE NOT NULL,
  `account` CHAR(20) UNIQUE NOT NULL,
  `balance` DOUBLE NOT NULL,
  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `from_` CHAR(20) NOT NULL,
  `to_` CHAR(20) NOT NULL,
  `transfer_type` CHAR(3) NOT NULL,
  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `transfer_comment` TEXT NOT NULL,
  `sum` DOUBLE NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Bank_Cards` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `account_id` INT NOT NULL,
  `card` CHAR(16) UNIQUE NOT NULL,
  `card_limit` DOUBLE NOT NULL,
  `card_balance` DOUBLE DEFAULT 0,
  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE USER 'processing'@'%' IDENTIFIED BY 'ALKHsd871gekag8J*@!&YTEOIEY^!@#';
GRANT ALL PRIVILEGES ON `Processing`.* TO 'processing'@'%';
GRANT SUPER ON *.* TO 'processing'@'%';
FLUSH PRIVILEGES;

INSERT INTO `Bank` (bin, bik, name, vat, commission) VALUES (161800, 112358132, 'Just Bank', 18, 1.5);

INSERT INTO `Bank_Accounts` (client, account, balance) VALUES (
    (SELECT bik FROM `Bank` ORDER BY id DESC LIMIT 1),
    '31337840000420000001',
    100000000
  );

DROP PROCEDURE IF EXISTS `Create_Account`;
DELIMITER //

CREATE PROCEDURE `Create_Account` (IN client_id INT, OUT result_id INT, OUT result_text TEXT)
LANGUAGE SQL
BEGIN
  DECLARE account_number CHAR(20);
  DECLARE flag INT DEFAULT 0;

  IF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE client = client_id)
    THEN
      WHILE flag < 1 DO
        SET account_number = CONCAT('3133784000042', CONVERT(ROUND((RAND() * (9999999-1000000))+1000000), CHAR));
        IF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE BINARY account = account_number)
          THEN
            SET flag = 1;
        END IF;
      END WHILE;

      IF flag >= 1 THEN
        INSERT INTO `Bank_Accounts` (client, account, balance)
        VALUES (
          client_id,
          account_number,
          1000
        );
        SET result_id = LAST_INSERT_ID();
        SET result_text = 'OK';
      END IF;
  ELSE
    SET result_id = 0;
    SET result_text = 'Account already exist';
  END IF;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS `Create_Card`;
DELIMITER //

CREATE PROCEDURE `Create_Card` (IN client_id INT, OUT result_id INT, OUT result_text TEXT)
LANGUAGE SQL
BEGIN
  DECLARE account INT;
  DECLARE flag INT DEFAULT 0;
  DECLARE card_number CHAR(16);

  SELECT id FROM Bank_Accounts WHERE client = client_id INTO account;

  IF account IS NOT NULL
    THEN
      WHILE flag < 1 DO
        SET card_number = CONCAT('161800',
            CONVERT(ROUND((RAND() * (9999999999-1000000000))+1000000000), CHAR)
          );
        IF NOT EXISTS (SELECT id FROM Bank_Cards WHERE BINARY card = card_number)
          THEN
            SET flag = 1;
        END IF;
      END WHILE;

      IF flag >= 1 THEN
        INSERT INTO `Bank_Cards` (account_id, card, card_limit)
        VALUES (account, card_number, 500);
        SET result_id = LAST_INSERT_ID();
        SET result_text = 'OK';
      END IF;
  ELSE
    SET result_id = 0;
    SET result_text = 'Unknown client identificator.';
  END IF;
END//

DELIMITER ;

DROP TRIGGER IF EXISTS `Before_Transaction`;
DELIMITER //

CREATE TRIGGER `Before_Transaction`
BEFORE INSERT ON `Transactions` FOR EACH ROW
BEGIN
  DECLARE current_sender_balance DOUBLE;
  DECLARE current_card_limit DOUBLE;
  DECLARE current_receiver_balance DOUBLE;
  DECLARE current_bank_balance DOUBLE;
  DECLARE comission DOUBLE;
  DECLARE current_sender_account_balance DOUBLE;
  DECLARE current_receiver_account_balance DOUBLE;
  DECLARE total_amount DOUBLE;

  IF NEW.from_ <> NEW.to_
    THEN
      CASE NEW.transfer_type
        WHEN 'c2c' THEN
          IF NOT EXISTS (SELECT id FROM Bank_Cards WHERE BINARY card = NEW.from_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Sender card does not exist! Please check and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Cards WHERE BINARY card = NEW.to_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Receiver card does not exist! Please check and try again.';
          ELSE
            IF NEW.sum >= 1 THEN
              SELECT card_balance, card_limit INTO current_sender_balance, current_card_limit FROM Bank_Cards WHERE BINARY card = NEW.from_;

              IF EXISTS (SELECT account_id FROM Bank_Cards WHERE BINARY card = NEW.from_ AND account_id IN (SELECT account_id FROM Bank_Cards WHERE BINARY card = NEW.to_))
                THEN
                  SET comission = 0;
                  SET total_amount = NEW.sum;
              ELSE
                SET comission = NEW.sum * 0.015;
                SET total_amount = NEW.sum + (NEW.sum * 0.015);
              END IF;

              IF current_card_limit < total_amount THEN
                SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'You have a card limit!';
              ELSEIF current_sender_balance < total_amount THEN
                SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'Card have not enough money!';
              ELSE
                SELECT card_balance FROM Bank_Cards WHERE BINARY card = NEW.to_ INTO current_receiver_balance;
                SELECT balance FROM Bank_Accounts WHERE BINARY account = '31337840000420000001' INTO current_bank_balance;

                UPDATE Bank_Cards SET card_limit = ROUND((current_card_limit - total_amount), 2), card_balance = ROUND((current_sender_balance - total_amount), 2) WHERE BINARY card = NEW.from_;
                UPDATE Bank_Cards SET card_balance = ROUND((current_receiver_balance + NEW.sum), 2) WHERE BINARY card = NEW.to_;
                UPDATE Bank_Accounts SET balance = ROUND((current_bank_balance + comission), 2) WHERE BINARY account = '31337840000420000001';

                IF LOCATE(NEW.from_, NEW.transfer_comment) OR LOCATE(NEW.to_, NEW.transfer_comment) THEN
                  CALL Change_Message(NEW.from_, NEW.to_, NEW.transfer_comment);
                END IF;

              END IF;

            ELSE
              SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Sum must be equal or more than $1.';
            END IF;
          END IF;
        WHEN 'a2a' THEN
          IF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE BINARY account = NEW.from_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Sender account does not exist! Please check it and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE BINARY account = NEW.to_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Receiver account does not exist! Please check and try again.';
          ELSE
            IF NEW.sum >= 1 THEN
              IF NEW.from_ <> NEW.to_ THEN
                SELECT balance FROM Bank_Accounts WHERE BINARY account = NEW.from_ INTO current_sender_account_balance;

                IF current_sender_account_balance < (NEW.sum + (NEW.sum * 0.18)) THEN
                  SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Have not enough money on account.';
                ELSE
                  SELECT balance FROM Bank_Accounts WHERE BINARY account = NEW.to_ INTO current_receiver_account_balance;
                  SELECT balance FROM Bank_Accounts WHERE BINARY account = '31337840000420000001' INTO current_bank_balance;

                  UPDATE Bank_Accounts SET balance = ROUND((current_sender_account_balance - (NEW.sum + (NEW.sum * 0.18))), 2) WHERE BINARY account = NEW.from_;
                  UPDATE Bank_Accounts SET balance = ROUND((current_receiver_account_balance + NEW.sum), 2) WHERE BINARY account = NEW.to_;
                  UPDATE Bank_Accounts SET balance = ROUND((current_bank_balance + (NEW.sum * 0.18)), 2) WHERE BINARY account = '31337840000420000001';

                END IF;
              ELSE
                SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'Operation dismissed.';
              END IF;
            ELSE
              SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Sum must be equal or more than $1.';
            END IF;
          END IF;
        WHEN 'a2c' THEN
          IF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE BINARY account = NEW.from_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Sender account does not exist! Please check and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Cards WHERE BINARY card = NEW.to_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Receiver card does not exist! Please check and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE id = (SELECT account_id FROM Bank_Cards WHERE BINARY card = NEW.to_)) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Account has not a card like that. Try again.';
          ELSE
            IF NEW.sum >= 1 THEN
              SELECT balance FROM Bank_Accounts WHERE BINARY account = NEW.from_ INTO current_sender_account_balance;

              IF current_sender_account_balance < (NEW.sum) THEN
                SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'Have not enough money on account.';
              ELSE
                SELECT card_balance FROM Bank_Cards WHERE BINARY card = NEW.to_ INTO current_receiver_balance;

                UPDATE Bank_Accounts SET balance = ROUND((current_sender_account_balance - NEW.sum), 2) WHERE BINARY account = NEW.from_;
                UPDATE Bank_Cards SET card_balance = ROUND((current_receiver_balance + NEW.sum), 2) WHERE BINARY card = NEW.to_;

              END IF;

            ELSE
              SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Sum must be equal or more than $1.';
            END IF;
          END IF;
        WHEN 'c2a' THEN
          IF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE BINARY account = NEW.to_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Account does not exist! Please check and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Cards WHERE BINARY card = NEW.from_) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Sender card does not exist! Please check and try again.';
          ELSEIF NOT EXISTS (SELECT id FROM Bank_Accounts WHERE id = (SELECT account_id FROM Bank_Cards WHERE BINARY card = NEW.from_)) THEN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Account has not a card like that. Try again.';
          ELSE
            IF NEW.sum >= 1 THEN
              IF ((SELECT card_balance FROM Bank_Cards WHERE BINARY card = NEW.from_) < (NEW.sum)) THEN
                SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'Have not enough money on card.';
              ELSE
                SELECT card_balance FROM Bank_Cards WHERE BINARY card = NEW.from_ INTO current_sender_balance;
                SELECT balance FROM Bank_Accounts WHERE BINARY account = NEW.to_ INTO current_receiver_balance;

                UPDATE Bank_Cards SET card_balance = ROUND((current_sender_balance - NEW.sum), 2) WHERE BINARY card = NEW.from_;
                UPDATE Bank_Accounts SET balance = ROUND((current_receiver_balance + NEW.sum), 2) WHERE BINARY account = NEW.to_;

              END IF;

            ELSE
              SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Sum must be equal or more than $1.';
            END IF;
          END IF;
        ELSE
          BEGIN
            SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Incorrect transaction type! Please, try another one.';
          END;
      END CASE;
  ELSE
    SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Sender and receiver can not be matched';
  END IF;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS `Change_Message`;
DELIMITER //

CREATE PROCEDURE `Change_Message` (IN from_card CHAR(20), IN to_card CHAR(20), INOUT message TEXT)
LANGUAGE SQL
BEGIN
  DECLARE from_card_mask TEXT;
  DECLARE to_card_mask TEXT;

  IF LOCATE(from_card, message) THEN
    CALL Card_Mask_Create(from_card, from_card_mask);
    SET message = (SELECT REPLACE(message, from_card, from_card_mask));
  END IF;

  IF LOCATE(to_card, message) THEN
    CALL Card_Mask_Create(from_card, to_card_mask);
    SET message = (SELECT REPLACE(message, to_card, to_card_mask));
  END IF;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS `Card_Mask_Create`;
DELIMITER //

CREATE PROCEDURE `Card_Mask_Create` (IN Card_Number CHAR(20), OUT Card_Mask CHAR(20))
LANGUAGE SQL
BEGIN
  SET Card_Mask = CONCAT(SUBSTRING(Card_Number,1,6), "******", SUBSTRING(Card_Number,13,16));
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS `Get_Cards_Transaction_History`;
DELIMITER //

CREATE PROCEDURE `Get_Cards_Transaction_History` (IN Cards TEXT(1024))
LANGUAGE SQL
BEGIN
  SET @sql = CONCAT('SELECT CONCAT(SUBSTRING(from_,1,6), "******", SUBSTRING(from_,13,16)), CONCAT(SUBSTRING(to_,1,6), "******", SUBSTRING(to_,13,16)), transfer_type, transfer_comment, date, sum FROM Transactions WHERE from_ IN (', Cards, ') or to_ IN (', Cards, ')');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END//

DELIMITER ;
