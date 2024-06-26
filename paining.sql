-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema painting
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `painting` ;

-- -----------------------------------------------------
-- Schema painting
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `painting` DEFAULT CHARACTER SET utf8 ;
USE `painting` ;

-- -----------------------------------------------------
-- Table `painting`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `painting`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `painting`.`paintings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `painting`.`paintings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `price` FLOAT NOT NULL,
  `quantity` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_shows_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_shows_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `painting`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `painting`.`users_has_paintings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `painting`.`users_has_paintings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `painting_id` INT NOT NULL,
  INDEX `fk_users_has_paintings_paintings1_idx` (`painting_id` ASC) VISIBLE,
  INDEX `fk_users_has_paintings_users1_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_users_has_paintings_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `painting`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_paintings_paintings1`
    FOREIGN KEY (`painting_id`)
    REFERENCES `painting`.`paintings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
