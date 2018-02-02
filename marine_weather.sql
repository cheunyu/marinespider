/*
SQLyog  v12.2.6 (64 bit)
MySQL - 5.7.19 : Database - marine_weather
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`marine_weather` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `marine_weather`;

/*Table structure for table `coastal` */

DROP TABLE IF EXISTS `coastal`;

CREATE TABLE `coastal` (
  `ID` int(4) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT '主键',
  `OCEAN_NAME` varchar(10) NOT NULL COMMENT '海区名称',
  `FORECAST_TIME` varchar(10) NOT NULL COMMENT '预报时间',
  `PHENOMENON` varchar(10) NOT NULL COMMENT '天气现象',
  `WIND_DIRECTION` varchar(10) NOT NULL COMMENT '风向',
  `WIND_POWER` varchar(10) NOT NULL COMMENT '风力',
  `VISIBILITY` varchar(10) NOT NULL COMMENT '能见度',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`ID`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;