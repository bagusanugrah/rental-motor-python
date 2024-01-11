-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for rental_motor
CREATE DATABASE IF NOT EXISTS `rental_motor` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `rental_motor`;

-- Dumping structure for table rental_motor.motor
CREATE TABLE IF NOT EXISTS `motor` (
  `plat_nomor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `merek` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `tipe` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `sewa_perhari` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_pemilik` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`plat_nomor`),
  KEY `id_pemilik` (`id_pemilik`),
  CONSTRAINT `motor_ibfk_1` FOREIGN KEY (`id_pemilik`) REFERENCES `pemilik` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rental_motor.pemilik
CREATE TABLE IF NOT EXISTS `pemilik` (
  `username` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `nik` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rental_motor.pengembalian
CREATE TABLE IF NOT EXISTS `pengembalian` (
  `id_pengembalian` int NOT NULL AUTO_INCREMENT,
  `tgl_penyewaan` date NOT NULL,
  `tgl_pengembalian` date NOT NULL,
  `plat_nomor` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_penyewaan` int NOT NULL,
  PRIMARY KEY (`id_pengembalian`),
  KEY `id_penyewaan` (`id_penyewaan`),
  CONSTRAINT `pengembalian_ibfk_1` FOREIGN KEY (`id_penyewaan`) REFERENCES `penyewaan` (`id_penyewaan`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rental_motor.penyewa
CREATE TABLE IF NOT EXISTS `penyewa` (
  `username` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `nik` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rental_motor.penyewaan
CREATE TABLE IF NOT EXISTS `penyewaan` (
  `id_penyewaan` int NOT NULL AUTO_INCREMENT,
  `tgl_penyewaan` date NOT NULL,
  `tgl_pengembalian` date DEFAULT NULL,
  `merek_motor` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `tipe_motor` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `plat_nomor` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `id_pemilik` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `sewa_perhari` int NOT NULL,
  `id_penyewa` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_penyewaan`),
  KEY `id_penyewa` (`id_penyewa`),
  KEY `plat_nomor` (`plat_nomor`),
  CONSTRAINT `penyewaan_ibfk_1` FOREIGN KEY (`id_penyewa`) REFERENCES `penyewa` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `plat_nomor` FOREIGN KEY (`plat_nomor`) REFERENCES `motor` (`plat_nomor`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
