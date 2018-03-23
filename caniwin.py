#!/usr/bin/env python3.4

from collections import OrderedDict
from copy import deepcopy
from enum import Enum

def print_picks():
    """Prints a board of each player's picks"""
    header = ''
    pickstr = 11*['']
    for player, pickset in picks.items():
        header += player.name
        while len(header) % 10 != 0:
            header += ' '
        for i in range(len(pickset)):
            if pickset[i]:
                pickstr[i] += pickset[i].name
            else:
                pickstr[i] += ' '
            while len(pickstr[i]) % 10 != 0:
                pickstr[i] += ' '
    print(header)
    for s in pickstr:
        print(s)

def print_winners(winners):
    """
    Prints the winners of each game in a rudimentary bracket format
    winners: dict of the winner of each game, using the key/value pairing Games/Teams
    """
    print(50*' ',winners[Games.eastSS1].value)
    print(winners[Games.southFinal].value,30*' ',winners[Games.eastFinal].value)
    print(50*' ',winners[Games.eastSS2].value)
    print(10*' ',winners[Games.four1].value,winners[Games.final].value,winners[Games.four2].value)
    print(50*' ',winners[Games.midwestSS1].value)
    print(winners[Games.westFinal].value,30*' ',winners[Games.midwestFinal].value)
    print(50*' ',winners[Games.midwestSS2].value)

def print_points(these_points):
    """
    Prints the points for each user
    these_points: dict of scores, using the key/value pairing Players/int
    """
    for player, points in these_points.items():
        line = player.name
        while len(line) % 10 != 0:
            line += ' '
        line += str(points)
        print(line)

class Players(Enum):
    Matt=1
    Shawn=2
    Brian=3
    Elgyn=4
    Daniel=5
    Tim=6
    Chris=7
    Adam=8
    JD=9
    Kevin=10
    Forrest=11

class Teams(Enum):
    nova='Nova      '
    wvu='WVU       '
    ttu='TTU       '
    purdue='Purdue    '
    kansas='Kansas    '
    clemson='Clemson   '
    cuse='Cuse      '
    duke='Duke    '
    kstate='KState    '
    loyola='Loyola    '
    fsu='FSU       '
    michigan='Michigan  '

class Games(Enum):
    eastSS1=0
    eastSS2=1
    midwestSS1=2
    midwestSS2=3
    southFinal=4
    westFinal=5
    eastFinal=6
    midwestFinal=7
    four1=8
    four2=9
    final=10

class Game():
    def __init__(self, one=None, two=None):
        self.teamone = one
        self.teamtwo = two

    def get_winner(self, value):
        return self.teamone if value else self.teamtwo

initial_points = {
    Players.Matt: 46,
    Players.Shawn: 41,
    Players.Brian: 40,
    Players.Elgyn: 39,
    Players.Daniel: 39,
    Players.Tim: 37,
    Players.Chris: 35,
    Players.Adam: 34,
    Players.JD: 33,
    Players.Kevin: 33,
    Players.Forrest: 29
}

