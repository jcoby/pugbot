import unittest
import time
from game import Lobby, Player, Game

class TestLobbyMethods(unittest.TestCase):
    def setUp(self):
        self.lobby = Lobby()
    
    def test_add(self):
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.player_count(), 1)
        self.assertEqual(self.lobby.captain_count(), 0)
        
        # add a captain
        c = Player("testB", ["scout"], True)
        self.lobby.add(c)
        self.assertEqual(self.lobby.player_count(), 2)
        self.assertEqual(self.lobby.captain_count(), 1)
        
        #verify the playerid attr
        self.assertEqual(self.lobby.players["testA"].id, 1)
        self.assertEqual(self.lobby.players["testB"].id, 2)
        
    def test_remove(self):
        p = Player("testC", ["soldier"], False)
        self.lobby.add(p)
        self.lobby.remove("testC")
        self.assertEqual(self.lobby.player_count(), 0)

    def test_class_count(self):
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.class_count("soldier"), 1)
        
        p = Player("testB", ["soldier", "scout"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.class_count("soldier"), 2)
        self.assertEqual(self.lobby.class_count("scout"), 1)
    
    def test_roster_full(self):
        roster = {"scout": 1, "soldier": 1}
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), False)

        p = Player("testB", ["soldier", "scout"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), True)

        p = Player("testC", ["soldier", "scout"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), True)
    
    def test_afk_players(self):
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        
        self.assertEqual(self.lobby.afk_count(), 0)
        
        self.lobby.players["testA"].last = time.time() - 500
        self.assertEqual(self.lobby.afk_count(), 1)
    
    def test_random_captain(self):
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)

        self.assertIsNone(self.lobby.random_captain())

        p = Player("testB", ["soldier"], True)
        self.lobby.add(p)
        
        self.assertIsNotNone(self.lobby.random_captain())

class TestGameMethods(unittest.TestCase):
    def setUp(self):
        self.roster = {"soldier": 4, "scout": 4, "demo": 2, "medic": 2}
        self.lobby = Lobby()
        self.game = Game(self.lobby, self.roster)
    
    def populate_lobby(self):
        classes = ["soldier", "soldier", "soldier", "soldier", "scout", "scout", "scout", "scout", "demo", "demo", "medic", "medic"]
        for i, cls in enumerate(classes):
            p = Player("test" + str(i), [cls], False)
            self.lobby.add(p)
        
        c = Player("testC1" + str(i), ["medic"], True)
        self.lobby.add(c)
        c = Player("testC2" + str(i), ["scout"], True)
        self.lobby.add(c)
    
    def test_assign_captains(self):
        self.populate_lobby()
        self.game.assign_captains()
        
        self.assertIsNotNone(self.game.teams[0].captain)
        self.assertIsNotNone(self.game.teams[1].captain)
        
        self.assertEqual(len(self.game.teams[0].players), 1)
        self.assertEqual(len(self.game.teams[1].players), 1)
    
    def test_random_teams(self):
        self.populate_lobby()
        self.game.random_teams()
        
        self.assertEqual(len(self.game.teams[0].players), 6)
        self.assertEqual(len(self.game.teams[1].players), 6)
    
    def test_reset_teams(self):
        self.populate_lobby()
        self.game.random_teams()
        
        self.game.reset_teams()
        
        self.assertEqual(len(self.game.teams[0].players), 0)
        self.assertEqual(len(self.game.teams[1].players), 0)
        
        self.assertEqual(len(self.lobby.players), 14)
    
    def test_next_captain(self):
        self.populate_lobby()
        self.game.assign_captains()
        
        for i, pick in enumerate(range(10)):
            self.assertIsNotNone(self.game.current_captain())
            self.game.next_captain()
            
    def test_captain_picks_remaining(self):
        self.populate_lobby()
        self.game.assign_captains()
        
        for i, pick in enumerate(range(10)):
            self.assertEqual(self.game.captain_picks_remaining(), 10 - i)
            self.game.next_captain()
            
        
if __name__ == '__main__':
    unittest.main()