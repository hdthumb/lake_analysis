import cv2


def clip_mask():
    test_frame = cv2.imread('frame0.jpg')  # read in frame
    frame_grey = cv2.cvtColor(test_frame, cv2.COLOR_RGB2GRAY)
    ret, thresh_frame = cv2.threshold(frame_grey, 200, 255, cv2.THRESH_BINARY)
    print(type(thresh_frame))
    # edge_frame_thresh = cv2.Canny(thresh_frame, 150, 200)  # apply canny edge detection
    cv2.imwrite('edge0.jpg', thresh_frame)


clip_mask()
