-- Removal code for gamesats
-- Could be used to reset the database
DROP DATABASE gamestatsdb;
USE lab_1;
SHOW DATABASES;

-- Some simple querries to view stuff
SELECT * FROM matches;
SELECT * FROM playermatchstats;
SELECT * FROM players;
SELECT * FROM teammembers;
SELECT * FROM teams;