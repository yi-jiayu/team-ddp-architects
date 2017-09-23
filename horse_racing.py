# Question 1
import requests

def solve(inp3):
    #inp1 = requests.get('http://cis2017-horse-racing.herokuapp.com/api/data')
    #inp = inp1.json() + inp3
    inp = inp3
    inp2 = inp  # copy of inp to be used for ordered data in Question 3

    raceorder = []  # all races in order by date and number
    racepool = []  # list of all unique races
    jockpool = []  # list of all unique jockeys

    winners = []  # list of winners for each unique race
    trainers = []  # list of trainers of winning horse for each unique race
    horses = []  # list of winning horses for each unique race
    winners2 = []
    trainers2 = []
    horses2 = []
    winners3 = []
    trainers3 = []
    horses3 = []

    winnercount = 0  # latest highest wincount for jockey wins
    trainercount = 0  # latest highest wincount of trainers for winning horses
    horsecount = 0  # latest highest wincount for winning horse
    finalwinner = ''  # best jockey
    finaltrainer = ''  # best trainer
    finalhorse = ''  # best horse

    for i in range(len(inp)):
        if inp[i]['RaceIndex'] not in racepool:
            racepool.append(inp[i]['RaceIndex'])
        if inp[i]['jockeycode'] not in jockpool:
            jockpool.append(inp[i]['jockeycode'])

    for j in range(len(racepool)):
        for i in range(len(inp)):
            if racepool[j] == inp[i]['RaceIndex'] and inp[i]['Placing'] == '1':
                winners.append(inp[i]['jockeycode'])
                trainers.append(inp[i]['Trainer'])
                horses.append(inp[i]['Horse'])
            elif racepool[j] == inp[i]['RaceIndex'] and inp[i]['Placing'] == '2':
                winners2.append(inp[i]['jockeycode'])
                trainers2.append(inp[i]['Trainer'])
                horses2.append(inp[i]['Horse'])
            elif racepool[j] == inp[i]['RaceIndex'] and inp[i]['Placing'] == '3':
                winners3.append(inp[i]['jockeycode'])
                trainers3.append(inp[i]['Trainer'])
                horses3.append(inp[i]['Horse'])

    for i in range(len(winners)):
        if winners.count(winners[i]) > winnercount:
            finalwinner = winners[i]
            winnercount = winners.count(winners[i])
        if trainers.count(trainers[i]) > trainercount:
            finaltrainer = trainers[i]
            trainercount = trainers.count(trainers[i])
        if horses.count(horses[i]) > horsecount:
            finalhorse = horses[i]
            horsecount = horses.count(horses[i])

        # Question 2

    betvalue = {}  # dictionary of points for jockeys
    betvalue1 = {}  # dictionary of points for trainers
    betvalue2 = {}  # dictionary of points for horses

    for i in range(len(winners)):
        if winners[i] not in betvalue.keys():
            betvalue[winners[i]] = 7 * winners.count(winners[i]) + 3 * winners2.count(winners[i]) + winners3.count(
                winners[i])
        if trainers[i] not in betvalue1.keys():
            betvalue1[trainers[i]] = 7 * trainers.count(trainers[i]) + 3 * trainers2.count(
                trainers[i]) + trainers3.count(trainers[i])
        if horses[i] not in betvalue2.keys():
            betvalue2[horses[i]] = 7 * horses.count(horses[i]) + 3 * horses2.count(horses[i]) + horses3.count(horses[i])

    betvaluefinal = sorted(betvalue.items(), key=lambda x: -x[1])  # ordered by value
    betvalue1final = sorted(betvalue1.items(), key=lambda x: -x[1])  # ordered by value
    betvalue2final = sorted(betvalue2.items(), key=lambda x: -x[1])  # ordered by value

    bestwinner = betvaluefinal[0][0]  # most points jockey
    besttrainer = betvalue1final[0][0]  # most points trainer
    besthorse = betvalue2final[0][0]  # most points horse

    # Question 3

    inpo = sorted(inp2, key=lambda x: (x['racedate'], x['raceno']))  # data ordered by date first, then raceindex

    for i in range(len(inpo)):
        a = (int(inpo[i]['raceno']), inpo[i]['racedate'])
        raceorder.append(a)

    raceunique = sorted(set(raceorder), key=lambda x: (x[0], x[1]))

    for i in range(len(raceunique)):
        raceunique[i] = [raceunique[i]]

    for i in range(len(raceunique)):
        for j in range(len(inpo)):
            if raceunique[i][0][0] == inpo[j]['raceno'] and raceunique[i][0][1] == inpo[j]['racedate']:
                a = (inpo[j]['jockeycode'], int(inpo[j]['Placing']))
                raceunique[i].append(a)

    for i in range(len(raceunique)):
        popped = raceunique[i][0]
        raceunique[i].pop(0)
        raceunique[i] = filter(lambda x: x[1] > 0, raceunique[i])
        raceunique[i] = sorted(raceunique[i], key=lambda x: x[1])
        raceunique[i].insert(0, popped)

    q3 = []
    dates = []
    jockeys = []

    def check1(z1, z2, z3):
        for f in range(1, (len(z1) - 2)):
            name1 = z1[f][0]
            name2 = z1[f + 1][0]
            name3 = z1[f + 2][0]
            for g in range(1, (len(z2) - 2)):
                if name1 in z2[g] and name2 in z2[g + 1] and name3 in z2[g + 2]:
                    for h in range(1, (len(z3) - 2)):
                        if name1 in z3[h] and name2 in z3[h + 1] and name3 in z3[h + 2]:
                            jockeys.append([name1, name2, name3])
                            return True
                        else:
                            continue
                else:
                    continue
            else:
                continue

    for i in range((len(raceunique) - 2)):
        if raceunique[i][0][0] - raceunique[i + 1][0][0] == -1:
            if raceunique[i + 1][0][0] - raceunique[i + 2][0][0] == -1:
                check1(raceunique[i], raceunique[i + 1], raceunique[i + 2])
                if True:
                    dates.append([str(raceunique[i][0][1]) + ":" + str(raceunique[i][0][0]),
                                  str(raceunique[i + 1][0][1]) + ":" + str(raceunique[i + 1][0][0]),
                                  str(raceunique[i + 2][0][1]) + ":" + str(raceunique[i + 2][0][0])])
                else:
                    continue
            else:
                continue
        else:
            continue

    for i in range(len(jockeys)):
        q3.append({"jockeys": jockeys[i], "races": dates[i]})

    ans = {"q1": {"horse": finalhorse, "jockey": finalwinner, "trainer": finaltrainer},
           "q2": {"horse": besthorse, "jockey": bestwinner, "trainer": besttrainer}, "q3": q3}
    return ans