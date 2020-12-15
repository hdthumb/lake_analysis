import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt


# def disp_frame(name, src):
#     # function to display frames so they fit my laptop screen
#     re_frame = cv2.resize(src, (1360, 780))  # Resize image to laptop dimensions
#     cv2.imshow(name, re_frame)
#     cv2.waitKey(0)


def list_pixels(mask):
    pixels = list()
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if np.all(mask[i, j]):
                pass
            else:
                pixels.append([i, j])  # else append to PIO list
    return pixels


# def gen_hist(frame, pixels):
#     frame_grey = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#     # init contour mask for locate func here to reduce total loop counts
#     mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
#     intents = list()
#     for i in range(len(pixels)):
#         ref = pixels[i]
#         intent = frame_grey[ref[0], ref[1]]
#         intents.append(intent)
#         if intent > 245:  # set pixel intensity sensitivity for mask here
#             mask[ref[0], ref[1]] = 1
#     frame_binary = cv2.bitwise_and(frame, frame, mask=mask)  # binop w mask to create binary frame for locate func
#     # plt.hist(intents, 255)
#     # plt.show()
#     return intents, frame_binary


def rect_ratio(contour, frame_binary):
    x, y, w, h = cv2.boundingRect(contour)
    bubble_pixels = 0
    for i in range(w):
        for j in range(h):
            if np.all(frame_binary[y + j, x + i][0]):
                bubble_pixels += 1
    ratio = bubble_pixels/(w * h)
    return ratio


def locate(frame, pixels):
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # init contour mask for locate func here to reduce total loop counts
    mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
    intents = list()
    for i in range(len(pixels)):
        ref = pixels[i]
        intent = frame_grey[ref[0], ref[1]]
        intents.append(intent)
        if intent > 245:  # set pixel intensity sensitivity for mask here
            mask[ref[0], ref[1]] = 1
    frame_binary = cv2.bitwise_and(frame, frame, mask=mask)  # binop w mask to create binary frame for locate func
    # plt.hist(intents, 255)
    # plt.show()

    #################################################
    # dont really understand eveything above... go over it to make sure it is actually needed
    # look into moving creating a hist into extract
    #################################################

    frame_final = frame.copy()
    grey_bin_frame = cv2.cvtColor(frame_binary, cv2.COLOR_BGR2GRAY)

    # find contours in the edge map
    contours = cv2.findContours(grey_bin_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    centres = list()
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 15:  # set contour area condition
            rect = cv2.minAreaRect(contours[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            rect_width = rect[1][0]
            rect_height = rect[1][1]
            rect_aspect = rect_height/rect_width
            if 0.25 < rect_aspect < 4:
                if len(contours[i]) > 5:
                    ratio = rect_ratio(contours[i], frame_binary)
                    if ratio > 0.35:
                        cv2.drawContours(frame_final, [box], 0, (0, 0, 255), 2)  # draw min area rect red
                        centres.append(rect[0])

    return centres, frame_final