picks = {
    Players.Matt: [Teams.nova, Teams.purdue, Teams.kansas, Teams.duke, None, Teams.michigan, Teams.nova, Teams.duke, None, Teams.nova, None],
    Players.Shawn: [Teams.nova, Teams.purdue, Teams.kansas, Teams.duke, None, None, Teams.nova, Teams.duke, None, Teams.nova, Teams.nova],
    Players.Brian: [Teams.wvu, Teams.purdue, Teams.kansas, Teams.duke, None, None, Teams.purdue, Teams.duke, None, Teams.purdue, Teams.purdue],
    Players.Elgyn: [Teams.nova, Teams.ttu, Teams.kansas, Teams.duke, None, Teams.michigan, Teams.nova, Teams.duke, None, Teams.nova, Teams.nova],
    Players.Daniel: [Teams.nova, Teams.purdue, Teams.kansas, Teams.duke, None, None, Teams.purdue, Teams.kansas, None, Teams.purdue, Teams.purdue],
    Players.Tim: [Teams.nova, Teams.purdue, Teams.clemson, None, None, Teams.michigan, Teams.nova, None, Teams.michigan, Teams.nova, Teams.nova],
    Players.Chris: [Teams.nova, Teams.purdue, Teams.kansas, None, None, None, Teams.nova, None, None, None, None],
    Players.Adam: [Teams.nova, None, Teams.kansas, None, None, None, Teams.nova, None, None, None, None],
    Players.JD: [Teams.nova, Teams.purdue, Teams.kansas, Teams.duke, None, None, Teams.nova, Teams.duke, None, Teams.duke, Teams.duke],
    Players.Kevin: [Teams.nova, Teams.ttu, Teams.kansas, None, None, None, Teams.nova, None, None, Teams.nova, Teams.nova],
    Players.Forrest: [Teams.nova, None, None, None, None, None, Teams.nova, None, None, Teams.nova, Teams.nova]
}

games = OrderedDict()
games[Games.eastSS1] = Game(Teams.nova, Teams.wvu)
games[Games.eastSS2] = Game(Teams.ttu, Teams.purdue)
games[Games.midwestSS1] = Game(Teams.kansas, Teams.clemson)
games[Games.midwestSS2] = Game(Teams.cuse, Teams.duke)
games[Games.southFinal] = Game(Teams.kstate, Teams.loyola)
games[Games.westFinal] = Game(Teams.fsu, Teams.michigan)
games[Games.eastFinal] = Game()
games[Games.midwestFinal] = Game()
games[Games.four1] = Game()
games[Games.four2] = Game()
games[Games.final] = Game()

best = initial_points[Players.Daniel]
best_winners = None
best_points = None
iwin = 0
points = []
for i in range(2048):
    points.append(deepcopy(initial_points))
    winners = {}
    bitlist = list(bin(i)[2:])
    while len(bitlist) < len(list(games.items())):
        bitlist.insert(0, False)
    for b in range(len(bitlist)):
        bitlist[b] = bitlist[b] == '1'
    j = 0
    for key, value in games.items():
        winners[key] = value.get_winner(bitlist[j])
        if key == Games.eastSS1:
            games[Games.eastFinal].teamone = winners[key]
        if key == Games.eastSS2:
            games[Games.eastFinal].teamtwo = winners[key]
        if key == Games.midwestSS1:
            games[Games.midwestFinal].teamone = winners[key]
        if key == Games.midwestSS2:
            games[Games.midwestFinal].teamtwo = winners[key]
        if key == Games.southFinal:
            games[Games.four1].teamone = winners[key]
        if key == Games.westFinal:
            games[Games.four1].teamtwo = winners[key]
        if key == Games.eastFinal:
            games[Games.four2].teamone = winners[key]
        if key == Games.midwestFinal:
            games[Games.four2].teamtwo = winners[key]
        if key == Games.four1:
            games[Games.final].teamone = winners[key]
        if key == Games.four2:
            games[Games.final].teamtwo = winners[key]
        j += 1
    for player in points[i].keys():
        j = 0
        for game, winner in winners.items():
            point = 0
            if 'SS' in game.name:
                point = 4
            elif 'Final' in game.name:
                point = 8
            elif 'four' in game.name:
                point = 16
            elif 'final' in game.name:
                point = 32
            if winner == picks[player][game.value]:
                points[i][player] += point
            j += 1
    points[i] = OrderedDict(sorted(points[i].items(), key=lambda t:t[1], reverse=True))
    if points[i][Players.Daniel] > best:
        best = points[i][Players.Daniel]
        best_points = deepcopy(points[i])
        best_winners = deepcopy(winners)
    if max(points[i].values()) == points[i][Players.Daniel]:
        iwin += 1

print("Daniel's odds of winning: {}".format(iwin * 100 / 2048))

print("Daniel's best possible score (leaderboard)")
print_points(best_points)
print_winners(best_winners)
