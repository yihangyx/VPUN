from flask import Flask, Response
import requests
import hmac
import hashlib
import re

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

@app.route('/api/test-visitlondon', methods=['GET'])
def test_visitlondon():
    results = []
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 多生成几次邮箱，看看有哪些后缀
    results.append("=== 生成多个邮箱测试 ===")
    for i in range(3):
        s.get('https://beeinbox.com/', headers=headers)
        r = s.get('https://beeinbox.com/', headers=headers)
        const_match = re.search(r"const email = '([^']+)'", r.text)
        if const_match:
            email = const_match.group(1)
            results.append(f"邮箱{i+1}: {email}")
    
    # 用最后一个邮箱测试发送验证码
    email = const_match.group(1)
    results.append(f"\n=== 测试发送验证码到 {email} ===")
    
    # device/init
    imei = '{CDF214C1-2D62-4D89-A221-DEA05DF2A8BA}'
    vpn_headers = {
        'app-id': '2',
        'version': '1.0.8',
        'buildNumber': '3',
        'os': 'ios',
        'x-sign': make_sign('device/init'),
        'imei': imei,
        'device-name': 'iPhone 15 Pro',
    }
    r = requests.get('https://api.jumperservice.com/v1/device/init', headers=vpn_headers, timeout=10)
    device_token = r.json()['data']['user_info']['token']
    
    # 发送验证码
    vpn_headers['j-token'] = device_token
    vpn_headers['x-sign'] = make_sign('user/send_email_code')
    vpn_headers['Content-Type'] = 'application/json'
    
    r = requests.post(
        'https://api.jumperservice.com/v1/user/send_email_code',
        headers=vpn_headers,
        json={'email': email, 'type': 10},
        timeout=10,
    )
    results.append(f"结果: {r.json()}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
