CREATE DATABASE  IF NOT EXISTS `retrothreads_group30` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `retrothreads_group30`;
-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (x86_64)
--
-- Host: 192.168.41.16    Database: retrothreads_group30
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '9e73c792-c45a-11f0-87f6-e3d272c27918:1-501';

--
-- Table structure for table `Celebrity`
--

DROP TABLE IF EXISTS `Celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Celebrity` (
  `celebrity_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `profession` varchar(100) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  `birth_year` int DEFAULT NULL,
  PRIMARY KEY (`celebrity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Celebrity`
--

LOCK TABLES `Celebrity` WRITE;
/*!40000 ALTER TABLE `Celebrity` DISABLE KEYS */;
/*!40000 ALTER TABLE `Celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Designer`
--

DROP TABLE IF EXISTS `Designer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Designer` (
  `designer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `birth_year` int DEFAULT NULL,
  `death_year` int DEFAULT NULL,
  `biography` text,
  `nationality` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`designer_id`),
  CONSTRAINT `designer_chk_1` CHECK (((`death_year` is null) or (`death_year` >= `birth_year`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Designer`
--

LOCK TABLES `Designer` WRITE;
/*!40000 ALTER TABLE `Designer` DISABLE KEYS */;
/*!40000 ALTER TABLE `Designer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Era`
--

DROP TABLE IF EXISTS `Era`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Era` (
  `era_id` int NOT NULL AUTO_INCREMENT,
  `start_year` int NOT NULL,
  `end_year` int NOT NULL,
  `cultural_context` text,
  PRIMARY KEY (`era_id`),
  CONSTRAINT `era_chk_1` CHECK ((`end_year` >= `start_year`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Era`
--

LOCK TABLES `Era` WRITE;
/*!40000 ALTER TABLE `Era` DISABLE KEYS */;
/*!40000 ALTER TABLE `Era` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Event_Celebrity`
--

DROP TABLE IF EXISTS `Event_Celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Event_Celebrity` (
  `event_id` int NOT NULL,
  `celebrity_id` int NOT NULL,
  PRIMARY KEY (`event_id`,`celebrity_id`),
  KEY `celebrity_id` (`celebrity_id`),
  CONSTRAINT `event_celebrity_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `Provenance_event` (`event_id`) ON DELETE CASCADE,
  CONSTRAINT `event_celebrity_ibfk_2` FOREIGN KEY (`celebrity_id`) REFERENCES `Celebrity` (`celebrity_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Event_Celebrity`
--

LOCK TABLES `Event_Celebrity` WRITE;
/*!40000 ALTER TABLE `Event_Celebrity` DISABLE KEYS */;
/*!40000 ALTER TABLE `Event_Celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Garment`
--

DROP TABLE IF EXISTS `Garment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Garment` (
  `garment_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `description` text,
  `condition` enum('Excellent','Good','Fair','Poor') DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `material` varchar(100) DEFAULT NULL,
  `image_reference` text,
  `date_acquired` date DEFAULT NULL,
  `designer_id` int DEFAULT NULL,
  `era_id` int DEFAULT NULL,
  PRIMARY KEY (`garment_id`),
  KEY `idx_garment_designer` (`designer_id`),
  KEY `idx_garment_era` (`era_id`),
  CONSTRAINT `garment_ibfk_1` FOREIGN KEY (`designer_id`) REFERENCES `Designer` (`designer_id`) ON DELETE SET NULL,
  CONSTRAINT `garment_ibfk_2` FOREIGN KEY (`era_id`) REFERENCES `Era` (`era_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Garment`
--

LOCK TABLES `Garment` WRITE;
/*!40000 ALTER TABLE `Garment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Garment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Garment_Style`
--

DROP TABLE IF EXISTS `Garment_Style`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Garment_Style` (
  `garment_id` int NOT NULL,
  `style_id` int NOT NULL,
  PRIMARY KEY (`garment_id`,`style_id`),
  KEY `style_id` (`style_id`),
  CONSTRAINT `garment_style_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `Garment` (`garment_id`) ON DELETE CASCADE,
  CONSTRAINT `garment_style_ibfk_2` FOREIGN KEY (`style_id`) REFERENCES `Style_attribute` (`style_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Garment_Style`
--

LOCK TABLES `Garment_Style` WRITE;
/*!40000 ALTER TABLE `Garment_Style` DISABLE KEYS */;
/*!40000 ALTER TABLE `Garment_Style` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Listing`
--

DROP TABLE IF EXISTS `Listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Listing` (
  `listing_id` int NOT NULL AUTO_INCREMENT,
  `garment_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `listing_date` date DEFAULT (curdate()),
  `status` enum('active','sold','cancelled') DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  PRIMARY KEY (`listing_id`),
  KEY `garment_id` (`garment_id`),
  KEY `idx_listing_seller` (`seller_id`),
  CONSTRAINT `listing_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `Garment` (`garment_id`),
  CONSTRAINT `listing_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `Users` (`user_id`),
  CONSTRAINT `listing_chk_1` CHECK ((`price` > 0)),
  CONSTRAINT `listing_chk_2` CHECK ((`rating` between 0 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Listing`
--

LOCK TABLES `Listing` WRITE;
/*!40000 ALTER TABLE `Listing` DISABLE KEYS */;
/*!40000 ALTER TABLE `Listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Provenance_event`
--

DROP TABLE IF EXISTS `Provenance_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Provenance_event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `garment_id` int NOT NULL,
  `event_name` varchar(150) DEFAULT NULL,
  `event_type` varchar(100) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `description` text,
  `location` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `idx_provenance_garment` (`garment_id`),
  CONSTRAINT `provenance_event_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `Garment` (`garment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Provenance_event`
--

LOCK TABLES `Provenance_event` WRITE;
/*!40000 ALTER TABLE `Provenance_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `Provenance_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Style_attribute`
--

DROP TABLE IF EXISTS `Style_attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Style_attribute` (
  `style_id` int NOT NULL AUTO_INCREMENT,
  `style_type` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`style_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Style_attribute`
--

LOCK TABLES `Style_attribute` WRITE;
/*!40000 ALTER TABLE `Style_attribute` DISABLE KEYS */;
/*!40000 ALTER TABLE `Style_attribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Transactions`
--

DROP TABLE IF EXISTS `Transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `listing_id` int NOT NULL,
  `buyer_id` int NOT NULL,
  `final_price` decimal(10,2) DEFAULT NULL,
  `transaction_date` date DEFAULT (curdate()),
  `payment_status` enum('pending','completed','failed') DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `listing_id` (`listing_id`),
  KEY `idx_transaction_buyer` (`buyer_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `Listing` (`listing_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Transactions`
--

LOCK TABLES `Transactions` WRITE;
/*!40000 ALTER TABLE `Transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `role` enum('buyer','seller','admin') DEFAULT NULL,
  `registration_date` date DEFAULT (curdate()),
  `password_hash` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-30 13:11:15
