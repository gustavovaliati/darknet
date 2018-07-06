import os, glob
from os.path import basename

command = "./darknet detector recall cfg/voc.data cfg/yolo-voc.cfg {} &> backup/recall_{}.txt && \n"

files = glob.glob("backup/*.weights")
files.sort()
#files.append("yolo-voc.backup")

commands_file = open("commands.sh", "w")

for f in files:
    commands_file.write(command.format(f,basename(f)))


files = glob.glob("backup/recall_*.weights.txt")
files.sort()
command_header = "echo '{}' >> backup/recall_result.txt && \n"
command_tail = "tail -n 1 {} >> backup/recall_result.txt && \n"
for f in files:
    commands_file.write(command_header.format(f))
    commands_file.write(command_tail.format(f))

