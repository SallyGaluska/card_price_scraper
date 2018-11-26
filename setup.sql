CREATE TABLE Cards{
card_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
card_name VARCHAR(100)
}engine=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE Sets{
set_id INT UNSIGNED,
set_code VARCHAR(4),
set_name VARCHAR(50)
}engine=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE Card_Sets{
card_id INT UNSIGNED,
set_id INT UNSIGNED,
price DECIMAL(10:2)
}engine=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE Card_Sets ADD FOREIGN KEY (set_id) REFERENCES Sets(set_id);
ALTER TABLE Card_Sets ADD FOREIGN KEY (card_id) REFERENCES Cards(card_id);