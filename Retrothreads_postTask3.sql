-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: retrothreads_group30
-- ------------------------------------------------------
-- Server version	9.6.0

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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '9e73c792-c45a-11f0-87f6-e3d272c27918:1-501,
be55a0db-fdf6-11f0-8efc-78465c419a4a:1-17';

--
-- Table structure for table `celebrity`
--

DROP TABLE IF EXISTS `celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celebrity` (
  `celebrity_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `profession` varchar(100) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  `birth_year` int DEFAULT NULL,
  PRIMARY KEY (`celebrity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celebrity`
--

LOCK TABLES `celebrity` WRITE;
/*!40000 ALTER TABLE `celebrity` DISABLE KEYS */;
INSERT INTO `celebrity` VALUES (1,'Audrey Hepburn','Actress','British',1929),(2,'Princess Diana','Royalty','British',1961),(3,'Madonna','Singer','American',1958),(4,'Aishwarya Rai','Actress','Indian',1973);
/*!40000 ALTER TABLE `celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `designer`
--

DROP TABLE IF EXISTS `designer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `designer` (
  `designer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `birth_year` int DEFAULT NULL,
  `death_year` int DEFAULT NULL,
  `biography` text,
  `nationality` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`designer_id`),
  CONSTRAINT `designer_chk_1` CHECK (((`death_year` is null) or (`death_year` >= `birth_year`)))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `designer`
--

