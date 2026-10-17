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

def create_shop_email():
    """循环生成直到找到beeinbox.shop后缀的邮箱"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for attempt in range(10):
        s = requests.Session()
        s.get('https://beeinbox.com/', headers=headers)
        r = s.get('https://beeinbox.com/', headers=headers)
        
        const_match = re.search(r"const email = '([^']+)'", r.text)
        if const_match:
            email = const_match.group(1)
            if email.endswith('beeinbox.shop'):
                return s, email
    
    return None, None

@app.route('/api/complete-register', methods=['GET'])
def complete_register():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Step 1: 创建beeinbox.shop邮箱
    results.append("=== Step 1: 创建邮箱 ===")
    s, email = create_shop_email()
    if not email:
        results.append("❌ 创建邮箱失败")
        return Response("\n".join(results), mimetype='text/plain')
    results.append(f"✅ 邮箱: {email}")
    
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
    results.append("✅ 成功")
    
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
    results.append(f"✅ 结果: {r.json()}")
    
    # Step 4: 等待验证码
    results.append("\n=== Step 4: 等待验证码 ===")
    code = None
    
    for i in range(20):
        time.sleep(3)
        r = s.get('https://beeinbox.com/', headers=headers)
        
        # 找所有可能的验证码
        # 先找邮件正文里的数字
        # 排除常见的非验证码数字
        text = r.text
        
        # 找所有iframe的src
        iframe_srcs = re.findall(r'<iframe[^>]*src="([^"]*)"', text)
        
        # 找所有4-6位数字
        numbers = re.findall(r'\b(\d{4,6})\b', text)
        
        for num in numbers:
            # 过滤掉年份、版本号等
            if num in ['2024', '2025', '2026', '2027', '1000', '2000', '3000', '5000', '10000']:
                continue
            # 验证码通常是4-6位，而且不会是整千整万
            if len(num) >= 4:
                code = num
                results.append(f"  尝试 {i+1}: 找到验证码 {num}")
                break
        
        if code:
            break
        if i % 5 == 4:
            results.append(f"  已等待 {(i+1)*3} 秒...")
    
    if not code:
        results.append("❌ 没找到验证码")
        return Response("\n".join(results), mimetype='text/plain')
    
    # Step 5: 注册
    results.append("\n=== Step 5: 完成注册 ===")
    pwd_raw = 'Test123456'
    pwd_md5 = hashlib.md5(pwd_raw.encode()).hexdigest()
    
    vpn_headers['x-sign'] = make_sign('user/signup')
    
    r = requests.post(
        'https://api.jumperservice.com/v1/user/signup',
        headers=vpn_headers,
        json={
            'email': email,
            'password': pwd_md5,
            'repassword': pwd_md5,
            'code': code,
        },
        timeout=10,
    )
    
    result = r.json()
    results.append(f"注册结果: {result}")
    
    if result.get('code') == 200:
        results.append("\n🎉 注册成功!")
        results.append(f"邮箱: {email}")
        results.append(f"密码: {pwd_raw}")
    else:
        results.append(f"\n❌ 注册失败: {result.get('message')}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
