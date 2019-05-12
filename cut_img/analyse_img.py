import cv2
import os
import numpy as np

# 读取图片，高斯模糊，获取轮廓，识别直线
def read_image(filename):
    path = filename.split(".")[0]
    isExists = os.path.exists(path)
    print(isExists)
    print(path)
    if not isExists:
        os.makedirs(path)

    image = cv2.imread(filename)
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
    binary2 = cv2.Canny(args, 0, 10, apertureSize=3)
    # cv2.imshow("canny", args)

    cv2.namedWindow('canny2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('canny3', cv2.WINDOW_NORMAL)
    cv2.resizeWindow("canny2", 640, 860)
    cv2.resizeWindow("canny3", 640, 860)
    cv2.imshow("canny2", binary)
    cv2.imshow("canny3", binary2)
    minLineLength = 40
    maxLineGap = 30
    lines = cv2.HoughLinesP(binary2, 1, np.pi / 360, 40, minLineLength, maxLineGap)

    lines = analyse_lines(lines, image)

    # make_area(lines[0], lines[1], path, image)
    search_area(lines[0], lines[1], image, filename)

    cv2.waitKey(0)


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
                if (abs(x2 - x1)>40):
                    y_lines.append([x1,y1,x2,y2])
            else:
                x_lines.append([x1,y1,x2,y2])

    #sort x_lines,y_lines
    x_lines.sort(key=(lambda x: x[0]))
    y_lines.sort(key=(lambda y: y[1]))
    print("x_lines:")
    print(x_lines)
    print("y_lines:")
    print(y_lines)
    print("------")

    #delete adjacent lines
    min_len = 20
    x_filter_lines = []
    flag = True
    for i in range(len(x_lines)):
        if i + 1 < len(x_lines):
            if abs(x_lines[i][0] - x_lines[i + 1][0]) < min_len and (abs(x_lines[i][1] - x_lines[i + 1][1]) < min_len or abs(x_lines[i][3] - x_lines[i + 1][3]) < min_len):
                mid_x = int((x_lines[i + 1][0] + x_lines[i][0]) / 2)
                mid_y1 = int((x_lines[i + 1][1] + x_lines[i][1]) / 2)
                mid_y2 = int((x_lines[i + 1][3] + x_lines[i][3]) / 2)

                x_filter_lines.append([mid_x, mid_y1, mid_x, mid_y2])
                flag = False
            else:
                if flag:
                    x_filter_lines.append(x_lines[i])
                else:
                    flag = True
        else:
            if flag:
                x_filter_lines.append(x_lines[i])

    y_filter_lines = []
    flag = True
    for i in range(len(y_lines)):
        if abs((y_lines[i][2] + y_lines[i][0])/2 - srcWidth/2) < min_len:
            if i + 1 < len(y_lines):
                if abs(y_lines[i][1] - y_lines[i + 1][1]) < min_len and (
                        abs(y_lines[i][0] - y_lines[i + 1][0]) < min_len or abs(
                        y_lines[i][2] - y_lines[i + 1][2]) < min_len):
                    mid_y = int((y_lines[i + 1][1] + y_lines[i][1]) / 2)
                    mid_x1 = int((y_lines[i + 1][0] + y_lines[i][0]) / 2)
                    mid_x2 = int((y_lines[i + 1][2] + y_lines[i][2]) / 2)
                    y_filter_lines.append([mid_x1, mid_y, mid_x2, mid_y])
                    flag = False
                else:
                    if flag:
                        y_filter_lines.append(y_lines[i])
                    else:
                        flag = True
            else:
                if flag:
                    y_filter_lines.append(y_lines[i])

    add_len = 15
    for line in x_filter_lines:
        line[1] += add_len
        line[3] -= add_len

    for line in y_filter_lines:
        line[0] -= add_len
        line[2] += add_len

    for line in x_filter_lines+y_filter_lines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 1)


    print("x_filter_lines:")
    print(x_filter_lines)
    print("y_filter_lines:")
    print(y_filter_lines)
    print("------")


    cv2.namedWindow('canny4', cv2.WINDOW_NORMAL)
    cv2.resizeWindow("canny4", 640, 860)
    cv2.imshow("canny4", result)

    return [x_filter_lines,y_filter_lines]


