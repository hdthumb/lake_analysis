from find_bubbles import *
from clusters import *
from plots import *
import cv2
import os
import csv

# change clip below

clip = 'HMM_201311191039'
# clip = 'HMM_201407231344'
# clip = 'HMM_201312030418'

# provide parameters for each section below:

# HMM_201311191039
# ranges = [range(1, 35), range(35, 90), range(90, 120), range(120, 455), range(455, 550), range(550, 675)]
# ranges = [range(1, 35), range(90, 120), range(120, 455), range(550, 675)]  # remove rockfall events. 78% remaining
# seq_limits = [5, 20, 50, 75, 50, 50]  # limit for bubbles in cluster to be sequential
# seq_limit = 10
# bubble_counts = [3, 15, 15, 50, 20, 30]


# HMM_201407231344
# ranges = [range(1, 57), range(57, 98), range(98, 190), range(190, 961)]
# frame_limits = [15, 20, 40, 70]
# seq_limits = [15, 15, 30, 50]

# HMM_201312030218
# ranges = [range(1, 73), range(73, 476), range(476, 961)]
# frame_limits = [15, 30, 50]
# seq_limits = [30, 200, 200]

project_directory = os.getcwd()  # folder directory
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # init fourccc code
subplot_video = cv2.VideoWriter('{}.avi'.format(clip), fourcc, 3, (745, 1110))  # init vid creation
clip_directory = os.path.join(project_directory, clip)  # create clip dir
os.chdir(clip_directory)
## below not present in diss_main
clip_length = len(os.listdir(clip_directory)) - 1
cluster_file = open('clusters.csv', 'w', newline='')
writer = csv.writer(cluster_file)
##
# create directories for all created figures
os.makedirs('loc_frames'), os.makedirs('map_frames'), os.makedirs('Results'), os.makedirs('subplots')
os.makedirs('hists')
mask_ref = clip + '_mask.png'
mask = cv2.imread(mask_ref)  # TODO Automate mask creation by id_ellipses
pixels = list_pixels(mask)  # create list of lake pixel coords only

# innit clip lists
# clip_lists = dict([('loc_all', list()), ('loc_less', list()), ('cluster_all', list()),
#                    ('cluster_loc_x', list()), ('cluster_loc_y', list())])
# loop through each section in clip
# for s in range(len(ranges)):
# refresh section lists
section_list = list()
clip_lists = dict([('loc_all', list()), ('loc_less', list()), ('cluster_act', list()), ('cluster_all', list()),
                   ('cluster_loc_x', list()), ('cluster_loc_y', list())])
bubble_count = 0

# list through each frame in section
for i in range(clip_length):
    os.chdir(clip_directory)
    frame_ref = 'frame{}.jpg'.format(i)
    loc_frame_ref = 'C:/Users/haydn/PycharmProjects/Dissertation/{}/loc_frames/{}'.format(clip, frame_ref)
    frame = cv2.imread(frame_ref)
    print(frame_ref)
    centres, loc_frame, section_list = locate(frame, pixels, clip, i, section_list)  # locate centres of bubble bursts
    bubble_count += len(centres) ##different
    # clip_lists['loc_all'].extend(centres), clip_lists['loc_less'].extend(centres)
    clip_lists['loc_all'].extend(centres), clip_lists['loc_less'].extend(centres)
    ##sect list append here in diss_main
    cv2.imwrite(loc_frame_ref, loc_frame)
    # for each frame plot locations, create subplot with org frame and gen vid:
    plot_bubbles(clip_lists['loc_all'], frame, clip, frame_ref)
    gen_subplot(clip, frame_ref)  # change frame to map of locations
    gen_video(clip, subplot_video, frame_ref)
    ## sect lists here instead of clip lists below
    clip_lists['cluster_act'], clip_lists['cluster_all'] = id_clusters(centres, clip_lists['cluster_act'],
                                                                       clip_lists['cluster_all'], seq_limit, i)

cluster_locations(clip_lists, bubble_count, writer, section_list)  # update cluster list and create cluster x, y lists

# add section clusters lists to clip cluster lists
# clip_lists['clu++ster_all'].extend(sect_lists['cluster_all'])
# clip_lists['cluster_loc_x'].extend(sect_lists['cluster_loc_x'])
# clip_lists['cluster_loc_y'].extend(sect_lists['cluster_loc_y'])


# for each section plot: all bubbles, clusters only, combo
# plot_clusters(clip, sect_lists['cluster_loc_x'], sect_lists['cluster_loc_y'], s, frame, 0)
# plot_bubbles(sect_lists['loc_all'], frame, clip, s)  # plot all bubble locations for section. why the none
# plot cluster locations and locations of bubbles not within a cluster
# plot_both(sect_lists['loc_less'], sect_lists['cluster_loc_x'], sect_lists['cluster_loc_y'], frame, clip, s)

# subplot_video.release()
# plot all locations from all sections
# plot_bubbles(clip_lists['loc_all'], frame, clip, 'All')
# plot cluster locations and locations not in cluster for all sections
# plot_both(clip_lists['loc_less'], clip_lists['cluster_loc_x'], clip_lists['cluster_loc_y'],
#           frame, clip, 'All')
