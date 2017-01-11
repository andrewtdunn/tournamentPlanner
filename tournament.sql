-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (

          name TEXT,
          id SERIAL primary key
);

CREATE TABLE matches (

          id SERIAL primary key,
          winner INTEGER references players(id),
          loser INTEGER references players(id)
);

CREATE VIEW current_standings AS
                            SELECT players.id, players.name,
                            COUNT(CASE players.id WHEN winner
                                THEN 1 ELSE NULL END) AS wins,
                            COUNT(matches.id) AS matches
                            FROM players
                            LEFT JOIN matches
                            ON players.id IN (winner, loser)
                            GROUP by players.id
                            ORDER BY wins DESC;
