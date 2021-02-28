import os
import subprocess

if __name__ == '__main__':
    #1
    x = os.system('ls -a')

    #2
    y = subprocess.run(args=['ls', '-l'], capture_output=True)
    print(y.stdout)

    # onmt_translate -model toy-ende/run/model_step_1000.pt -src toy-ende/src-test.txt -output toy-ende/pred_1000.txt -gpu 0 -verbose