def search_area(x_lines, y_lines, image, path):
    print(if_joined(y_lines[5], x_lines[1]))
    print(if_joined(y_lines[5], x_lines[2]))
    print(if_joined(y_lines[6], x_lines[1]))
    print(if_joined(y_lines[6], x_lines[2]))

    srcHeight, width, channels = image.shape
    flag = True
    cnt = 0
    k = 1
    mid_x = find_mid_x(x_lines, width)
    min_len = 15
    while k < len(y_lines):
        for l_y in range(len(y_lines) - k):
            r_y = l_y + k
            if abs(y_lines[l_y][0] - y_lines[r_y][0]) < min_len or abs(y_lines[l_y][2] - y_lines[r_y][2]) < min_len:
                l_x = mid_x
                r_x = mid_x + 1
                while l_x >= 0 and not (if_joined(x_lines[l_x], y_lines[l_y]) and if_joined(x_lines[l_x], y_lines[r_y])):
                    l_x -= 1
                while r_x < len(x_lines) and not (
                        if_joined(x_lines[r_x], y_lines[l_y]) and if_joined(x_lines[r_x], y_lines[r_y])):
                    r_x += 1
                # if if_joined(x_lines[l_x], y_lines[l_y]) and if_joined(x_lines[l_x], y_lines[r_y]) and if_joined(
                #         x_lines[r_x], y_lines[l_y]) and if_joined(x_lines[r_x], y_lines[r_y]):
                if l_x>=0 and r_x < len(x_lines):
                    x1 = x_lines[l_x][0]
                    x2 = x_lines[r_x][0]
                    y1 = y_lines[l_y][1]
                    y2 = y_lines[r_y][1]
                    print(x1, x2, y1, y2)
                    save_cut_img([x1,y1,x2,y2],cnt,image,path)
                    cnt+=1
        k += 1


def find_mid_x(x_lines, width):
    l = 0
    r = len(x_lines) - 1
    while l < r:
        mid = int((l + r) / 2)
        if x_lines[mid][0] - width/2 > 0:
            r = mid - 1
        else:
            if x_lines[mid][0] - width / 2 < 0:
                l = mid + 1
            else:
                return mid

    return l

#
#
# def make_area(x_lines, y_lines, path, img):
#     '''
#     返回一系列被直线框起来的封闭矩形区域r
#     :param x_lines:
#     :param y_lines:
#     :return: list(rec)
#     '''
#     # 大概思路是这样，遍历xline，找到和两条以上yline相交的，再找到一条xline和其中两条yline都相交
#     x_joined = {}
#     y_joined = {}
#     for each_x in x_lines:
#         x_joined[each_x] = [each_y for each_y in y_lines if if_joined(each_x,each_y)]
#
#     for each_x,value in x_joined.iteritems():
#         if not len(value) >= 2:     #和2条以上y相交
#             continue
#         for another_x in x_joined:
#             if each_x == another_x:
#                 continue
#             intersec = list(set(value).intersection(set(x_joined[another_x])))          #求交集
#             if len(intersec) >=2:       #相同的y条数大于2
#                 #这里开始切出选中的矩形区域
#                 #each_x,another_x, intersec是选出的边框的线
#                 None
#
#     return


def save_cut_img(area,k,image,path):
    filename = path.split(".")[0] + "/" + str(k) + ".jpg"
    print(filename)
    cut_img = image[area[1]:area[3], area[0]:area[2]]
    cv2.imwrite(filename, cut_img)


def if_joined(a,b):
    #判断两条直线是否有交点
    if a[0] == a[2] and b[1] == b[3]:
        if (a[0] >= b[0] and a[0] <= b[2]) or (a[0] <= b[0] and a[0] >= b[2]):
            if (b[1] >= a[1] and b[1] <= a[3]) or (b[1] <= a[1] and b[1] >= a[3]):
                return True

    if a[1] == a[3] and b[0] == b[2]:

        if (a[1] >= b[1] and a[1] <= b[3]) or (a[1] <= b[1] and a[1] >= b[3]):
            if (b[0] >= a[0] and b[0] <= a[2]) or (b[0] <= a[0] and b[0] >= a[2]):
                return True

    return False

read_image("60.jpg")
