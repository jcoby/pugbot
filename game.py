import time


class LobbyError(RuntimeError):
    pass


class Team:
    players = []
    captain = None


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

    def class_count(self, cls):
        count = 0
        for nick, player in self.players.iteritems():
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
            if self.class_count(cls) < count:
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


class Player:
    def __init__(self, nick, classes, captain=False, authorization=1):
        """Creates a Player object"""
        self.touch()
        self.classes = classes
        self.nick = nick
        self.captain = captain
        self.authorization = authorization
        self.remove = False

    def is_class(self, cls):
        return cls in self.classes
    
    def preferred_class(self):
        """get the player's preferred class"""
        return self.classes[0]

    def touch(self):
        self.last = time.time()
