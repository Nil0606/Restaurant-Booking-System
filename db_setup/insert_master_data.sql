-- -----------------------------------------------------

USE `production`;


INSERT INTO `table` (`position`, `capacity`, `active_flag`, `maintenance_flag`, `special_event_flag`) VALUES
('center', 2, 1, 0, 0),
('window', 4, 1, 0, 1),
('outdoor', 3, 1, 1, 0),
('indoor', 6, 1, 0, 0),
('center', 8, 1, 0, 0),
('window', 2, 1, 0, 0),
('outdoor', 4, 1, 0, 0),
('indoor', 3, 1, 0, 1),
('center', 6, 1, 1, 0),
('window', 8, 1, 0, 0);

-- Insert sample time slots (2-hour slots)
INSERT INTO `time_slot` (`start_time`, `end_time`) VALUES
('10:00:00', '12:00:00'),
('12:00:00', '14:00:00'),
('14:00:00', '16:00:00'),
('16:00:00', '18:00:00'),
('18:00:00', '20:00:00'),
('20:00:00', '22:00:00');

-- Insert sample customers
INSERT INTO `customer` (`name`, `email`, `preferences`, `dietary_requirements`, `visit_history`, `special_occasions`) VALUES
('Alice Smith', 'alice@example.com', 'Window seat', 'Vegetarian', '', 'Birthday'),
('Bob Lee', 'bob@example.com', 'Outdoor table', 'None', '', ''),
('Carol Jones', 'carol@example.com', 'Quiet area', 'Gluten-free', '', 'Anniversary');

-- Insert sample bookings
INSERT INTO `booking` (`table_id`, `customer_id`, `start_time`, `end_time`, `active_flag`) VALUES
(1, 1, '2025-10-10 10:00:00', '2025-10-10 12:00:00', 1),
(2, 2, '2025-10-10 12:00:00', '2025-10-10 14:00:00', 1),
(3, 3, '2025-10-10 18:00:00', '2025-10-10 20:00:00', 1);
