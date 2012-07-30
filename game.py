import random
import time


class LobbyError(RuntimeError):
    pass

class GameError(RuntimeError):
    pass
    
class Game:
    def __init__(self, lobby, roster={}, player_limit=24):
        self.lobby = lobby
        self.roster = roster
        self.player_limit = player_limit
        self.teams = [Team(), Team()]
        self.captain_pick = None
        self.captain_pick_order = [0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
    
    def assign_captains(self):
        if self.lobby.captain_count() < 2:
            raise GameError("Two captains are required to assign captains.")
            
        for team in self.teams:
            captain = self.lobby.random_captain()
            captain.game_class = captain.preferred_class()
            team.players.append(captain)
            team.captain = captain
            self.lobby.remove(captain.nick)

        self.captain_pick = 0

    def current_captain(self):
        if self.captain_pick is None:
            return None
        
        return self.current_captain_team().captain
    
    def current_captain_team(self):
        if self.captain_pick is None:
            return None
        
        return self.teams[self.captain_pick_order[self.captain_pick]]
    
    def other_captain_team(self):
        if self.captain_pick is None:
            return None
        if self.captain_pick_order[self.captain_pick] == 0:
            return self.teams[1]
        else:
            return self.teams[0]
    
    def captain_picks_remaining(self):
        if self.captain_pick is None:
            return 0
        
        return len(self.captain_pick_order) - self.captain_pick - 1
        
    def next_captain(self):
        self.captain_pick += 1
        if self.captain_pick >= len(self.captain_pick_order):
            self.captain_pick = None
        
    def random_teams(self):
        for team in range(2):
            for cls, count in self.roster.iteritems():
                for i in range(count / 2):
                    player = self.lobby.random_player(cls)
                    player.game_class = cls
                    self.teams[team].players.append(player)
                    self.lobby.remove(player.nick)
    
    def reset_teams(self):
        """Remove all players from the teams and put them back into the lobby"""
        for team in self.teams:
            while len(team.players) > 0:
                player = team.players.pop()
                player.game_class = None
                self.lobby.add(player)

            team.captain = None

class Team:
    def __init__(self, captain=None):
        self.players = []
        self.captain = captain
    
    def has_class(self, cls):
        for player in self.players:
            if player.game_class == cls:
                return True

        return False

class Lobby:
    def __init__(self):
        self.players = {}
        self._playerid = 0

    def _next_playerid(self):
        playerid = 0
        for nick, player in self.players.iteritems():
            if player.id > playerid:
                playerid = player.id

        return playerid + 1

    def class_count(self, cls, include_afk=True, seconds=420):
        count = 0
        for nick, player in self.players.iteritems():
            if include_afk == False and player.last < time.time() - seconds:
                continue

            if cls in player.classes:
                count = count + 1
        return count

    def player_count(self):
        return len(self.players)

    def captain_count(self):
        count = 0
        for nick, player in self.players.iteritems():
            if player.captain:
                count = count + 1
        return count

    def add(self, player):
        """Adds a player to the lobby"""
        if player.nick in self.players:
            player.id = self.players[player.nick].id
        else:
            player.id = self._next_playerid()

        self.players[player.nick] = player
        return True

    def remove(self, nick):
        """Removes a player by name from the lobby"""
        if nick in self.players:
            del self.players[nick]
        return True

    def roster_full(self, roster):
        """Tests to see if a roster can be filled"""
        players_needed = 0
        for cls, count in roster.iteritems():
            players_needed = players_needed + count
            if self.class_count(cls, include_afk=False) < count:
                return False

        return players_needed <= self.player_count()

    def afk_count(self, seconds=420):
        return len(self.afk_players(seconds))

    def afk_players(self, seconds=420):
        """Gets a list of players that are considered AFK"""
        players = []
        for nick, player in self.players.iteritems():
            if player.last < time.time() - seconds:
                players.append(player)

        return players

    def random_player(self, playerType):
        forcedList = []
        candidateList = []
        for nick, player in self.players.iteritems():
            forcedList.append(nick)
            if len(player.classes) > 0 and playerType == player.preferred_class():
                candidateList.append(player)
        if len(candidateList) > 0:
            return random.choice(candidateList)
        else:
            return random.choice(forcedList)
    
    def random_captain(self):
        if self.captain_count() == 0:
            return None
        
        medics = []
        medicsCaptains = []
        otherCaptains = []
        for nick, player in self.players.iteritems():
            if "medic" in player.classes:
                if player.captain:
                    medicsCaptains.append(player)
                else:
                    medics.append(player)
            elif player.captain:
                otherCaptains.append(player)
        if len(medicsCaptains) > 0:
            player = random.choice(medicsCaptains)
            player.classes = ['medic']
        elif len(otherCaptains) > 0:
            maximum = 0
            otherCaptainWithMaximumRatio = ''
            for otherCaptain in otherCaptains:
                winStats = otherCaptain.win_stats
                if winStats[3] > maximum:
                    maximum = winStats[3]
                    otherCaptainWithMaximumRatio = otherCaptain.nick
            if maximum > 0:
                player = self.players[otherCaptainWithMaximumRatio]
            else:
                player = random.choice(otherCaptains)
            if len(player.classes) > 0:
                player.classes = [player.preferred_class()]
            else:
                player.classes = ['scout']
        else:
            player = random.choice(medics)
            player.classes = ['medic']
        return player


class Player:
    def __init__(self, nick, classes, captain=False, authorization=1):
        """Creates a Player object"""
        self.touch()
        self.classes = classes
        self.nick = nick
        self.captain = captain
        self.authorization = authorization
        self.remove = False
        self.win_stats = [nick, 0, 0, 0, 0]
        self.game_class = None

    def is_class(self, cls):
        return cls in self.classes
    
    def preferred_class(self):
        """get the player's preferred class"""
        return self.classes[0]

    def touch(self):
        self.last = time.time()
