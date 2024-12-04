-- MySQL Script generated by MySQL Workbench
-- Sat Nov 30 19:29:27 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`ingredient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ingredient` (
  `idingredient` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `amount` INT NOT NULL,
  `price` FLOAT NOT NULL,
  `description` VARCHAR(200) NULL,
  `product_type` VARCHAR(15) NOT NULL,
  `image_path` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idingredient`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `price` FLOAT NOT NULL,
  `description` VARCHAR(200) NULL,
  `image_path` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idproduct`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`order` (
  `idorder` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `total` FLOAT NOT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`idorder`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ingredient_has_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ingredient_has_product` (
  `ingredient_idingredient` INT NOT NULL,
  `product_idproduct` INT NOT NULL,
  PRIMARY KEY (`ingredient_idingredient`, `product_idproduct`),
  INDEX `fk_ingredient_has_product_product1_idx` (`product_idproduct` ASC) VISIBLE,
  INDEX `fk_ingredient_has_product_ingredient_idx` (`ingredient_idingredient` ASC) VISIBLE,
  CONSTRAINT `fk_ingredient_has_product_ingredient`
    FOREIGN KEY (`ingredient_idingredient`)
    REFERENCES `mydb`.`ingredient` (`idingredient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ingredient_has_product_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `mydb`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`product_has_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`product_has_order` (
  `product_idproduct` INT NOT NULL,
  `order_idorder` INT NOT NULL,
  PRIMARY KEY (`product_idproduct`, `order_idorder`),
  INDEX `fk_product_has_order_order1_idx` (`order_idorder` ASC) VISIBLE,
  INDEX `fk_product_has_order_product1_idx` (`product_idproduct` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_order_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `mydb`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_order_order1`
    FOREIGN KEY (`order_idorder`)
    REFERENCES `mydb`.`order` (`idorder`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`order_entry_wraper`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`order_entry_wraper` (
  `idorder_product_wraper` INT NOT NULL AUTO_INCREMENT,
  `amount` INT NULL,
  `subtotal` FLOAT NULL,
  `product_idproduct` INT NOT NULL,
  `order_idorder` INT NOT NULL,
  PRIMARY KEY (`idorder_product_wraper`),
  INDEX `fk_order_product_wraper_product1_idx` (`product_idproduct` ASC) VISIBLE,
  INDEX `fk_order_product_wraper_order1_idx` (`order_idorder` ASC) VISIBLE,
  CONSTRAINT `fk_order_product_wraper_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `mydb`.`product` (`idproduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_product_wraper_order1`
    FOREIGN KEY (`order_idorder`)
    REFERENCES `mydb`.`order` (`idorder`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;