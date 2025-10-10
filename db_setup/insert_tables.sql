-- -----------------------------------------------------
-- Database setup script for restaurant booking system
-- -----------------------------------------------------

-- Create database (optional)
CREATE DATABASE IF NOT EXISTS `production`;
USE `production`;

-- -----------------------------------------------------
DROP TABLE IF EXISTS `table`;


CREATE TABLE `table` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `position` VARCHAR(255) NOT NULL,
  `capacity` INT NOT NULL,
  `active_flag` INT DEFAULT 1,
  `maintenance_flag` INT DEFAULT 0,
  `special_event_flag` INT DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `booking`;


CREATE TABLE `booking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `table_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `booking_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP NOT NULL,
  `active_flag` INT DEFAULT 1,
  `cancellation_time` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`table_id`) REFERENCES `table`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`customer_id`) REFERENCES `customer`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table structure for `time_slot`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `time_slot`;

CREATE TABLE `time_slot` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start_time` TIME NOT NULL,
  `end_time` TIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table structure for `customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `preferences` TEXT,
  `dietary_requirements` TEXT,
  `visit_history` TEXT,
  `special_occasions` TEXT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
