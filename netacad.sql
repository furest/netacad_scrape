-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 14, 2019 at 08:05 PM
-- Server version: 10.1.38-MariaDB-0+deb9u1
-- PHP Version: 7.0.33-0+deb9u3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `netacad`
--

-- --------------------------------------------------------

--
-- Table structure for table `academies`
--

CREATE TABLE `academies` (
  `ID` int(11) NOT NULL,
  `name` mediumtext NOT NULL,
  `street` mediumtext NOT NULL,
  `locality` mediumtext NOT NULL,
  `state` mediumtext NOT NULL,
  `country_code` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `countries`
--

CREATE TABLE `countries` (
  `country_code` varchar(4) NOT NULL,
  `country` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academies`
--
ALTER TABLE `academies`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `academies_FK_country_code` (`country_code`);

--
-- Indexes for table `countries`
--
ALTER TABLE `countries`
  ADD PRIMARY KEY (`country_code`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academies`
--
ALTER TABLE `academies`
  ADD CONSTRAINT `academies_FK_country_code` FOREIGN KEY (`country_code`) REFERENCES `countries` (`country_code`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
