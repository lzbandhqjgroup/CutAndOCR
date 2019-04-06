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


def invoke_ocr(access_token,):

    return None


r = get_access_token(API_Key, Secret_Key)
print(r)
