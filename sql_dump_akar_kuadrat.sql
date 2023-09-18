/*
SQLyog Ultimate v12.5.1 (64 bit)
MySQL - 10.4.25-MariaDB : Database - db-square-root
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db-square-root` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `db-square-root`;

/*Table structure for table `logs` */

DROP TABLE IF EXISTS `logs`;

CREATE TABLE `logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `input` double DEFAULT NULL,
  `hasil` double DEFAULT NULL,
  `waktu` double DEFAULT NULL,
  `jenis` char(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `logs` */

/* Procedure structure for procedure `square_root` */

/*!50003 DROP PROCEDURE IF EXISTS  `square_root` */;

DELIMITER $$

/*!50003 CREATE DEFINER=`root`@`localhost` PROCEDURE `square_root`(IN input DOUBLE, OUT output DOUBLE, OUT timeoutput DOUBLE)
BEGIN
		DECLARE hasil DOUBLE;
		DECLARE tebak DOUBLE;
		DECLARE toleransi DOUBLE;
		
		SET hasil = input/2;
		SET tebak = 0;
		SET toleransi = 0.00001;
		
		SET @mulai = now(6)+0;
		WHILE abs(hasil - tebak) > toleransi DO
			SET tebak = hasil;
			SET hasil = 0.5 * (hasil + (input/hasil));
		END WHILE;
		SET @akhir = NOW(6)+0;
		SET @waktu = @akhir - @mulai;
		
		INSERT INTO `logs`(input, hasil, waktu, jenis, created_at, updated_at)
		VALUES(
			input,
			hasil,
			@waktu,
			'PL-SQL',
			NOW(),
			NOW()
		);
		
		set output = hasil;
		SET timeoutput = @waktu;
	END */$$
DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
