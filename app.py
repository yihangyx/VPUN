from flask import Flask, Response
import requests
import hmac
import hashlib
import re
import time

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

@app.route('/api/full-test', methods=['GET'])
def full_test():
    results = []
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Step 1: 创建邮箱
    results.append("=== Step 1: 创建邮箱 ===")
    s.get('https://beeinbox.com/', headers=headers)
    r = s.get('https://beeinbox.com/', headers=headers)
    
    const_match = re.search(r"const email = '([^']+)'", r.text)
    email = const_match.group(1)
    results.append(f"邮箱: {email}")
    
    # Step 2: device/init
    results.append("\n=== Step 2: device/init ===")
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
    results.append("成功")
    
    # Step 3: 发送验证码
    results.append("\n=== Step 3: 发送验证码 ===")
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
    
    # Step 4: 等待并检查邮件
    results.append("\n=== Step 4: 等待验证码 ===")
    code = None
    for i in range(15):
        time.sleep(3)
        r = s.get('https://beeinbox.com/', headers=headers)
        
        # 找iframe里的验证码
        # 先找所有iframe
        iframes = re.findall(r'<iframe[^>]*src="([^"]*)"', r.text)
        results.append(f"  检查{i+1}: 找到{len(iframes)}个iframe")
        
        # 找所有数字
        codes = re.findall(r'\b(\d{4,6})\b', r.text)
        if codes:
            # 过滤掉明显不是验证码的
            for c in codes:
                if len(c) in [4, 5, 6] and c not in ['2025', '2026']:
                    results.append(f"  可能的验证码: {c}")
                    code = c
                    break
        
        if code:
            break
    
    if code:
        results.append(f"\n✅ 找到验证码: {code}")
    else:
        results.append("\n❌ 没找到验证码")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
