import unittest
import time
from game import Lobby, Player

class TestGameMethods(unittest.TestCase):
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
        roster = {"scout": 1, "soldier": 2}
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), False)

        p = Player("testB", ["soldier", "scout"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), False)

        p = Player("testC", ["soldier", "scout"], False)
        self.lobby.add(p)
        self.assertEqual(self.lobby.roster_full(roster), True)
    
    def test_afk_players(self):
        p = Player("testA", ["soldier"], False)
        self.lobby.add(p)
        
        self.assertEqual(self.lobby.afk_count(), 0)
        
        self.lobby.players["testA"].last = time.time() - 500
        self.assertEqual(self.lobby.afk_count(), 1)
        
if __name__ == '__main__':
    unittest.main()