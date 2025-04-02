-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2025 at 06:47 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_pos`
--

-- --------------------------------------------------------

--
-- Table structure for table `bill`
--

CREATE TABLE `bill` (
  `bill_id` int(11) NOT NULL,
  `bill_number` varchar(230) NOT NULL,
  `total_amount` float NOT NULL,
  `paid_total_amount` float DEFAULT NULL,
  `date` varchar(350) NOT NULL,
  `trans_time` varchar(19) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `table_number` varchar(23) DEFAULT NULL,
  `waiter_id` varchar(100) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `bill_type` varchar(100) DEFAULT NULL,
  `created_date` varchar(100) DEFAULT NULL,
  `modified_date` varchar(100) DEFAULT NULL,
  `status` varchar(110) DEFAULT 'draft'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bill`
--

INSERT INTO `bill` (`bill_id`, `bill_number`, `total_amount`, `paid_total_amount`, `date`, `trans_time`, `customer_id`, `table_number`, `waiter_id`, `centers_id`, `bill_type`, `created_date`, `modified_date`, `status`) VALUES
(3, '251401140405_54', 6, NULL, '2025-14-01', '14: 04: 05', NULL, NULL, '1', 1, 'New', NULL, NULL, 'posted'),
(4, '251501140443_75', 0, NULL, '2025-15-01', '14: 04: 43', NULL, NULL, '1', 1, 'New', NULL, NULL, 'draft'),
(5, '251701140442_22', 0, NULL, '2025-17-01', '14: 04: 42', NULL, NULL, '1', 1, 'New', '2025-17-01', NULL, 'draft'),
(6, '251801140448_33', 0, NULL, '2025-18-01', '14: 04: 48', NULL, NULL, '1', 1, 'Complementary', '2025-18-01', NULL, 'draft');

-- --------------------------------------------------------

--
-- Table structure for table `centers`
--

