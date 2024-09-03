/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - debtease
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`debtease` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `debtease`;

/*Table structure for table `canteen` */

DROP TABLE IF EXISTS `canteen`;

CREATE TABLE `canteen` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `lid` int(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pin` bigint(100) DEFAULT NULL,
  `phone` bigint(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `license` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `canteen` */

insert  into `canteen`(`id`,`lid`,`name`,`place`,`post`,`pin`,`phone`,`email`,`license`) values 
(6,17,'canteen1','Kottayam','pambady',671313,8647696661,'canteen@gmail.com','20210728_101537168.jpg'),
(7,19,'canteen2','cheruvathur','cheruvathur',671313,8647696661,'canteen2@gmail.com','abhi_sign.jpg');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `user_id` int(100) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`id`,`user_id`,`complaint`,`date`,`reply`) values 
(3,18,'kjbh','hkh','jnm');

/*Table structure for table `debtdetails` */

DROP TABLE IF EXISTS `debtdetails`;

CREATE TABLE `debtdetails` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `canteen_id` int(100) DEFAULT NULL,
  `user_id` int(100) DEFAULT NULL,
  `amount` bigint(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `debtdetails` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`id`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(17,'canteen1','canteen1','canteen'),
(18,'abhi','abhi','user'),
(19,'canteen2','canteen2','pending');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `lid` int(100) DEFAULT NULL,
  `canteen_id` int(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `id_details` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` bigint(100) DEFAULT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`id`,`lid`,`canteen_id`,`name`,`id_details`,`email`,`phone`,`profile_photo`) values 
(4,18,17,'abhilash','Screenshot_20231201-2321162.png','abhi@gmail.com',9188641904,'Abhi_photo.jpg');

/*Table structure for table `wallet` */

DROP TABLE IF EXISTS `wallet`;

CREATE TABLE `wallet` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `lid` int(100) DEFAULT NULL,
  `amount` bigint(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `wallet` */

insert  into `wallet`(`id`,`lid`,`amount`) values 
(2,18,2233);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
