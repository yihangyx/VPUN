from flask import Flask, request, Response
import requests
import hmac
import hashlib

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'
TEMPPIN_API = 'https://temppin.com'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ===== Temppin API 代理 =====

@app.route('/api/temppin/create', methods=['GET', 'POST', 'OPTIONS'])
def temppin_create():
    if request.method == 'OPTIONS':
        return add_cors(Response('', 204))
    
    try:
        r = requests.post(
            f'{TEMPPIN_API}/api/tempmail/create',
            json={"expiryHours": 3},
            headers={
                'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
                'Accept': 'application/json',
                'Referer': 'https://temppin.com/zh/',
            },
            timeout=15,
        )
        
        response = Response(r.content, r.status_code)
        response.headers['Content-Type'] = 'application/json'
        return add_cors(response)
    except Exception as e:
        return add_cors(Response(
            f'{{"error": "{str(e)}"}}',
            status=500,
            mimetype='application/json'
        ))

@app.route('/api/temppin/inbox', methods=['GET', 'OPTIONS'])
def temppin_inbox():
    if request.method == 'OPTIONS':
        return add_cors(Response('', 204))
    
    token = request.args.get('token', '')
    
    try:
        r = requests.get(
            f'{TEMPPIN_API}/api/tempmail/inbox',
            params={'token': token},
            headers={
                'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
                'Accept': 'application/json',
                'Referer': 'https://temppin.com/zh/',
            },
            timeout=15,
        )
        
        response = Response(r.content, r.status_code)
        response.headers['Content-Type'] = 'application/json'
        return add_cors(response)
    except Exception as e:
        return add_cors(Response(
            f'{{"error": "{str(e)}"}}',
            status=500,
            mimetype='application/json'
        ))

@app.route('/api/temppin/email/<mail_id>', methods=['GET', 'OPTIONS'])
def temppin_email(mail_id):
    if request.method == 'OPTIONS':
        return add_cors(Response('', 204))
    
    token = request.args.get('token', '')
    
    try:
        r = requests.get(
            f'{TEMPPIN_API}/api/tempmail/email/{mail_id}',
            params={'token': token},
            headers={
                'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
                'Accept': 'application/json',
                'Referer': 'https://temppin.com/zh/',
            },
            timeout=15,
        )
        
        response = Response(r.content, r.status_code)
        response.headers['Content-Type'] = 'application/json'
        return add_cors(response)
    except Exception as e:
        return add_cors(Response(
            f'{{"error": "{str(e)}"}}',
            status=500,
            mimetype='application/json'
        ))

# ===== VPN API 代理 =====

@app.route('/api/vpn/', defaults={'target_path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/api/vpn/<path:target_path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy_vpn(target_path):
    if request.method == 'OPTIONS':
        return add_cors(Response('', 204))
    
    url = f'https://api.jumperservice.com/v1/{target_path}'
    
    headers = {
        'app-id': '2',
        'version': '1.0.8',
        'buildNumber': '3',
        'os': 'ios',
        'Content-Language': 'en-us',
        'User-Agent': 'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2',
        'Accept-Language': 'zh-Hans-CN;q=1.0',
        'x-sign': make_sign(target_path),
        'Content-Type': 'application/json',
    }
    
    if request.headers.get('j-token'):
        headers['j-token'] = request.headers.get('j-token')
    if request.headers.get('imei'):
        headers['imei'] = request.headers.get('imei')
    headers['device-name'] = 'iPhone 15 Pro'
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            timeout=15,
        )
        
        response = Response(resp.content, resp.status_code)
        response.headers['Content-Type'] = 'application/json'
        return add_cors(response)
    except Exception as e:
        return add_cors(Response(
            f'{{"error": "{str(e)}"}}',
            status=500,
            mimetype='application/json'
        ))

if __name__ == '__main__':
    app.run()
