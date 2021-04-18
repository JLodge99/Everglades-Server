import subprocess
import pandas

# targetType will be the name of the outputted .csv file.
targetType = "lethal-vs-lethal" # Valid options: randomlySelect, lowestHealth, highestHealth, mostLethal
# These two variables determine which targeting system is used by what player.
targetType0 = "mostLethal"
targetType1 = "mostLethal"
targetSystems = [targetType0, targetType1]
# Determines how many games to run.
maxIterations = 1 # Temporarily set to 1
# The output file where processData() outputs to.
collectiveStats = "collectiveStats.txt"

# Procesess the data placed in the various targeting statistics .csv files
def processData(filename, output):
    df = pandas.read_csv(filename)
    output.write(targetType0 + " vs " + targetType1 + "\n")

    player0 = df.loc[df['player'] == 0]
    player1 = df.loc[df['player'] == 1]

    # Player 0 Setup
    # Takes various statistics on the damage dealt per round.
    damageMean0 = player0['damage dealt'].mean()
    damageMode0 = player0['damage dealt'].mode()[0]
    damageMedian0 = player0['damage dealt'].median()
    damageMin0 = player0['damage dealt'].min()
    damageMax0 = player0['damage dealt'].max()

    # Takes various statistics on the number of units killed per round.
    unitsMean0 = player0['units killed'].mean()
    unitsMode0 = player0['units killed'].mode()[0]
    unitsMedian0 = player0['units killed'].median()
    unitsMin0 = player0['units killed'].min()
    unitsMax0 = player0['units killed'].max()

    # Takes various statistics on the number of groups destroyed per round.
    groupsMean0 = player0['groups killed'].mean()
    groupsMode0 = player0['groups killed'].mode()[0]
    groupsMedian0 = player0['groups killed'].median()
    groupsMin0 = player0['groups killed'].min()
    groupsMax0 = player0['groups killed'].max()

    # Player 1 setup
    # Takes various statistics on the damage dealt per round.
    damageMean1 = player1['damage dealt'].mean()
    damageMode1 = player1['damage dealt'].mode()[0]
    damageMedian1 = player1['damage dealt'].median()
    damageMin1 = player1['damage dealt'].min()
    damageMax1 = player1['damage dealt'].max()

    # Takes various statistics on the number of units killed per round.
    unitsMean1 = player1['units killed'].mean()
    unitsMode1 = player1['units killed'].mode()[0]
    unitsMedian1 = player1['units killed'].median()
    unitsMin1 = player1['units killed'].min()
    unitsMax1 = player1['units killed'].max()

    # Takes various statistics on the number of groups destroyed per round.
    groupsMean1 = player1['groups killed'].mean()
    groupsMode1 = player1['groups killed'].mode()[0]
    groupsMedian1 = player1['groups killed'].median()
    groupsMin1 = player1['groups killed'].min()
    groupsMax1 = player1['groups killed'].max()

    # Output the collected data to the output file.
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

    output.close()

# Runs the game for the amount of iterations specified.
if __name__ == '__main__':
    outputFile = open(targetType + "-stats.csv", "w")
    collectiveFile = open(collectiveStats, "a")

    # Initialize the columns of hte output file.
    outputFile.write("player,damage dealt,units killed,groups killed\n")
    outputFile.close()

    # This can be heavily improved upon with multithreading.
    for i in range(maxIterations):
        print("Current Iteration:", i)
        subprocess.call('python testbattle.py', shell = False)

    processData(targetType + "-stats.csv", collectiveFile)
    outputFile.close()

