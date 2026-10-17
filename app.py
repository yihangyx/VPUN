from flask import Flask, request, Response
import requests
import hmac
import hashlib

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

@app.route('/api/beeinbox/<path:target_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_beeinbox(target_path):
    if request.method == 'OPTIONS':
        return ('', 204)
    
    query_string = request.query_string.decode()
    url = f'https://beeinbox.com/{target_path}'
    if query_string:
        url += '?' + query_string
    
    resp = requests.request(
        method=request.method,
        url=url,
        headers={
            'User-Agent': request.headers.get('User-Agent', ''),
            'Accept': request.headers.get('Accept', '*/*'),
        },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'host']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    response = Response(resp.content, resp.status_code, headers)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/vpn/<path:target_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_vpn(target_path):
    if request.method == 'OPTIONS':
        return ('', 204)
    
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
    if request.headers.get('device-name'):
        headers['device-name'] = request.headers.get('device-name')
    
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
    )
    
    response = Response(resp.content, resp.status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
