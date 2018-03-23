#!/usr/bin/env python3.4

from collections import OrderedDict
from copy import deepcopy
from enum import Enum

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
    print(50*' ',winners[Games.eastSS1].value)
    print(winners[Games.southFinal].value,30*' ',winners[Games.eastFinal].value)
    print(50*' ',winners[Games.eastSS2].value)
    print(10*' ',winners[Games.four1].value,winners[Games.final].value,winners[Games.four2].value)
    print(50*' ',winners[Games.midwestSS1].value)
    print(winners[Games.westFinal].value,30*' ',winners[Games.midwestFinal].value)
    print(50*' ',winners[Games.midwestSS2].value)

def print_points(these_points):
    for player, points in these_points.items():
        line = player.name
        while len(line) % 10 != 0:
            line += ' '
        line += str(points)
        print(line)

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
    def __init__(self, one, two, div):
        self.teamone = one
        self.teamtwo = two
        self.div = div

    def get_winner(self, value):
        #winner1 = self.teamone if type(self.teamone) == Teams else self.teamone.get_winner(value/2)
        #winner2 = self.teamtwo if type(self.teamtwo) == Teams else self.teamtwo.get_winner(value/2)
        #return winner1 if value % 2 == 0 else winner2
        return self.teamone if value % self.div < self.div/2 else self.teamtwo

    def get_teams(self):
#        print(self.teamone, self.teamtwo)
        if type(self.teamone) == list and type(self.teamtwo) == list:
            return self.teamone.extend(self.teamtwo)
        elif type(self.teamone) == list:
            return self.teamone.append(self.teamtwo)
        elif type(self.teamtwo) == list:
            return self.teamtwo.append(self.teamone)
        return [self.teamone, self.teamtwo]

games = OrderedDict()
games[Games.eastSS2] = Game(Teams.nova, Teams.wvu, 2)
games[Games.eastSS1] = Game(Teams.purdue, Teams.ttu, 2)
games[Games.midwestSS1] = Game(Teams.kansas, Teams.clemson, 2)
games[Games.midwestSS2] = Game(Teams.cuse, Teams.duke, 2)
games[Games.southFinal] = Game(Teams.kstate, Teams.loyola, 2)
games[Games.westFinal] = Game(Teams.fsu, Teams.michigan, 2)
games[Games.eastFinal] = Game(None, None, 4)
games[Games.midwestFinal] = Game(None, None, 4)
games[Games.four1] = Game(None, None, 8)
games[Games.four2] = Game(None, None, 8)
games[Games.final] = Game(None, None, 16)

best = initial_points[Players.Daniel]
best_winners = None
best_points = None
iwin = 9
points = []
for i in range(2048):
    points.append(deepcopy(initial_points))
    winners = {}
    for key, value in games.items():
        winners[key] = value.get_winner(i)
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
            games[Games.final].teamtwo = winners[key]
        if key == Games.four2:
            games[Games.final].teamone = winners[key]
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
    if points[i][Players.Daniel] > best:
        best = points[i][Players.Daniel]
        best_points = deepcopy(points[i])
        best_winners = deepcopy(winners)
    if max(points[i].values()) == points[i][Players.Daniel]:
        iwin += 1

print(iwin * 100 / 2048)

print('best case')
print_winners(best_winners)
print_points(best_points)
