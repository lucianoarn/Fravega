-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-11-2025 a las 04:56:10
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `user_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventory`
--

CREATE TABLE `inventory` (
  `ID` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventory`
--

INSERT INTO `inventory` (`ID`, `name`, `stock`) VALUES
(1, 'Tv samsung', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `sector_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`ID`, `username`, `password`, `sector_id`) VALUES
(1, 'luciano', '123', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `inventory`
--
ALTER TABLE `inventory`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

CREATE TABLE `financial_movements` (
  `id` INT(11) NOT NULL,
  `type` VARCHAR(50) NOT NULL COMMENT 'Tipo de movimiento: Ingreso o Gasto',
  `amount` DECIMAL(10, 2) NOT NULL COMMENT 'Monto del movimiento (positivo para ingreso, negativo para gasto)',
  `description` VARCHAR(255) DEFAULT NULL,
  `date` DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para financial_movements
--
ALTER TABLE `financial_movements`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `financial_movements`
  MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `campaigns` (Marketing)
--
CREATE TABLE `campaigns` (
  `campaign_id` INT(11) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `objective` VARCHAR(255) DEFAULT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE DEFAULT NULL,
  `budget` DECIMAL(10, 2) DEFAULT 0.00,
  `status` VARCHAR(50) DEFAULT 'Active' COMMENT 'Active, Completed, Paused'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para campaigns
--
ALTER TABLE `campaigns`
  ADD PRIMARY KEY (`campaign_id`);

ALTER TABLE `campaigns`
  MODIFY `campaign_id` INT(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `employees` (RRHH)
--
CREATE TABLE `employees` (
  `employee_id` INT(11) NOT NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `hire_date` DATE NOT NULL,
  `salary` DECIMAL(10, 2) DEFAULT NULL,
  `position` VARCHAR(100) DEFAULT NULL,
  `sector_id` INT(11) DEFAULT NULL COMMENT 'Relacionado con sector_id en users si es necesario',
  `is_active` BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para employees
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`);

ALTER TABLE `employees`
  MODIFY `employee_id` INT(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;