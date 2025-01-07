drop table if exists `score`;
create table `score` (
  `player` char(6) not null,
  `type` enum('A','B') not null,
  `score` int unsigned not null,
  `level` int unsigned not null,
  `timestamp` timestamp not null default current_timestamp,
  key `score_player_index` (`player`),
  key `score_timestamp_index` (`timestamp`)
) engine=innodb default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;
