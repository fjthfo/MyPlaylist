-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
SELECT * FROM comment where playlist_id ='1';

-- SET foreign_key_checks = 1;

TRUNCATE comment; 
create table test select track_id, SUBSTRING_INDEX(SUBSTRING_INDEX(artist_genres, '\'', 2),'\'',-1) AS genre from song;
Insert Into test (select track_id, SUBSTRING_INDEX(SUBSTRING_INDEX(artist_genres, '\'', 4),'\'',-1) AS genre from song);
Insert Into test (select track_id, SUBSTRING_INDEX(SUBSTRING_INDEX(artist_genres, '\'', 6),'\'',-1) AS genre from song);
Insert Into test (select track_id, SUBSTRING_INDEX(SUBSTRING_INDEX(artist_genres, '\'', 8),'\'',-1) AS genre from song);
select * into outfile "/Users/afo/Documents/USW/3-2/database/장르_1128.csv" fields terminated by ',' enclosed by "" escaped by '\\' lines terminated by '\n'from test;
-- show variables like 'secure_file%';
-- SHOW VARIABLES LIKE "secure_file_priv";
-- SELECT @@GLOBAL.secure_file_priv;

-- select artist_genres from song where track_id='0203aGEIzVVlmvQ8lX4fmV';
-- SELECT * FROM myplaylistdb.Song;
-- alter table song drop column artist_genres;
-- ALTER TABLE playlist ADD UNIQUE (user_id, Song_track_id);

-- select * FROM track where Playlist_user_id ='fjthfo' and Song_track_id = '0b5xMWDVHK7SSZI0Lr2iNg';

-- 노래 검색
-- SELECT DISTINCT * FROM (select a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(b.genre) AS genres FROM song a LEFT JOIN genres b ON a.track_id = b.Song_track_id GROUP BY a.track_id) AS a WHERE a.track_name LIKE '%%%je%%' OR a.artist_name LIKE '%%%je%%';
-- 내 플리 노래 조회
-- SELECT DISTINCT * FROM (SELECT a.track_name, a.artist_name, a.track_id, GROUP_CONCAT(b.genre) AS genres FROM song a INNER JOIN genres b ON a.track_id = b.Song_track_id GROUP BY a.track_id) c where track_id IN( SELECT Song_track_id from track where Playlist_user_id = 'wngur');
-- select track_name, artist_name, track_id from song where track_name ="2step";
-- 중복 제거--
-- delete from song where track_id in (select track_id from( select ROW_NUMBER() OVER (PARTITION BY track_name order by track_id) a, track_id from song ) b where a >1 );

-- SELECT track_name, artist_name from track INNER JOIN song ON track.Song_track_id = song.track_id;


-- comment 자동증가
-- ALTER TABLE comment MODIFY comment_id int AUTO_INCREMENT;

-- -----------------------------------------------------
-- Schema myplaylistdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema myplaylistdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `myplaylistdb` DEFAULT CHARACTER SET utf8mb3 ;
USE `myplaylistdb` ;

-- -----------------------------------------------------
-- Table `myplaylistdb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`User` (
  `id` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  `gender` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `myplaylistdb`.`Playlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`Playlist` (
  `playlist_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(45) NOT NULL,
  `title` VARCHAR(255) NULL,
  `describe` VARCHAR(255) NULL,
  `hashtag` VARCHAR(255) NULL,
  `recommend` INT(45) NULL,
  INDEX `fk_Playlist_user1_idx` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`playlist_id`, `user_id`),
  CONSTRAINT `fk_Playlist_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `myplaylistdb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `myplaylistdb`.`Song`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`Song` (
  `track_id` VARCHAR(255) NOT NULL,
  `track_name` VARCHAR(255) NOT NULL,
  `artist_id` VARCHAR(255) NOT NULL,
  `artist_name` VARCHAR(255) NOT NULL,
  `artist_genres` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`track_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

- -----------------------------------------------------
-- Table `myplaylistdb`.`Genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`Genres` (
  `track_id` VARCHAR(255) NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  INDEX `fk_table1_Song1_idx` (`track_id` ASC) VISIBLE,
  CONSTRAINT `fk_table1_Song1`
    FOREIGN KEY (`track_id`)
    REFERENCES `myplaylistdb`.`Song` (`track_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myplaylistdb`.`Track`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`Track` (
  `track_id` VARCHAR(255) NOT NULL,
  `user_id` VARCHAR(45) NOT NULL,
  INDEX `fk_track_Song1_idx` (`track_id` ASC) VISIBLE,
  PRIMARY KEY (`track_id`),
  INDEX `fk_track_Playlist1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_track_Song1`
    FOREIGN KEY (`track_id`)
    REFERENCES `myplaylistdb`.`Song` (`track_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_track_Playlist1`
    FOREIGN KEY (`user_id`)
    REFERENCES `myplaylistdb`.`Playlist` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `myplaylistdb`.`Comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `myplaylistdb`.`Comment` (
  `playlist_id` INT NOT NULL,
  `user_id` VARCHAR(45) NOT NULL,
  `body` VARCHAR(255) NOT NULL,
  INDEX `fk_Comment_User1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_Comment_Playlist1_idx` (`playlist_id` ASC) VISIBLE,
  CONSTRAINT `fk_Comment_User1`
    FOREIGN KEY (`user_id`)
    REFERENCES `myplaylistdb`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comment_Playlist1`
    FOREIGN KEY (`playlist_id`)
    REFERENCES `myplaylistdb`.`Playlist` (`playlist_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
