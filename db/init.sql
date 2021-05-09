CREATE DATABASE airtravelData;
use airtravelData;

CREATE TABLE IF NOT EXISTS airtravelInput
(
    `id` int AUTO_INCREMENT,
    `YEAR` INT,
    `JAN` INT,
    `FEB` INT,
    `MAR` INT,
    `APR` INT,
    `MAY` INT,
    `JUN` INT,
    `JUL` INT,
    `AUG` INT,
    `SEP` INT,
    `OCT` INT,
    `NOV` INT,
    `DECE` INT,
    PRIMARY KEY (`id`)
);
INSERT INTO airtravelInput (YEAR, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DECE)
VALUES (1958, 340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337),
       (1959, 360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405),
       (1960, 417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432);


CREATE TABLE IF NOT EXISTS accounts
(
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
  	`confirmed` boolean DEFAULT FALSE NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO accounts (`id`, `username`, `password`, `email`, `confirmed`)
VALUES (1, 'test', 'test', 'test@test.com', TRUE);