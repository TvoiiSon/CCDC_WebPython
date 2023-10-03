-- MySQL Script generated by MySQL Workbench
-- Sat Sep 30 12:06:33 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema builder
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema builder
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `builder` DEFAULT CHARACTER SET utf8 ;
USE `builder` ;

-- -----------------------------------------------------
-- Table `builder`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `builder`.`users` (
  `idusers` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NULL,
  `password` TEXT(255) NULL,
  PRIMARY KEY (`idusers`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `builder`.`users_hash`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `builder`.`users_hash` (
  `idusers_hash` INT NOT NULL AUTO_INCREMENT,
  `users_iduser` INT NOT NULL,
  `hash` TEXT(255) NOT NULL,
  PRIMARY KEY (`idusers_hash`),
  INDEX `fk_users_hash_users_idx` (`users_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_users_hash_users`
    FOREIGN KEY (`users_iduser`)
    REFERENCES `builder`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `builder`.`projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `builder`.`projects` (
  `idprojects` INT NOT NULL AUTO_INCREMENT,
  `users_iduser` INT NOT NULL,
  `project_name` VARCHAR(100) NOT NULL,
  `project_path` TEXT(255) NOT NULL,
  PRIMARY KEY (`idprojects`),
  INDEX `fk_projects_users1_idx` (`users_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_projects_users1`
    FOREIGN KEY (`users_iduser`)
    REFERENCES `builder`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `builder`.`sites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `builder`.`sites` (
  `idsites` INT NOT NULL AUTO_INCREMENT,
  `projects_idproject` INT NOT NULL,
  `site_name` VARCHAR(100) NOT NULL,
  `folder_name` VARCHAR(100) NOT NULL,
  `site_json` JSON NOT NULL,
  PRIMARY KEY (`idsites`),
  INDEX `fk_sites_projects1_idx` (`projects_idproject` ASC) VISIBLE,
  CONSTRAINT `fk_sites_projects1`
    FOREIGN KEY (`projects_idproject`)
    REFERENCES `builder`.`projects` (`idprojects`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `builder`.`blocks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `builder`.`blocks` (
  `idblocks` INT NOT NULL AUTO_INCREMENT,
  `users_iduser` INT NOT NULL,
  `block_html` BLOB NOT NULL,
  `block_css` BLOB NOT NULL,
  `block_js` BLOB NULL,
  PRIMARY KEY (`idblocks`),
  INDEX `fk_blocks_users1_idx` (`users_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_blocks_users1`
    FOREIGN KEY (`users_iduser`)
    REFERENCES `builder`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;