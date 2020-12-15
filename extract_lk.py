import cv2
import os
import shutil


clips = ['HMM_201312030418.mov']
project_directory = os.getcwd()
print(project_directory)
for clip_name in clips:
    final_directory = os.path.join(project_directory, clip_name[0:len(clip_name) - 4])  # generate dir name
    os.makedirs(final_directory)  # make dir
    shutil.move(project_directory + '\\' + clip_name, final_directory + '\\' + clip_name)  # move clip into clip dir
    os.chdir(final_directory)
    clip = cv2.VideoCapture(clip_name)
    success, image = clip.read()  # read first frame of clip, retval = true if another frame to read
    count = 0
    while success:  # while retval = true, loop through frames of clip
        cv2.imwrite("frame{}.jpg".format(count), image)
        success, image = clip.read()
        # cv2.imwrite("frame{}.jpg".format(count), image)  # was commented out before
        count += 1

print('complete')

