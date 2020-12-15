from find_bubbles_lk import *
from clusters_lk import *
from plots_lk import *
import cv2
import os


# change clip below

clip = 'HMM_201311191039'
# clip = 'HMM_201407231344'
# clip = 'HMM_201312030418'

# provide parameters for each section below:

# HMM_201311191039
# ranges = [range(1, 35), range(35, 90), range(90, 120), range(120, 455), range(455, 550), range(550, 675)]
ranges = [range(1, 35), range(90, 120), range(120, 455), range(550, 675)]  # remove rockfall events. 78% remaining
frame_limits = [1, 20, 50, 75, 50, 50]
bubble_counts = [3, 15, 15, 50, 20, 30]
# HMM_201407231344
# ranges = [range(1, 57), range(57, 98), range(98, 190), range(190, 961)]
# frame_limits = [15, 20, 40, 70]
# bubble_counts = [15, 15, 30, 50]
# HMM_201312030218
# ranges = [range(1, 73), range(73, 476), range(476, 961)]
# frame_limits = [15, 30, 50]
# bubble_counts = [30, 200, 200]

project_directory = os.getcwd()
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
subplot_video = cv2.VideoWriter('{}.avi'.format(clip), fourcc, 3, (745, 1110))
clip_directory = os.path.join(project_directory, clip)  # go to dir for each clip
os.chdir(clip_directory)
# create directories for all created figures
os.makedirs('loc_frames'), os.makedirs('map_frames'), os.makedirs('hists'), os.makedirs('subplots')
mask_ref = clip + '_mask.png'
mask = cv2.imread(mask_ref)
# dimensions = mask.shape  # this variable is imported into plots.py for all plotting functions to use
pixels = list_pixels(mask)  # create list of lake pixel coords only

# innit clip lists
clip_lists = dict([('loc_all', list()), ('loc_less', list()), ('cluster_list', list())])

# loop through each section in clip
for s in range(len(ranges)):
    # init section lists
    sect_lists = dict([('loc_all', list()), ('loc_less', list()), ('cluster_list', list())])
    # list through each frame in section
    for i in ranges[s]:
        os.chdir(clip_directory)
        frame_ref = 'frame{}.jpg'.format(i)
        loc_frame_ref = 'C:/Users/haydn/PycharmProjects/Dissertation/{}/loc_frames/{}'.format(clip, frame_ref)
        frame = cv2.imread(frame_ref)
        print(frame_ref)  # to track progress in console
        centres, loc_frame = locate(frame, pixels)  # call func to locate centres of bubble burstse
        clip_lists['loc_all'].extend(centres), clip_lists['loc_less'].extend(centres)
        sect_lists['loc_all'].extend(centres), sect_lists['loc_less'].extend(centres)
        cv2.imwrite(loc_frame_ref, loc_frame)
        # for each frame plot locations, create subplot with org frame and gen vid:
        plot_bubbles(sect_lists['loc_all'], frame, clip, 999, frame_ref)
        gen_subplot(clip, frame_ref)  # change frame to map of locations
        gen_video(clip, subplot_video, frame_ref)
        sect_lists['cluster_list'] = id_clusters(centres, sect_lists['cluster_list'], frame_limits, s)  # id cl
    # append sections clusters to clips cluster list
    clip_lists['cluster_list'].extend(sect_lists['cluster_list'])
    # for each section plot: all bubbles, clusters only, combo
    cluster_locations(sect_lists, bubble_counts, s)
    plot_clusters(clip, sect_lists['cluster_loc_x'], sect_lists['cluster_loc_y'], s, frame, 0)
    plot_bubbles(sect_lists['loc_all'], frame, clip, s, None)  # plot all bubble locations for section
    # plot cluster locations and locations of bubbles not within a cluster
    plot_both(sect_lists['loc_less'], sect_lists['cluster_loc_x'], sect_lists['cluster_loc_y'], frame, clip, s)

subplot_video.release()
# plot all locations from all sections
plot_bubbles(clip_lists['loc_all'], frame, clip, 'All', None)
# plot cluster locations and locations not in cluster for all sections
cluster_locations(clip_lists, bubble_counts, s)  # find locations of bubbles not in cluster
plot_both(clip_lists['loc_less'], clip_lists['cluster_loc_x'], clip_lists['cluster_loc_y'],
          frame, clip, 'All')