LOCK TABLES `designer` WRITE;
/*!40000 ALTER TABLE `designer` DISABLE KEYS */;
INSERT INTO `designer` VALUES (2,'Christian Dior',1905,1957,'Revolutionized post-war fashion with the \"New Look\".','French'),(3,'Alexander McQueen',1969,2010,'Known for emotional power and raw energy in shows.','British'),(4,'Sabyasachi Mukherjee',1974,NULL,'Celebrated for revitalizing traditional Indian textiles.','Indian'),(5,'xyz',2026,NULL,'GYTTDTY','INDIA');
/*!40000 ALTER TABLE `designer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `era`
--

DROP TABLE IF EXISTS `era`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `era` (
  `era_id` int NOT NULL AUTO_INCREMENT,
  `start_year` int NOT NULL,
  `end_year` int NOT NULL,
  `cultural_context` text,
  PRIMARY KEY (`era_id`),
  CONSTRAINT `era_chk_1` CHECK ((`end_year` >= `start_year`))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `era`
--

LOCK TABLES `era` WRITE;
/*!40000 ALTER TABLE `era` DISABLE KEYS */;
INSERT INTO `era` VALUES (1,1920,1929,'Roaring Twenties: Jazz Age, Flapper culture, liberation of women\'s fashion.'),(2,1947,1957,'The New Look: Post-war return to opulence, defined waists, and full skirts.'),(3,1960,1969,'Swinging Sixties: Mod culture, mini skirts, psychedelic prints, and youth rebellion.'),(4,1990,1999,'The Nineties: Grunge, Minimalism, and the rise of Supermodels.');
/*!40000 ALTER TABLE `era` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_celebrity`
--

DROP TABLE IF EXISTS `event_celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_celebrity` (
  `event_id` int NOT NULL,
  `celebrity_id` int NOT NULL,
  PRIMARY KEY (`event_id`,`celebrity_id`),
  KEY `celebrity_id` (`celebrity_id`),
  CONSTRAINT `event_celebrity_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `provenance_event` (`event_id`) ON DELETE CASCADE,
  CONSTRAINT `event_celebrity_ibfk_2` FOREIGN KEY (`celebrity_id`) REFERENCES `celebrity` (`celebrity_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_celebrity`
--

LOCK TABLES `event_celebrity` WRITE;
/*!40000 ALTER TABLE `event_celebrity` DISABLE KEYS */;
INSERT INTO `event_celebrity` VALUES (3,4);
/*!40000 ALTER TABLE `event_celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garment`
--

DROP TABLE IF EXISTS `garment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garment` (
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
  CONSTRAINT `garment_ibfk_1` FOREIGN KEY (`designer_id`) REFERENCES `designer` (`designer_id`) ON DELETE SET NULL,
  CONSTRAINT `garment_ibfk_2` FOREIGN KEY (`era_id`) REFERENCES `era` (`era_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garment`
--

LOCK TABLES `garment` WRITE;
/*!40000 ALTER TABLE `garment` DISABLE KEYS */;
INSERT INTO `garment` VALUES (1,'1926 Little Black Dress','Original crepe de Chine dress, knee-length.','Good','S','Silk Crepe','img_lbd_1926.jpg','2020-05-15',NULL,1),(2,'1947 Bar Suit','Ivory silk shantung jacket with pleated black wool skirt.','Excellent','M','Silk and Wool','img_bar_suit.jpg','2019-11-20',2,2),(3,'Oyster Dress','Tattered organza gown from the \"Irere\" collection.','Fair','XS','Silk Organza','img_oyster_2003.jpg','2021-03-10',3,4),(4,'Bridal Lehenga 1999','Hand-embroidered velvet lehenga with zardosi work.','Good','L','Velvet','img_sabya_1999.jpg','2023-01-05',4,4),(5,'2026HBJE','Original ADVH knee-length.','Good','S','Silk Crepe','img_lBFDH.jpg','2020-05-15',NULL,1);
/*!40000 ALTER TABLE `garment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garment_style`
--

DROP TABLE IF EXISTS `garment_style`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garment_style` (
  `garment_id` int NOT NULL,
  `style_id` int NOT NULL,
  PRIMARY KEY (`garment_id`,`style_id`),
  KEY `style_id` (`style_id`),
  CONSTRAINT `garment_style_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `garment` (`garment_id`) ON DELETE CASCADE,
  CONSTRAINT `garment_style_ibfk_2` FOREIGN KEY (`style_id`) REFERENCES `style_attribute` (`style_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garment_style`
--

LOCK TABLES `garment_style` WRITE;
/*!40000 ALTER TABLE `garment_style` DISABLE KEYS */;
INSERT INTO `garment_style` VALUES (1,1),(2,1),(4,2),(1,3),(3,4);
/*!40000 ALTER TABLE `garment_style` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing`
--

DROP TABLE IF EXISTS `listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listing` (
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
  CONSTRAINT `listing_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `garment` (`garment_id`),
  CONSTRAINT `listing_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `listing_chk_1` CHECK ((`price` > 0)),
  CONSTRAINT `listing_chk_2` CHECK ((`rating` between 0 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing`
--

LOCK TABLES `listing` WRITE;
/*!40000 ALTER TABLE `listing` DISABLE KEYS */;
INSERT INTO `listing` VALUES (1,1,2,15000.00,'2025-02-01','active',NULL),(2,2,1,25000.50,'2025-01-20','sold',4.8),(3,4,1,8500.00,'2025-02-10','active',4.5);
/*!40000 ALTER TABLE `listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provenance_event`
--

DROP TABLE IF EXISTS `provenance_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provenance_event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `garment_id` int NOT NULL,
  `event_name` varchar(150) DEFAULT NULL,
  `event_type` varchar(100) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `description` text,
  `location` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `idx_provenance_garment` (`garment_id`),
  CONSTRAINT `provenance_event_ibfk_1` FOREIGN KEY (`garment_id`) REFERENCES `garment` (`garment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provenance_event`
--

LOCK TABLES `provenance_event` WRITE;
/*!40000 ALTER TABLE `provenance_event` DISABLE KEYS */;
INSERT INTO `provenance_event` VALUES (1,2,'The New Look Launch','Runway Show','1947-02-12','Debut of the Corolla collection, later dubbed the New Look.','Paris, France'),(2,3,'Savage Beauty Exhibition','Museum Exhibition','2011-05-04','Retrospective of McQueen work at the Met.','New York, USA'),(3,4,'Cannes Film Festival','Red Carpet','2003-05-20','Worn specifically for the premiere gala.','Cannes, France');
/*!40000 ALTER TABLE `provenance_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `style_attribute`
--

DROP TABLE IF EXISTS `style_attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `style_attribute` (
  `style_id` int NOT NULL AUTO_INCREMENT,
  `style_type` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`style_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `style_attribute`
--

LOCK TABLES `style_attribute` WRITE;
/*!40000 ALTER TABLE `style_attribute` DISABLE KEYS */;
INSERT INTO `style_attribute` VALUES (1,'Silhouette','The overall shape or outline of the garment.'),(2,'Embroidery','Decorative needlework using thread or yarn.'),(3,'Minimalist','Clean lines, monochromatic palettes, lack of clutter.'),(4,'Avant-Garde','Experimental, innovative, and pushing boundaries.');
/*!40000 ALTER TABLE `style_attribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `listing_id` int NOT NULL,
  `buyer_id` int NOT NULL,
  `final_price` decimal(10,2) DEFAULT NULL,
  `transaction_date` date DEFAULT (curdate()),
  `payment_status` enum('pending','completed','failed') DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `listing_id` (`listing_id`),
  KEY `idx_transaction_buyer` (`buyer_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`listing_id`) REFERENCES `listing` (`listing_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,2,3,25000.50,'2025-01-25','completed');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ananya Rao','ananya.r@museum.in','seller','2025-01-10','hash123','919876543210'),(2,'Marco Bianchi','marco.b@vintage.it','seller','2025-01-12','hash456','390123456789'),(3,'Oliver Grant','oliver.g@fashion.uk','buyer','2025-01-15','hash789','447123456789'),(4,'Dr. Cindney Belsville','cindney.b@uni.ru','admin','2025-01-01','hashadmin','79123456789'),(5,'Riya Mehta','riya.m@student.in','buyer','2025-02-01','hashstudent','919988776655');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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

-- Dump completed on 2026-02-09 12:18:17