CREATE TABLE `centers` (
  `centers_id` int(11) NOT NULL,
  `name` varchar(230) DEFAULT NULL,
  `address` varchar(56) DEFAULT NULL,
  `email` varchar(56) DEFAULT NULL,
  `tel` varchar(56) DEFAULT NULL,
  `po_box` varchar(230) DEFAULT NULL,
  `leter_head` varchar(1200) DEFAULT NULL,
  `date_created` varchar(23) DEFAULT NULL,
  `current_trade_date` varchar(12) DEFAULT NULL,
  `day_open_status` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `goods_received`
--

CREATE TABLE `goods_received` (
  `grn_id` int(11) DEFAULT NULL,
  `grn_status` varchar(110) DEFAULT NULL,
  `goods_received_id` int(11) NOT NULL,
  `name` varchar(110) DEFAULT NULL,
  `standard_quantity` int(11) DEFAULT NULL,
  `actual_units_received` int(11) DEFAULT NULL,
  `cost_price_per_unit` int(11) DEFAULT NULL,
  `selling_price_per_unit` int(11) DEFAULT NULL,
  `discount_in_percentage` int(11) DEFAULT 0,
  `reorder_level` int(11) DEFAULT 3,
  `date_updated` varchar(78) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `visibility` varchar(12) DEFAULT 'show',
  `item_source_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `status` varchar(110) DEFAULT 'pending_receive',
  `total_cost` float DEFAULT NULL,
  `photo` varchar(1100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `goods_received`
--

INSERT INTO `goods_received` (`grn_id`, `grn_status`, `goods_received_id`, `name`, `standard_quantity`, `actual_units_received`, `cost_price_per_unit`, `selling_price_per_unit`, `discount_in_percentage`, `reorder_level`, `date_updated`, `centers_id`, `visibility`, `item_source_id`, `supplier_id`, `status`, `total_cost`, `photo`) VALUES
(1, 'pending_approval', 1, 'Tusker Lite', 10, 20, 175, 250, 0, 3, '02-04-2025', 1, 'show', 1, 1, 'approved', 3500, 'photo.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `grn`
--

CREATE TABLE `grn` (
  `grn_id` int(11) NOT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `grn_no` varchar(110) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `waiter_id` int(11) DEFAULT NULL,
  `date` varchar(35) DEFAULT NULL,
  `trans_time` varchar(35) DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `total_items` int(11) DEFAULT NULL,
  `status` varchar(110) DEFAULT 'pending_approval',
  `comments` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `grn`
--

INSERT INTO `grn` (`grn_id`, `supplier_id`, `grn_no`, `centers_id`, `waiter_id`, `date`, `trans_time`, `total_amount`, `total_items`, `status`, `comments`) VALUES
(1, 1, '100456', 1, 1, '02-04-2025', '02:14', 3500, 20, 'approved', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE `item` (
  `item_id` int(11) NOT NULL,
  `name` varchar(110) DEFAULT NULL,
  `standard_quantity` int(11) DEFAULT NULL,
  `actual_units_in_stock` int(11) DEFAULT NULL,
  `cost_price_per_unit` int(11) DEFAULT NULL,
  `selling_price_per_unit` int(11) DEFAULT NULL,
  `discount_in_percentage` int(11) DEFAULT 0,
  `reorder_level` int(11) DEFAULT 3,
  `date_updated` varchar(78) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `visibility` varchar(12) DEFAULT 'show',
  `item_source_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `status` varchar(110) DEFAULT 'for sale',
  `photo` varchar(1100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`item_id`, `name`, `standard_quantity`, `actual_units_in_stock`, `cost_price_per_unit`, `selling_price_per_unit`, `discount_in_percentage`, `reorder_level`, `date_updated`, `centers_id`, `visibility`, `item_source_id`, `supplier_id`, `status`, `photo`) VALUES
(2, 'Tusker Lite', 20, 60, 175, 250, 0, 3, '02-04-2025', 1, 'show', 1, 1, 'pending_receive', 'photo.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `item_source`
--

CREATE TABLE `item_source` (
  `item_source_id` int(11) NOT NULL,
  `name` varchar(110) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `item_source`
--

INSERT INTO `item_source` (`item_source_id`, `name`) VALUES
(1, 'BAR'),
(2, 'KITCHEN');

-- --------------------------------------------------------

--
-- Table structure for table `payment_mode`
--

CREATE TABLE `payment_mode` (
  `payment_mode_id` int(11) NOT NULL,
  `name` varchar(110) DEFAULT NULL,
  `date` varchar(19) DEFAULT NULL,
  `trans_time` varchar(19) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `waiter_id` int(11) DEFAULT NULL,
  `visibility` varchar(35) DEFAULT 'show'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payment_mode`
--

INSERT INTO `payment_mode` (`payment_mode_id`, `name`, `date`, `trans_time`, `centers_id`, `waiter_id`, `visibility`) VALUES
(1, 'M-Pesa', '02-04-2025', '02:29', 1, 1, 'show'),
(2, 'Pesapal PDQ', '02-04-2025', '02:30', 1, 1, 'show');

-- --------------------------------------------------------

--
-- Table structure for table `sale`
--

CREATE TABLE `sale` (
  `sale_id` int(11) NOT NULL,
  `bill_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `item_name` varchar(1100) DEFAULT NULL,
  `no_of_items` int(11) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `waiter_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `status` varchar(19) DEFAULT 'draft'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sale`
--

INSERT INTO `sale` (`sale_id`, `bill_id`, `item_id`, `item_name`, `no_of_items`, `centers_id`, `waiter_id`, `date`, `time`, `total_amount`, `status`) VALUES
(1, 1, 1, 'Bluemoon Vodka', 2, 1, 1, '01-01-2025', '10:15', 900, 'sold'),
(2, 3, 1, 'Guarana', 1, 1, 1, '2025-32-01', '15: 04: 00', 1, 'sold'),
(3, 3, 1, 'Guarana', 1, 1, 1, '2025-33-01', '15: 04: 46', 1, 'sold'),
(4, 3, 1, 'Guarana', 1, 1, 1, '2025-41-01', '15: 04: 52', 1, 'sold'),
(5, 3, 1, 'Guarana', 1, 1, 1, '2025-42-01', '15: 04: 55', 1, 'sold'),
(6, 3, 1, 'Guarana', 1, 1, 1, '2025-23-01', '18: 04: 53', 1, 'sold'),
(7, 3, 1, 'Guarana', 1, 1, 1, '2025-24-01', '18: 04: 21', 1, 'sold');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `supplier_id` int(11) NOT NULL,
  `name` varchar(110) DEFAULT NULL,
  `phone` varchar(110) DEFAULT NULL,
  `email` varchar(110) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transaction_id` int(11) NOT NULL,
  `transaction_type` varchar(110) DEFAULT 'credit',
  `payment_mode_id` varchar(110) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `bill_id` int(11) DEFAULT NULL,
  `date` varchar(230) DEFAULT NULL,
  `trans_time` varchar(35) DEFAULT NULL,
  `transaction_code` varchar(110) DEFAULT NULL,
  `waiter_id` varchar(20) DEFAULT NULL,
  `centers_id` int(11) DEFAULT NULL,
  `description` varchar(1200) DEFAULT NULL,
  `trans_status` varchar(25) DEFAULT 'pending',
  `cash_in_hand` int(11) DEFAULT NULL,
  `change_amount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transaction_id`, `transaction_type`, `payment_mode_id`, `amount`, `bill_id`, `date`, `trans_time`, `transaction_code`, `waiter_id`, `centers_id`, `description`, `trans_status`, `cash_in_hand`, `change_amount`) VALUES
(1, 'credit', '1', 200, 1, '2025-31-02', '14: 04: 47', 'QRWERG784673Y', '1', 1, '', 'Completed', 0, 0),
(2, 'credit', '1', 200, 1, '2025-32-02', '14: 04: 01', 'QRWERG784673Y', '1', 1, '', 'Completed', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`bill_id`);

--
-- Indexes for table `centers`
--
ALTER TABLE `centers`
  ADD PRIMARY KEY (`centers_id`);

--
-- Indexes for table `goods_received`
--
ALTER TABLE `goods_received`
  ADD PRIMARY KEY (`goods_received_id`);

--
-- Indexes for table `grn`
--
ALTER TABLE `grn`
  ADD PRIMARY KEY (`grn_id`);

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `item_source`
--
ALTER TABLE `item_source`
  ADD PRIMARY KEY (`item_source_id`);

--
-- Indexes for table `payment_mode`
--
ALTER TABLE `payment_mode`
  ADD PRIMARY KEY (`payment_mode_id`);

--
-- Indexes for table `sale`
--
ALTER TABLE `sale`
  ADD PRIMARY KEY (`sale_id`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`supplier_id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bill`
--
ALTER TABLE `bill`
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `centers`
--
ALTER TABLE `centers`
  MODIFY `centers_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `goods_received`
--
ALTER TABLE `goods_received`
  MODIFY `goods_received_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `grn`
--
ALTER TABLE `grn`
  MODIFY `grn_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `item`
--
ALTER TABLE `item`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `item_source`
--
ALTER TABLE `item_source`
  MODIFY `item_source_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `payment_mode`
--
ALTER TABLE `payment_mode`
  MODIFY `payment_mode_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sale`
--
ALTER TABLE `sale`
  MODIFY `sale_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `supplier`
--
ALTER TABLE `supplier`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
