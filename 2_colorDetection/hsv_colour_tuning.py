# https://www.instructables.com/Color-Detection-in-Python-Using-OpenCV/
# https://www.rapidtables.com/web/color/RGB_Color.html
import cv2
import numpy as np


def empty():
    pass


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 600, 300)
cv2.createTrackbar("Hue min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Hue max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Sat min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val max", "TrackBars", 255, 255, empty)


while True:

    img = cv2.imread("colourmap.jpg")
    img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    # resize = cv2.resize(img, (400, 300))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val max", "TrackBars")
    print("Lower = ", h_min, s_min, v_min, " & ", "Upper = ", h_max, s_max, v_max)
    lower = np.array([h_min, s_min, v_min], dtype=np.uint8)
    upper = np.array([h_max, s_max, v_max], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("img", img)
    cv2.imshow("Output", mask)
    result = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("Result", result)
    if cv2.waitKey(1) & 0xFF == 27:  # ord("q"):
        break
cv2.destroyAllWindows()
