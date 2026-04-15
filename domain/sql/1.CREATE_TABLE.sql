CREATE TABLE `ev_infrastructure_stats` (
  `year` int NOT NULL,
  `location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_ev_registration` int NOT NULL,
  `total_ev_charger` int NOT NULL,
  PRIMARY KEY (`year`,`location`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;