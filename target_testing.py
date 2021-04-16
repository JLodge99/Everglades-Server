#import testcombat
import subprocess
import pandas
import threading

targetType = "lethal-vs-lethal" # Valid options: randomlySelect, lowestHealth, highestHealth, mostLethal
targetType0 = "mostLethal"
targetType1 = "mostLethal"
targetSystems = [targetType0, targetType1]
maxIterations = 500
collectiveStats = "collectiveStats.txt"

def processData(filename, output):
    df = pandas.read_csv(filename)
    output.write(targetType0 + " vs " + targetType1 + "\n")
    # playerFreq = df['winner'].value_counts()
    #("player,damage dealt,units killed, groups killed\n")
    # player0 = df[df.player == '0']
    # player1 = df[df.player == '1']
    player0 = df.loc[df['player'] == 0]
    player1 = df.loc[df['player'] == 1]

    damageMean0 = player0['damage dealt'].mean()
    damageMode0 = player0['damage dealt'].mode()[0]
    damageMedian0 = player0['damage dealt'].median()
    damageMin0 = player0['damage dealt'].min()
    damageMax0 = player0['damage dealt'].max()

    unitsMean0 = player0['units killed'].mean()
    unitsMode0 = player0['units killed'].mode()[0]
    unitsMedian0 = player0['units killed'].median()
    unitsMin0 = player0['units killed'].min()
    unitsMax0 = player0['units killed'].max()

    groupsMean0 = player0['groups killed'].mean()
    groupsMode0 = player0['groups killed'].mode()[0]
    groupsMedian0 = player0['groups killed'].median()
    groupsMin0 = player0['groups killed'].min()
    groupsMax0 = player0['groups killed'].max()

    # Player 1 setup
    damageMean1 = player1['damage dealt'].mean()
    damageMode1 = player1['damage dealt'].mode()[0]
    damageMedian1 = player1['damage dealt'].median()
    damageMin1 = player1['damage dealt'].min()
    damageMax1 = player1['damage dealt'].max()

    unitsMean1 = player1['units killed'].mean()
    unitsMode1 = player1['units killed'].mode()[0]
    unitsMedian1 = player1['units killed'].median()
    unitsMin1 = player1['units killed'].min()
    unitsMax1 = player1['units killed'].max()

    groupsMean1 = player1['groups killed'].mean()
    groupsMode1 = player1['groups killed'].mode()[0]
    groupsMedian1 = player1['groups killed'].median()
    groupsMin1 = player1['groups killed'].min()
    groupsMax1 = player1['groups killed'].max()

    output.write("Player 0:\n")
    output.write("Damage Mean: " + str(damageMean0) + "\n")
    output.write("Damage Mode: " + str(damageMode0) + "\n")
    output.write("Damage Median: " + str(damageMedian0) + "\n")
    output.write("Damage Min: " + str(damageMin0) + "\n")
    output.write("Damage Max: " + str(damageMax0) + "\n")

    output.write("Units Killed Mean: " + str(unitsMean0) + "\n")
    output.write("Units Killed Mode: " + str(unitsMode0) + "\n")
    output.write("Units Killed Median: " + str(unitsMedian0) + "\n")
    output.write("Units Killed Min: " + str(unitsMin0) + "\n")
    output.write("Units Killed Max: " + str(unitsMax0) + "\n")

    output.write("Groups Killed Mean: " + str(groupsMean0) + "\n")
    output.write("Groups Killed Mode: " + str(groupsMode0) + "\n")
    output.write("Groups Killed Median: " + str(groupsMedian0) + "\n")
    output.write("Groups Killed Min: " + str(groupsMin0) + "\n")
    output.write("Groups Killed Max: " + str(groupsMax0) + "\n")

    output.write("Player 1:\n")
    output.write("Damage Mean: " + str(damageMean1) + "\n")
    output.write("Damage Mode: " + str(damageMode1) + "\n")
    output.write("Damage Median: " + str(damageMedian1) + "\n")
    output.write("Damage Min: " + str(damageMin1) + "\n")
    output.write("Damage Max: " + str(damageMax1) + "\n")

    output.write("Units Killed Mean: " + str(unitsMean1) + "\n")
    output.write("Units Killed Mode: " + str(unitsMode1) + "\n")
    output.write("Units Killed Median: " + str(unitsMedian1) + "\n")
    output.write("Units Killed Min: " + str(unitsMin1) + "\n")
    output.write("Units Killed Max: " + str(unitsMax1) + "\n")

    output.write("Groups Killed Mean: " + str(groupsMean1) + "\n")
    output.write("Groups Killed Mode: " + str(groupsMode1) + "\n")
    output.write("Groups Killed Median: " + str(groupsMedian1) + "\n")
    output.write("Groups Killed Min: " + str(groupsMin1) + "\n")
    output.write("Groups Killed Max: " + str(groupsMax1) + "\n\n")

    # averageHealth = df['average health'].mean()
    # stdHealth = df['average health'].std()

    # averageUnits = df['total units left'].mean()
    # stdUnits = df['total units left'].std()

    # output.write(playerFreq.to_string() + "\n")
    # output.write("Average Health Left: " + str(averageHealth) + "\n")
    # output.write("Average Health SD: " + str(stdHealth) + "\n")

    # output.write("Average Units Left: " + str(averageUnits) + "\n")
    # output.write("Average Units SD: " + str(stdUnits) + "\n")
    output.close()

if __name__ == '__main__':
    outputFile = open(targetType + "-stats.csv", "w")
    collectiveFile = open(collectiveStats, "a")

    #outputFile.write("winner,average health,total units left\n")
    outputFile.write("player,damage dealt,units killed,groups killed\n")
    outputFile.close()

    for i in range(maxIterations):
        print("Current Iteration:", i)
        subprocess.call('python testbattle.py', shell = False)

    processData(targetType + "-stats.csv", collectiveFile)
    outputFile.close()

