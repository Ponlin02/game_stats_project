-- Some players from the mushroom kingdom
INSERT INTO Players (Name) VALUES
('Mario'),
('Luigi'),
('Princess Peach'),
('Princess Daisy'),
('Yoshi'),
('Bowser'),
('Bowser jr'),
('Wario'),
('Waluigi'),
('Kamek');

INSERT INTO Teams (TeamName) VALUES 
('Team Mario'),
('Team Bowser');

-- Team Mario
INSERT INTO TeamMembers (TeamID, PlayerID) VALUES
(1, 1),  -- Mario
(1, 2),  -- Luigi
(1, 3),  -- Peach
(1, 4),  -- Daisy
(1, 5);  -- Yoshi

-- Team Bowser
INSERT INTO TeamMembers (TeamID, PlayerID) VALUES
(2, 6),  -- Bowser
(2, 7),  -- Bowser Jr.
(2, 8),  -- Wario
(2, 9),  -- Waluigi
(2, 10); -- Kamek

-- Insert a match played
INSERT INTO Matches (Team1ID, Team2ID, WinningTeamID, MatchDate)
VALUES (1, 2, 1, '2025-05-20');

-- Team Mario (Winners)
INSERT INTO PlayerMatchStats (MatchID, PlayerID, Kills, Deaths, Assists) VALUES
(1, 1, 5, 2, 3),  -- Mario
(1, 2, 3, 1, 4),  -- Luigi
(1, 3, 2, 2, 5),  -- Peach
(1, 4, 1, 1, 6),  -- Daisy
(1, 5, 4, 3, 1);  -- Yoshi

-- Team Bowser
INSERT INTO PlayerMatchStats (MatchID, PlayerID, Kills, Deaths, Assists) VALUES
(1, 6, 2, 4, 1),  -- Bowser
(1, 7, 1, 5, 0),  -- Bowser Jr.
(1, 8, 3, 3, 2),  -- Wario
(1, 9, 0, 4, 1),  -- Waluigi
(1, 10, 2, 2, 2); -- Kamek
