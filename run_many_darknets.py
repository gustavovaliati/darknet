import os, sys, glob, shutil

file_names = glob.glob(os.path.join('/home/grvaliati/workspace/datasets/pti/PTI01/', '**/*.jpg'), recursive=True)
file_names.sort()
for index, file_name in enumerate(file_names):
    #if index >= 2:
    #    sys.exit()

    command = './darknet detector test cfg/coco.data cfg/yolo.cfg /home/grvaliati/workspace/darknet-resources/yolo.weights {}'.format(file_name)
    os.system(command)
    print(file_name)
    new_image = './test2' + file_name
    new_image_dir = os.path.dirname(new_image)
    os.makedirs(new_image_dir, exist_ok=True)
    shutil.move('predictions.jpg', new_image)

