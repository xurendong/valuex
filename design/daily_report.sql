/*
Navicat MySQL Data Transfer

Source Server         : 10.0.7.53
Source Server Version : 50717
Source Host           : 10.0.7.53:3306
Source Database       : clearx

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-01-31 16:10:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for daily_report
-- ----------------------------
DROP TABLE IF EXISTS `daily_report`;
CREATE TABLE `daily_report` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增序号',
  `trade_date` date NOT NULL COMMENT '交易日期',
  `account_id` varchar(32) NOT NULL COMMENT '账户编号',
  `net_unit` double(16,4) DEFAULT '0.00' COMMENT '单位净值',
  `net_cumulative` double(16,4) DEFAULT '0.00' COMMENT '累计净值',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_trade_date_account_id` (`trade_date`,`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
