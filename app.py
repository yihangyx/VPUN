from flask import Flask, Response
import requests
import hmac
import hashlib
import re

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

@app.route('/api/test-chinasteel', methods=['GET'])
def test_chinasteel():
    results = []
    
    # Step 1: 通过beeinbox.com创建邮箱
    s = requests.Session()
    s.get('https://beeinbox.com/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    r = s.get('https://beeinbox.com/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    
    const_match = re.search(r"const email = '([^']+)'", r.text)
    email = const_match.group(1)
    results.append(f"生成邮箱: {email}")
    
    # Step 2: device/init
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
    results.append(f"device/init: 成功")
    
    # Step 3: 发送验证码
    vpn_headers['j-token'] = device_token
    vpn_headers['x-sign'] = make_sign('user/send_email_code')
    vpn_headers['Content-Type'] = 'application/json'
    
    r = requests.post(
        'https://api.jumperservice.com/v1/user/send_email_code',
        headers=vpn_headers,
        json={'email': email, 'type': 10},
        timeout=10,
    )
    results.append(f"发送验证码结果: {r.json()}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
