from find_bubbles import *
from clusters import *
from plots import *
import cv2
import os
import csv


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


# clip = 'HMM_201311191039'
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


def evaluate(mode, directory, clip=None, start=None, end=None):
    if mode == 'analysis':
        # extract
        # create mask
        analysis(directory, clip, start, end)
    elif mode == 'interp':
        # interp()
        pass
    else:
        # extract
        # create mask
        analysis(directory, clip, start, end)
        # interp()


def analysis(directory, clip, start=0, end=None):
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # init fourcc code
    if clip:
        clips = [clip]
    else:
        clips = os.listdir(directory)
    if not end:  # if no end parameter given
        end = len(os.listdir(directory)) - 1

    for clip in clips:
        subplot_video = cv2.VideoWriter('{}.avi'.format(clip), fourcc, 3, (745, 1110))  # init vid creation
        clip_directory = os.path.join(directory, clip)  # create clip dir
        os.chdir(clip_directory)
        cluster_file = open('clusters.csv', 'w', newline='')
        writer = csv.writer(cluster_file)
        # create directories for all created figures
        os.makedirs('loc_frames'), os.makedirs('map_frames'), os.makedirs('Results'), os.makedirs('subplots')
        os.makedirs('hists')
        mask_ref = clip + '_mask.png'
        mask = cv2.imread(mask_ref)  # TODO Automate mask creation by id_ellipses
        pixels = list_pixels(mask)  # create list of lake pixel coords only

        section_list = list()
        clip_lists = dict([('loc_all', list()), ('loc_less', list()), ('cluster_act', list()),
                           ('cluster_all', list()), ('cluster_loc_x', list()), ('cluster_loc_y', list())])
        bubble_count = 0

        # list through each frame in clip
        for i in range(start, end):
            os.chdir(clip_directory)
            frame_ref = 'frame{}.jpg'.format(i)
            loc_frame_ref = 'C:/Users/haydn/PycharmProjects/Dissertation/{}/loc_frames/{}'.format(clip, frame_ref)
            frame = cv2.imread(frame_ref)
            print(frame_ref)  # is there another way to monitor progress
            centres, loc_frame, section_list = locate(frame, pixels, clip, i, section_list)  # locate centres
            bubble_count += len(centres)
            clip_lists['loc_all'].extend(centres), clip_lists['loc_less'].extend(centres)
            cv2.imwrite(loc_frame_ref, loc_frame)
            # for each frame plot locations, create subplot with org frame and gen vid:
            plot_bubbles(clip_lists['loc_all'], frame, clip, frame_ref)
            gen_subplot(clip, frame_ref)  # change frame to map of locations
            gen_video(clip, subplot_video, frame_ref)
            clip_lists['cluster_act'], clip_lists['cluster_all'] = id_clusters(centres, clip_lists['cluster_act'],
                                                                               clip_lists['cluster_all'], i)
        cluster_locations(clip_lists, bubble_limit, writer, section_list)  # update cluster list, create x,y
