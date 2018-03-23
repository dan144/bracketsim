#!/usr/bin/env python3.4

from collections import OrderedDict
from copy import deepcopy
from enum import Enum

class Players(Enum):
    Matt='Matt      '
    Shawn='Shawn     '
    Brian='Brian     '
    Elgyn='Elgyn     '
    Daniel='Daniel    '
    Tim='Tim       '
    Chris='Chris     '
    Adam='Adam      '
    JD='JD        '
    Kevin='Kevin     '
    Forrest='Forrest   '

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

def print_picks():
    """Prints a board of each player's picks"""
    header = ''
    pickstr = 11*['']
    for player, pickset in picks.items():
        header += player.value
        for i in range(len(pickset)):
            if pickset[i]:
                pickstr[i] += pickset[i].value
            else:
                pickstr[i] += '          '
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

def print_final(wins, total_sims, best_points, best_winners):
    if total_sims == 0:
        print('No simulations completed; impossible filter likely applied')
        print('Blacklist:')
        for game, teams in blacklist.items():
            print('{}\t\t{}'.format(game.name, ', '.join([t.value for t in teams])))
        print('Whitelist:')
        for game, teams in whitelist.items():
            print('{}\t\t{}'.format(game.name, ', '.join([t.value for t in teams])))
        return
    print('Odds of winning:')
    for player, odds in wins.items():
        print(player.value, 100 * odds / total_sims)

    print()
    if best_points and best_winners:
        print("Daniel's best possible outcome (leaderboard)")
        print_points(best_points)
        print_winners(best_winners)
    else:
        print('Daniel cannot win')

whitelist = {
    #Games.final: {Teams.purdue}
}
blacklist = {
    #Games.eastSS2: {Teams.purdue}
}
def forbidden_condition(games):
    """
    Checks the white and blacklists to see if outcomes are forbidden
    returns True if an outcome is not allowed
    """
    for game, teams in blacklist.items():
        if games[game].get_winner(bitlist[game.value]) in teams:
            return True
    for game, teams in whitelist.items():
        if games[game].get_winner(bitlist[game.value]) not in teams:
            return True
    return False

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

best_win = initial_points[Players.Daniel]
best = deepcopy(initial_points)
best_winners = None
best_points = None
total_sims = 0
points = []
wins = {}

for i in range(2048):
    # creates list of booleans based on the binary representation of the for loop counter
    # this provides a unique set of outcomes for the 11 games
    bitlist = list(bin(i)[2:])
    while len(bitlist) < len(list(games.items())):
        bitlist.insert(0, False)
    for b in range(len(bitlist)):
        bitlist[b] = bitlist[b] == '1'

    points.append(deepcopy(initial_points))
    winners = {}

    # iterates through all games in the list, selecting winners based on the bitlist
    for key, value in games.items():
        winners[key] = value.get_winner(bitlist[key.value])

        # (inefficiently) puts the winners into their following game
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

    if forbidden_condition(games):
        continue # skips this outcome if it isn't allowed

    # calculate each player's points total for the sim
    for player in points[i].keys():
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
        if points[i][player] > best[player]:
            best[player] = points[i][player]

    # store points data, update winners count, handle Daniel special case analysis
    points[i] = OrderedDict(sorted(points[i].items(), key=lambda t:t[1], reverse=True))
    winner = list(points[i].items())[0]
    wins[winner[0]] = wins.get(winner[0], 0) + 1
    if points[i][Players.Daniel] >= best_win and winner[0] == Players.Daniel:
        best_win = points[i][Players.Daniel]
        best_points = deepcopy(points[i])
        best_winners = deepcopy(winners)
    total_sims += 1

# sort wins by probability
wins = OrderedDict(sorted(wins.items(), key=lambda t:t[1], reverse=True))
print_final(wins, total_sims, best_points, best_winners)
