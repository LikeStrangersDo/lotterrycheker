import requests
import hashlib
import base64
import json
import re

# 百度AI开放平台提供的API接口信息
APP_ID = '******'
API_KEY = '*********'
SECRET_KEY = '*****************'
OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'


# 图片识别函数，接收一张图片路径作为参数，并返回图片中的文字识别结果
def recognize_text(image_path):
    # 读取图片文件
    with open(image_path, 'rb') as f:
        image_data = f.read()
    # 对图片进行base64编码
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    # 计算图片MD5值
    image_md5 = hashlib.md5(image_data).hexdigest()
    # 构造API请求数据
    data = {
        'image': image_base64,
        'language_type': 'CHN_ENG',
        'detect_direction': 'true',
        'detect_language': 'true',
        'probability': 'false',
        'image_md5': image_md5,
        'id_card_side': 'front'
    }
    # 构造API请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # 发送API请求
    response = requests.post(OCR_URL, headers=headers, data=data, params={'access_token': get_access_token()})
    # 解析API响应结果
    result = json.loads(response.text)
    if result.get('words_result'):
        # 获取识别结果中的文字内容
        text = ''.join([item.get('words', '') for item in result['words_result']])
        print(text)

        # 使用正则表达式提取期号
        pattern1 = r'期号：(\d+)(?:开奖期：(\d+)-(\d+))?'
        match1 = re.search(pattern1, text)
        if match1:
            issue = match1.group(1)  # 期号
            # 输出提取结果
            print('期号：', issue)
        else:
            print('未找到相关信息')

        # 使用正则表达式提取彩票号码和倍数
        pattern2 = r'①(\d+)\-(\d+)\[(\d+)倍\]' \
                   r'|②(\d+)\-(\d+)\[(\d+)倍\]' \
                   r'|③(\d+)\-(\d+)\[(\d+)倍\]' \
                   r'|④(\d+)\-(\d+)\[(\d+)倍\]' \
                   r'|⑤(\d+)\-(\d+)\[(\d+)倍\]'
        match2 = re.findall(pattern2, text)
        print(match2)
        match2 = [tuple(filter(None, t)) for t in match2]
        print(match2)
        numbers = []  # 彩票号码列表    这里缺少蓝球号码  后期补充
        multiple = []  # 倍数列表
        for x in range(len(match2)):
            if match2[x]:
                numbers.append(match2[x][0])
                multiple.append(match2[x][2])
        print(numbers, multiple)
        # 将读取彩票获取的彩票号码以字典的形式记录红篮球同时存入列表内
        lottery_numbers = []
        for k in range(len(numbers)):
            red_balls = [numbers[k][i:i + 2] for i in range(0, 13, 2)][:-1]
            blue_ball = match2[k][1]
            lottery_numbers_n = {
                'red_balls': red_balls,
                'blue_ball': blue_ball,
                'multiple': multiple[k]
            }
            lottery_numbers.append(lottery_numbers_n)

        return issue, lottery_numbers

    else:
        return None


def get_lottery_numbers(issue):
    """通过期号及指定的url获取中奖号码"""
    # 请求头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.302'
                      '9.110 Safari/537.3'}

    req_issue = issue[2:7]
    url = f"https://kaijiang.500.com/shtml/ssq/{req_issue}.shtml"
    # 发送请求，获取网页内容
    response = requests.get(url)
    html_doc = response.content.decode(response.encoding)
    # 使用正则表达式解析开奖号码
    pattern = re.compile('<li class="ball_red">(\d+)</li>')
    red_balls = pattern.findall(html_doc)
    blue_ball = re.search('<li class="ball_blue">(\d+)</li>', html_doc).group(1)
    # 输出开奖号码信息
    print('开奖红球：', red_balls)
    print('开奖蓝球：', blue_ball)
    return red_balls, blue_ball


# 判断彩票是否中奖
def check_lottery_numbers(lottery_numbers, winning_numbers):
    # 判断红球中奖个数
    red_hits = 0
    for number in lottery_numbers['red_balls']:
        if number in winning_numbers['red_balls']:
            red_hits += 1
    # 判断蓝球是否中奖
    blue_hit = lottery_numbers['blue_ball'] == winning_numbers['blue_ball']
    # 判断中奖等级
    if red_hits == 6 and blue_hit:
        return '一等奖'
    elif red_hits == 6 and not blue_hit:
        return '二等奖'
    elif red_hits == 5 and blue_hit:
        return '三等奖'
    elif red_hits == 5 and not blue_hit:
        return '四等奖'
    elif red_hits == 4 and blue_hit:
        return '五等奖'
    elif red_hits == 4 and not blue_hit:
        return '六等奖'
    elif red_hits == 3 and blue_hit:
        return '七等奖'
    else:
        return '未中奖'


# 获取百度AI开放平台提供的access_token
def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}' \
          f'&client_secret={SECRET_KEY}'
    response = requests.get(url)
    result = json.loads(response.text)
    return result.get('access_token', '')



