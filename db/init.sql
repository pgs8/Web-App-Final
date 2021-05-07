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

