DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    username VARCHAR(45) NOT NULL,
    name VARCHAR(45) NOT NULL,
    lastname VARCHAR(45) NOT NULL,
    password VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    PRIMARY KEY (username)
);
