import os
import subprocess

if __name__ == '__main__':
    #1
    x = os.system('ls -a')

    #2
    y = subprocess.run(args=['ls', '-l'], capture_output=True)
    print(y.stdout)


