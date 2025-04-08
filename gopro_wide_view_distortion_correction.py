import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = 'D:/CV/homework/Gopro_Wide_Calibration_with_OpenCV/data/chessboard.avi'
K = np.array(
 #=================1 image================================================
# [[3.13001947e+02, 0.00000000e+00, 1.04185593e+03],
#  [0.00000000e+00, 2.73523647e+02, 5.67008972e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
 #=================44 images================================================
 #    [[760.60913613,   0,         966.35761847],
 # [  0,         708.76761067, 539.17018328],
 # [  0,           0,           1        ]]
 #=================76 images================================================
[[792.86298416,   0,         952.48662826],
 [  0,         734.3632487,  534.80188396],
 [  0,           0,           1        ]]
             ) # Derived from `calibrate_camera.py`
dist_coeff = np.array(
    # =================1 image================================================
    # [-0.03887438,  0.00777214,  0.00043639,  0.0014292,  -0.00086478]
    # =================44 images================================================
    # [-0.23078145,  0.17038474,  0.00320475,  0.00778075, -0.06751446]
    # =================76 images================================================
    [-0.24012391,  0.16793469, -0.00373626,  0.00596004, -0.06071182]
)

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# Run distortion correction
show_rectify = True
map1, map2 = None, None
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Rectify geometric distortion (Alternative: `cv.undistort()`)
    info = "Original"
    if show_rectify:
        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1)
        img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
        info = "Rectified"
    cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow("Geometric Distortion Correction", img)
    key = cv.waitKey(10)
    if key == ord(' '):     # Space: Pause
        key = cv.waitKey()
    if key == 27:           # ESC: Exit
        break
    elif key == ord('\t'):  # Tab: Toggle the mode
        show_rectify = not show_rectify

video.release()
cv.destroyAllWindows()
