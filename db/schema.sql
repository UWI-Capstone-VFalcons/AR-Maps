DROP DATABASE IF EXISTS arMapsDB;
CREATE DATABASE arMapsDB;
USE arMapsDB;


CREATE TABLE `users` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`firstname` varchar(255) NOT NULL,
	`lastname` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

INSERT into users(firstname,lastname)
VALUES ("Tom","Bill");
