import cv2
import numpy as np

# 读取图片，高斯模糊，获取轮廓，识别直线
def read_image(image_str):
    image = cv2.imread(image_str)

    image = cv2.resize(image, (768, 1024), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # binary = cv2.medianBlur(gray, 7)

    gauss = cv2.GaussianBlur(gray, (3, 3), 1)
    maxvalue = 255
    value = cv2.getTrackbarPos("value", "Threshold")
    if (value < 3):
        value = 3
    if (value % 2 == 0):
        value = value + 1

    args = cv2.adaptiveThreshold(gauss, maxvalue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, value, 1)

    binary = cv2.Canny(args, 0, 60, apertureSize=3)

    cv2.imshow("canny", args)
    cv2.imshow("canny2", binary)
    minLineLength = 10
    maxLineGap = 300
    lines = cv2.HoughLinesP(binary, 1, np.pi / 180, 80, minLineLength, maxLineGap)
    analyse_lines(lines,image)

# 对获取直线进行分析
def analyse_lines(lines,image):
    result = image
    srcHeight, srcWidth, channels = image.shape
    print(srcWidth, srcHeight)

    lines = np.insert(lines, 0, [[0, 0, 0, srcHeight - 1]], axis=0)
    lines = np.insert(lines, 0, [[srcWidth - 1, 0, srcWidth - 1, srcHeight - 1]], axis=0)
    lines = np.insert(lines, 0, [[0, srcHeight - 1, srcWidth - 1, srcHeight - 1]], axis=0)

    x_lines = []
    y_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if (y1 == y2):
                y_lines.append([x1,y1,x2,y2])
            else:
                x_lines.append([x1,y1,x2,y2])
    x_lines.sort(key=(lambda x: x[1]))
    print("x_lines:")
    print(x_lines)
    y_lines.sort(key=(lambda x: x[0]))
    print("y_lines:")
    print(y_lines)
    print("------")

    for line in lines:
        print(line)
        for x1, y1, x2, y2 in line:
            cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("rs", result)

    cv2.waitKey(0)



read_image("5958.jpg")