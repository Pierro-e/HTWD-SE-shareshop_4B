-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 141.56.137.83    Database: share_shop
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.1

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

--
-- Table structure for table `Bedarfsvorhersage`
--

DROP TABLE IF EXISTS `Bedarfsvorhersage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Bedarfsvorhersage` (
  `nutzer_id` int NOT NULL,
  `produkt_id` int NOT NULL,
  `counter` decimal(10,2) DEFAULT '0.00',
  `last_bought` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`nutzer_id`,`produkt_id`),
  KEY `Bedarfsvorhersage_ibfk_2` (`produkt_id`),
  CONSTRAINT `Bedarfsvorhersage_ibfk_1` FOREIGN KEY (`nutzer_id`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Bedarfsvorhersage_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `Produkt` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Einheiten`
--

DROP TABLE IF EXISTS `Einheiten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Einheiten` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `abkürzung` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Einheiten`
--

LOCK TABLES `Einheiten` WRITE;
/*!40000 ALTER TABLE `Einheiten` DISABLE KEYS */;
INSERT INTO `Einheiten` VALUES (1,'Kilogramm','kg'),(2,'Liter','L'),(3,'Stück','stk');
/*!40000 ALTER TABLE `Einheiten` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Einkaufsarchiv`
--

DROP TABLE IF EXISTS `Einkaufsarchiv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Einkaufsarchiv` (
  `einkauf_id` int NOT NULL AUTO_INCREMENT,
  `listen_id` int NOT NULL,
  `eingekauft_von` int DEFAULT NULL,
  `eingekauft_am` date DEFAULT NULL,
  `gesamtpreis` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`einkauf_id`),
  KEY `listen_id` (`listen_id`),
  KEY `getätigt_von` (`eingekauft_von`),
  CONSTRAINT `Einkaufsarchiv_ibfk_1` FOREIGN KEY (`listen_id`) REFERENCES `Listen` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Einkaufsarchiv_ibfk_2` FOREIGN KEY (`eingekauft_von`) REFERENCES `Nutzer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Kostenaufteilung`
--

DROP TABLE IF EXISTS `Kostenaufteilung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Kostenaufteilung` (
  `empfaenger_id` int NOT NULL,
  `schuldner_id` int NOT NULL,
  `betrag` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`empfaenger_id`,`schuldner_id`),
  KEY `empfaenger_id` (`empfaenger_id`),
  KEY `schuldner_id` (`schuldner_id`),
  CONSTRAINT `Kostenaufteilung_ibfk_1` FOREIGN KEY (`schuldner_id`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Kostenaufteilung_ibfk_2` FOREIGN KEY (`empfaenger_id`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ListeMitglieder`
--

DROP TABLE IF EXISTS `ListeMitglieder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ListeMitglieder` (
  `listen_id` int NOT NULL,
  `nutzer_id` int NOT NULL,
  `beigetreten_am` date DEFAULT NULL,
  PRIMARY KEY (`listen_id`,`nutzer_id`),
  KEY `nutzer_id` (`nutzer_id`),
  CONSTRAINT `ListeMitglieder_ibfk_1` FOREIGN KEY (`listen_id`) REFERENCES `Listen` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ListeMitglieder_ibfk_2` FOREIGN KEY (`nutzer_id`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ListeProdukte`
--

DROP TABLE IF EXISTS `ListeProdukte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ListeProdukte` (
  `listen_id` int NOT NULL,
  `produkt_id` int NOT NULL,
  `produkt_menge` decimal(10,2) DEFAULT NULL,
  `einheit_id` int DEFAULT NULL,
  `hinzugefügt_von` int NOT NULL,
  `beschreibung` text,
  PRIMARY KEY (`listen_id`,`produkt_id`,`hinzugefügt_von`),
  KEY `produkt_id` (`produkt_id`),
  KEY `einheit_id` (`einheit_id`),
  KEY `FK_ListeProdukte_hinzugefuegt_von` (`hinzugefügt_von`),
  CONSTRAINT `FK_ListeProdukte_hinzugefuegt_von` FOREIGN KEY (`hinzugefügt_von`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ListeProdukte_ibfk_1` FOREIGN KEY (`listen_id`) REFERENCES `Listen` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ListeProdukte_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `Produkt` (`id`),
  CONSTRAINT `ListeProdukte_ibfk_3` FOREIGN KEY (`einheit_id`) REFERENCES `Einheiten` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Listen`
--

DROP TABLE IF EXISTS `Listen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Listen` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `ersteller` int DEFAULT NULL,
  `datum` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_listen_ersteller` (`ersteller`),
  CONSTRAINT `fk_listen_ersteller` FOREIGN KEY (`ersteller`) REFERENCES `Nutzer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Nutzer`
--

DROP TABLE IF EXISTS `Nutzer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Nutzer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `name` varchar(150) NOT NULL,
  `passwort_hash` varchar(255) NOT NULL,
  `theme` int DEFAULT '0',
  `color` int DEFAULT '0',
  `DecayDays` decimal(10,2) DEFAULT '7.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Produkt`
--

DROP TABLE IF EXISTS `Produkt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Produkt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `eingekaufte_Produkte`
--

DROP TABLE IF EXISTS `eingekaufte_Produkte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eingekaufte_Produkte` (
  `id` int NOT NULL AUTO_INCREMENT,
  `einkauf_id` int NOT NULL,
  `produkt_id` int NOT NULL,
  `produkt_menge` decimal(10,2) DEFAULT NULL,
  `einheit_id` int DEFAULT NULL,
  `produkt_preis` decimal(10,2) DEFAULT NULL,
  `hinzugefuegt_von` int DEFAULT NULL,
  `beschreibung` text,
  PRIMARY KEY (`id`),
  KEY `produkt_id` (`produkt_id`),
  KEY `hinzugefügt_von` (`hinzugefuegt_von`),
  KEY `eingekaufte_Produkte_ibfk_1` (`einkauf_id`),
  KEY `eingekaufte_Produkte_ibfk_3` (`einheit_id`),
  CONSTRAINT `eingekaufte_Produkte_ibfk_1` FOREIGN KEY (`einkauf_id`) REFERENCES `Einkaufsarchiv` (`einkauf_id`) ON DELETE CASCADE,
  CONSTRAINT `eingekaufte_Produkte_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `Produkt` (`id`),
  CONSTRAINT `eingekaufte_Produkte_ibfk_3` FOREIGN KEY (`einheit_id`) REFERENCES `Einheiten` (`id`),
  CONSTRAINT `eingekaufte_Produkte_ibfk_4` FOREIGN KEY (`hinzugefuegt_von`) REFERENCES `Nutzer` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=186 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fav_Produkte`
--

DROP TABLE IF EXISTS `fav_Produkte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fav_Produkte` (
  `nutzer_id` int NOT NULL,
  `produkt_id` int NOT NULL,
  `menge` decimal(10,2) DEFAULT NULL,
  `einheit_id` int DEFAULT NULL,
  `beschreibung` text,
  PRIMARY KEY (`nutzer_id`,`produkt_id`),
  KEY `produkt_id` (`produkt_id`),
  KEY `einheit_id` (`einheit_id`),
  CONSTRAINT `fav_Produkte_ibfk_1` FOREIGN KEY (`nutzer_id`) REFERENCES `Nutzer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fav_Produkte_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `Produkt` (`id`),
  CONSTRAINT `fav_Produkte_ibfk_3` FOREIGN KEY (`einheit_id`) REFERENCES `Einheiten` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-12 16:44:25
