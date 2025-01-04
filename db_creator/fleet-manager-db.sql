-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql:3306
-- Generation Time: Jan 04, 2025 at 02:06 PM
-- Server version: 8.0.40
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `assignments`
--
CREATE DATABASE IF NOT EXISTS `assignments` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `assignments`;

-- --------------------------------------------------------

--
-- Table structure for table `assignments`
--

CREATE TABLE `assignments` (
  `assignment_id` int NOT NULL,
  `driver_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `status` enum('completed','active','cancelled','scheduled') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `assignments`
--

INSERT INTO `assignments` (`assignment_id`, `driver_id`, `vehicle_id`, `start_date_time`, `end_date_time`, `status`) VALUES
(1, 1, 3, '2024-11-01 08:00:00', '2024-11-10 18:00:00', 'completed'),
(2, 2, 5, '2024-11-15 09:00:00', NULL, 'active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assignments`
--
ALTER TABLE `assignments`
  ADD PRIMARY KEY (`assignment_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assignments`
--
ALTER TABLE `assignments`
  MODIFY `assignment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Database: `driver_management`
--
CREATE DATABASE IF NOT EXISTS `driver_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `driver_management`;

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `driver_id` int NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `license_no` varchar(50) NOT NULL,
  `contact_info` varchar(100) NOT NULL,
  `sex` enum('Male','Female') NOT NULL,
  `status` enum('available','assigned','active','unavailable') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`driver_id`, `first_name`, `last_name`, `license_no`, `contact_info`, `sex`, `status`) VALUES
(1, 'Cherilynn', 'Pentony', 'D7745610393', '777-742-0696', 'Female', 'available'),
(2, 'Alethea', 'Rosewarne', 'D9570556013', '659-403-6683', 'Female', 'available'),
(3, 'Thayne', 'Ybarra', 'D2719105966', '148-389-8149', 'Male', 'available'),
(4, 'Hurley', 'Chasney', 'D4174458537', '192-973-7284', 'Male', 'available'),
(5, 'Miriam', 'Masette', 'D6285165706', '279-244-7217', 'Female', 'available');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`driver_id`),
  ADD UNIQUE KEY `license_no` (`license_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `drivers`
--
ALTER TABLE `drivers`
  MODIFY `driver_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- Database: `fuel_consumption`
--
CREATE DATABASE IF NOT EXISTS `fuel_consumption` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `fuel_consumption`;

-- --------------------------------------------------------

--
-- Table structure for table `fuel_consumption`
--

CREATE TABLE `fuel_consumption` (
  `fuel_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `date` date NOT NULL,
  `amount` float NOT NULL,
  `cost` float NOT NULL,
  `mileage` int DEFAULT NULL,
  `fuel_type` enum('petrol','diesel','not_specified') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fuel_consumption`
--
ALTER TABLE `fuel_consumption`
  ADD PRIMARY KEY (`fuel_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fuel_consumption`
--
ALTER TABLE `fuel_consumption`
  MODIFY `fuel_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Database: `maintenance`
--
CREATE DATABASE IF NOT EXISTS `maintenance` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `maintenance`;

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_logs`
--

CREATE TABLE `maintenance_logs` (
  `maintenance_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `maintenance_type` enum('routine','repair','unspecified') NOT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `expected_completion_date_time` datetime DEFAULT NULL,
  `cost` float DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `parts_used` varchar(255) DEFAULT NULL,
  `status` enum('scheduled','ongoing','cancelled','completed','overdue') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `maintenance_logs`
--

INSERT INTO `maintenance_logs` (`maintenance_id`, `vehicle_id`, `maintenance_type`, `start_date_time`, `end_date_time`, `expected_completion_date_time`, `cost`, `description`, `parts_used`, `status`) VALUES
(4, 1, 'unspecified', '2023-11-20 00:00:00', '2023-11-21 00:00:00', '2023-11-21 00:00:00', 150.75, 'routine oil change and filter replacement.', 'Oil filter, Engine oil', 'completed'),
(5, 2, 'repair', '2023-11-25 00:00:00', NULL, '2023-11-27 00:00:00', 500, 'Transmission repair and fluid replacement.', 'Transmission fluid, Gasket', 'ongoing');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `maintenance_logs`
--
ALTER TABLE `maintenance_logs`
  ADD PRIMARY KEY (`maintenance_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `maintenance_logs`
--
ALTER TABLE `maintenance_logs`
  MODIFY `maintenance_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- Database: `schedules`
--
CREATE DATABASE IF NOT EXISTS `schedules` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `schedules`;

-- --------------------------------------------------------

--
-- Table structure for table `schedules`
--

CREATE TABLE `schedules` (
  `schedule_id` int NOT NULL,
  `schedule_type` enum('maintenance','task','assignment') NOT NULL,
  `schedule_type_id` int DEFAULT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `expected_completion` datetime DEFAULT NULL,
  `status` enum('scheduled','ongoing','cancelled','completed','overdue','active') NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `schedules`
--

INSERT INTO `schedules` (`schedule_id`, `schedule_type`, `schedule_type_id`, `start_date_time`, `end_date_time`, `expected_completion`, `status`, `description`) VALUES
(1, 'maintenance', 3, '2024-12-05 00:00:00', '2024-12-05 00:00:00', '2024-12-05 00:00:00', 'scheduled', 'Routine maintenance for vehicle'),
(2, 'task', 4, '2024-12-06 00:00:00', '2024-12-06 00:00:00', '2024-12-06 00:00:00', 'ongoing', 'Delivery of goods to warehouse B');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `schedules`
--
ALTER TABLE `schedules`
  ADD PRIMARY KEY (`schedule_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `schedules`
--
ALTER TABLE `schedules`
  MODIFY `schedule_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Database: `tasks`
--
CREATE DATABASE IF NOT EXISTS `tasks` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `tasks`;

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `task_id` int NOT NULL,
  `task` varchar(255) NOT NULL,
  `assignment_id` int DEFAULT NULL,
  `start_date_time` datetime NOT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `expected_completion_date_time` datetime DEFAULT NULL,
  `description` text,
  `priority` enum('low','medium','high','critical') NOT NULL,
  `status` enum('scheduled','ongoing','cancelled','completed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`task_id`, `task`, `assignment_id`, `start_date_time`, `end_date_time`, `expected_completion_date_time`, `description`, `priority`, `status`) VALUES
(1, 'Deliver goods to client A', 2, '2024-12-02 00:00:00', NULL, '2024-12-02 00:00:00', 'Deliver packaged goods to client A\'s warehouse.', 'high', 'scheduled'),
(2, 'Pick up supplies from depot', 3, '2024-12-03 00:00:00', NULL, '2024-12-03 00:00:00', 'Pick up supplies and deliver to main office.', 'medium', 'ongoing');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`task_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `task_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Database: `vehicle_management`
--
CREATE DATABASE IF NOT EXISTS `vehicle_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `vehicle_management`;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `vehicle_id` int NOT NULL,
  `make` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `reg_no` varchar(20) NOT NULL,
  `fuel_type` enum('petrol','diesel','electric','hybrid','not_specified') NOT NULL,
  `vehicle_type` enum('car','truck','van','bus','not_specified') NOT NULL,
  `status` enum('available','assigned','service','on_leave') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`vehicle_id`, `make`, `model`, `reg_no`, `fuel_type`, `vehicle_type`, `status`) VALUES
(1, 'MG', 'MGB', 'MNA2692', 'hybrid', 'not_specified', 'available'),
(2, 'Lexus', 'RX', 'GBK9371', 'diesel', 'not_specified', 'available'),
(3, 'Saab', '9-7X', 'KTL4599', 'petrol', 'van', 'available'),
(4, 'Chevrolet', 'Impala', 'ZQT5384', 'diesel', 'not_specified', 'available'),
(5, 'Dodge', 'Ram 2500', 'SDS3844', 'hybrid', 'truck', 'available');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD UNIQUE KEY `reg_no` (`reg_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `vehicle_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
