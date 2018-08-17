import yaml
import argparse
import os
from raven import Client
from subprocess import run

ap = argparse.ArgumentParser()

ap.add_argument("-c", "--config_path",
                required = True,
                default=None,
                type=str,
                help = "The yml config file.")

ARGS = ap.parse_args()


sentry_config = None
with open("sentry-config.yml", 'r') as stream:
    sentry_config = yaml.load(stream)
sentry = Client(sentry_config['sentry-url'])

train_config = None
with open(ARGS.config_path, 'r') as stream:
    train_config = yaml.load(stream)

try:
    # ./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg
    os.chdir('../')
    command = ["./darknet", "detector", "train", train_config['data'], train_config['cfg']]
    if not train_config['weights']:
        # scratch
        pass
    else:
        command = command + [train_config['weights']]

    print('command: ', command)
    process_completed = run(command)
    process_completed.check_returncode()
    
except:
    sentry.captureException()
