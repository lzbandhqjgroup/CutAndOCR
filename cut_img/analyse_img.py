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


def make_area(x_lines,y_lines):
    '''
    返回一系列被直线框起来的封闭矩形区域
    :param x_lines:
    :param y_lines:
    :return: list(rec)
    '''
    # 大概思路是这样，遍历xline，找到和两条以上yline相交的，再找到一条xline和其中两条yline都相交
    x_joined = {}
    y_joined = {}
    for each_x in x_lines:
        x_joined[each_x] = [each_y for each_y in y_lines if if_joined(each_x,each_y)]

    for each_x,value in x_joined.iteritems():
        if not len(value) >= 2:     #和2条以上y相交
            continue
        for another_x in x_joined:
            if each_x == another_x:
                continue
            intersec = list(set(value).intersection(set(x_joined[another_x])))          #求交集
            if len(intersec) >=2:       #相同的y条数大于2
                #这里开始切出选中的矩形区域
                None

    return


def if_joined(a,b):
    #判断两条直线是否有焦点
    None

read_image("5958.jpg")