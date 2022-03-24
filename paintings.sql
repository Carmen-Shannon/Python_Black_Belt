-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema paintings
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema paintings
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `paintings` DEFAULT CHARACTER SET utf8 ;
USE `paintings` ;

-- -----------------------------------------------------
-- Table `paintings`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paintings`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `paintings`.`paintings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paintings`.`paintings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `description` TEXT NULL,
  `price` INT NULL,
  `quantity` INT NULL,
  `created_by` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `amount_purchased` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `paintings`.`owned_paintings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `paintings`.`owned_paintings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `painting_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_paintings_paintings1_idx` (`painting_id` ASC) VISIBLE,
  INDEX `fk_users_has_paintings_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_paintings_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `paintings`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_paintings_paintings1`
    FOREIGN KEY (`painting_id`)
    REFERENCES `paintings`.`paintings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
