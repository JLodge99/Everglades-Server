#import testcombat
import subprocess

targetSystems = ["lowestHealth", "lowestHealth"]
maxIterations = 2

if __name__ == '__main__':
    for i in range(maxIterations):
        subprocess.call('python testcombat.py')
        # exec("testcombat")