-- -----------------------------------------------------
-- Database setup script for restaurant booking system
-- -----------------------------------------------------

-- Create database (optional)
CREATE DATABASE IF NOT EXISTS `production`;
USE `production`;

-- -----------------------------------------------------
-- Table structure for `table`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `table`;

CREATE TABLE `table` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `position` VARCHAR(255) NOT NULL,
  `capacity` INT NOT NULL,
  `active_flag` INT DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table structure for `booking`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `table_id` INT NOT NULL,
  `booking_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP NOT NULL,
  `customer_name` VARCHAR(255) NOT NULL,
  `customer_email` VARCHAR(255) NOT NULL,
  `active_flag` INT DEFAULT 1,
  `cancellation_time` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`table_id`) REFERENCES `table`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
