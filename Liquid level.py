import cv2 as cv
import numpy as np

vid = cv.VideoCapture("Vid/Water Filling Graduated Cylinder - constant rate.mp4")
width = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('new.mp4', fourcc, 20.0, (width, height))

while vid.isOpened():
    ret, frame = vid.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    low_green = np.array([52, 0, 55])
    upper_green = np.array([104, 255, 255])

    mask = cv.inRange(hsv, low_green, upper_green)
    edges = cv.Canny(mask, 75, 100)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

    x, y, w, h = cv.boundingRect(mask)  # drawing the ractangle
    liquid_level = h / 6.9
    cv.putText(frame, f"liquid level = {np.round(liquid_level)} ml", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.7,
               (0, 0, 255), 2)
    cv.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)

    #     print(x,y,w,h)
    out.write(frame)

    cv.imshow('frame', frame)
    #     cv.imshow('mask', mask)
    #     cv.imshow('edges',edges)

    key = cv.waitKey(25)
    if key == 27 & 0xff == ord('q'):
        break

vid.release()
out.release()
cv.destroyAllWindows()



