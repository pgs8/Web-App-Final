CREATE DATABASE airtravelData;
use airtravelData;

CREATE TABLE IF NOT EXISTS airtravelInput

(
    `id` int(3) AUTO_INCREMENT,
    `Months` VARCHAR(3) CHARACTER SET utf8,
    `YEAR_1958` INT,
    `YEAR_1959` INT,
    `YEAR_1960` INT,
    PRIMARY KEY (`id`)
);
INSERT INTO airtravelInput (Months, YEAR_1958, YEAR_1959, YEAR_1960)
VALUES
    ('JAN', 340, 360, 417),
    ('FEB', 318, 342, 391),
    ('MAR', 362, 406, 419),
    ('APR', 348, 396, 461),
    ('MAY', 363, 420, 472),
    ('JUN', 435, 472, 535),
    ('JUL', 491, 548, 622),
    ('AUG', 505, 559, 606),
    ('SEP', 404, 463, 508),
    ('OCT', 359, 407, 461),
    ('NOV', 310, 362, 390),
    ('DEC', 337, 405, 432);
