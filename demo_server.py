from flask import Flask, request, jsonify
import requests
import json
import time
from datetime import datetime
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed
from sign import get_sign
import random
import math

app = Flask(__name__)
CORS(app)  # 允许所有源跨域访问

def get_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        'terminal': '0',
        'UNI-Request-Source': '4',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.53(0x1800352e) NetType/WIFI Language/zh_CN',
        'content-type': 'application/json'
    }
    
def fetch_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def get_account_info(token):
    try:
        headers = get_headers(token)
        with ThreadPoolExecutor() as executor:
            futures = {
                'response1': executor.submit(fetch_data, "https://api.hikiot.com/api-saas/v1/account/detail", headers),
                'response2': executor.submit(fetch_data, f"https://api.hikiot.com/api-attendance/v1/statistics/individual/daily?month={datetime.now().strftime('%Y-%m')}&personNo=&ID=myStatic", headers),
                'response3': executor.submit(fetch_data, "https://api.hikiot.com/api-attendance/mobile-clock/v1/individual-clock-rules", headers),
            }

            response1 = futures['response1'].result()
            response2 = futures['response2'].result()
            response3 = futures['response3'].result()

            if not response1 or not response2 or not response3:
                return False

            account_info = {
                'nick_name': response1['data'].get('nickName', '未设置昵称'),
                'phone': response1['data'].get('phone', '未绑定手机号'),
                'team_name': response2['data'].get('orgName', '无团队身份'),
                'name': response2['data'].get('personName', '未设置姓名'),
                'rule': response3['data'].get('shiftDetail', '未设置打卡规则'),
                'message': 'success'
            }

            return account_info

    except Exception as e:
        print(f"发生错误: {e}")
        return False

@app.route('/api/test_token', methods=['POST'])
def test_token():
    data = request.get_json()
    token = data.get('token')
    if len(token) != 36:
        return jsonify({'message': 'token格式错误'})
    account_info = get_account_info(token)
    if account_info:
        return jsonify(account_info)
    else:
        return jsonify({'message': 'token无效 请重新获取'})

@app.route('/api/get_today_status', methods=['POST'])
def get_today_status():
    data = request.get_json()
    token = data.get('token')
    if len(token) != 36:
        return jsonify({'message': 'token格式错误'})
    # 获取今日打卡状态
    try:
        response = requests.request("GET", "https://api.hikiot.com/api-attendance/mobile-clock/v1/require-commuting", headers=get_headers(token)).json()
        if response['code'] == 0:
            return response['data']
        else:
            return jsonify({'message': '获取打卡状态失败'})
    except Exception as e:
        return jsonify({'message': 'token无效 请重新获取'})

def add_random_offset(latitude, longitude, max_distance=50):
    # 纬度和经度单位转换
    lat_offset = max_distance / 111000
    lng_offset = max_distance / (111000 * abs(math.cos(math.radians(latitude))))
    
    # 生成随机偏移
    new_latitude = latitude + random.uniform(-lat_offset, lat_offset)
    new_longitude = longitude + random.uniform(-lng_offset, lng_offset)
    
    return new_latitude, new_longitude
@app.route('/api/daka', methods=['POST'])
def daka():
    data = request.get_json()
    token = data.get('token')
    if len(token) != 36:
        return jsonify({'message': 'token格式错误'})
    # 打卡
    try:
        headers = get_headers(token)
        latitude = xxx
        longitude = xxx
        new_latitude, new_longitude = add_random_offset(latitude, longitude)
        data = {
            "deviceSerial": "",
            "longitude": new_longitude,
            "latitude": new_latitude,
            "clockSite": "xxx",
            "address": "xxx",
            "deviceName": "xxx",
            "wifiName": "xxx",
            "wifiMac": "xxx"
        }
        headers.update({
            "sign": get_sign(data),
            "timestamp": str(int(time.time() * 1000)),
            "authPerm": "PUNCHCLOCKFUN",
            "appNo": "__UNI__89A1A02",
        })
        response = requests.post("https://api.hikiot.com/api-attendance/mobile-clock/v1/normal", headers=headers, json=data).json()
        print(response)
        if response['code'] == 0:
            return jsonify({'message': '打卡成功'})
        else:
            return jsonify({'message': '打卡失败'})
    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({'message': 'token无效 请重新获取'})

if __name__ == '__main__':
    app.run(debug=True, port=6010, host='127.0.0.1')
