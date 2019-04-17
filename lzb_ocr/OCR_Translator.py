import base64
import urllib

import requests

API_Key = '2gQsB6LrdKc89k9qfA3tut4N'
Secret_Key = 'rWRo7jSQOlYc5fd9PCmsTVo5sQzTiy18'


def get_access_token(API_Key, Secret_Key):
    res = requests.get(url='https://aip.baidubce.com/oauth/2.0/token',
                       params={'grant_type': 'client_credentials',
                               'client_id': API_Key,
                               'client_secret': Secret_Key})
    access_token = res.json()['access_token']
    return access_token


def accurate_ocr(access_token, img_file):
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
    f = open(img_file, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    params = urllib.parse.urlencode(params)
    response = requests.post(url, data=params)
    return response.text

def get_ocr_words(img_file):
    access_token = get_access_token(API_Key, Secret_Key)
    print('access token = ',access_token)
    accurate_ocr(access_token,img_file)


get_ocr_words('1.png')


