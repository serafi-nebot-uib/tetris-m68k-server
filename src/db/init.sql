create table tetris.score
(
    player   char(6)                                not null,
    score    int unsigned                           not null,
    timestamp timestamp default current_timestamp() not null
);

create index score_player_index
    on tetris.score (player);

create index score_timestamp_index
    on tetris.score (timestamp);

insert into tetris.score (player, score, timestamp) values ("serafi", 50, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("jaume", 123061, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("serafi", 9999999, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("serafi", 144, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("ignasi", 912412, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("ignasi", 1456, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("jaume", 5, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("jaume", 991599, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("ignasi", 62, "2024-11-01 14:05:14");
insert into tetris.score (player, score, timestamp) values ("serafi", 44415, "2024-11-01 14:05:14");
