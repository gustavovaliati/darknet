import os, glob, sys, argparse, datetime, random

ap = argparse.ArgumentParser()

ap.add_argument("-d", "--dataset_path",
                required = True,
                default=None,
                type=str,
                help = "The PTI01 dataset root path location.")
ap.add_argument("-t", "--test_percentage",
                required = False,
                default=0.2,
                type=float,
                help = "The percentage for testing.")
ap.add_argument("-s", "--shuffle",
                required = False,
                default=True,
                type=bool,
                help = "The dataset should be splited before split?")

ARGS = ap.parse_args()

img_list =  glob.glob(os.path.join(ARGS.dataset_path,'**/*.jpg'), recursive=True)

total_count = len(img_list)
if total_count <= 0:
    raise Exception("There are not jpg images in the provided dataset folder.")
test_count = int(total_count * ARGS.test_percentage)
if test_count <= 0:
    raise Exception("Not enough image for the test set.")
train_count = total_count - test_count

dataset_version = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
train_file_path = 'train_pti01_{}imgs_v{}.txt'.format(train_count, dataset_version)
test_file_path = 'test_pti01_{}imgs_v{}.txt'.format(test_count, dataset_version)

if ARGS.shuffle:
    random.shuffle(img_list)

with open(train_file_path, 'w') as train_file:
    with open(test_file_path, 'w') as test_file:
        checked_folders = []
        for img in img_list:
            '''
            We are splitting the dataset by folder.
            Normally each folder represents a different camera.
            So we get a better representative splitting of train/test.
            '''
            folder = os.path.dirname(img)
            if not folder in checked_folders: #Procced only if the folder has never been verified
                checked_folders.append(folder) #mark this folder as checked.

                folder_images = [ im for im in img_list if os.path.dirname(im) == folder ]
                folder_total_count = len(folder_images)
                folder_test_count = int(folder_total_count * ARGS.test_percentage)
                folder_train_count = folder_total_count - folder_test_count
                for im in folder_images[:folder_train_count]:
                    train_file.write(im+'\n')
                for im in folder_images[folder_train_count:]:
                    test_file.write(im+'\n')

                print('Folder {}, {} imgs: train {} | test {}'.format(folder, folder_total_count, folder_train_count, folder_test_count))
