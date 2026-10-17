from flask import Flask, request, Response
import requests
import hmac
import hashlib

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'
TEMPMAIL_API = 'https://api.internal.temp-mail.io/api/v3'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

# ===== Temp-Mail API 代理 =====

@app.route('/api/tempmail/new', methods=['GET', 'POST', 'OPTIONS'])
def tempmail_new():
    if request.method == 'OPTIONS':
        return ('', 204)
    
    try:
        r = requests.post(
            f'{TEMPMAIL_API}/email/new',
            json={"min_name": 10, "max_name": 10},
            timeout=15,
        )
        response = Response(r.content, r.status_code)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return Response(f'{{"error": "{str(e)}"}}', status=500, mimetype='application/json')

@app.route('/api/tempmail/messages/<token>', methods=['GET', 'OPTIONS'])
def tempmail_messages(token):
    if request.method == 'OPTIONS':
        return ('', 204)
    
    try:
        r = requests.get(
            f'{TEMPMAIL_API}/email/{token}/messages',
            timeout=15,
        )
        response = Response(r.content, r.status_code)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return Response(f'{{"error": "{str(e)}"}}', status=500, mimetype='application/json')

# ===== VPN API 代理 =====

@app.route('/api/vpn/', defaults={'target_path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/api/vpn/<path:target_path>', methods=['GET', 'POST', 'OPTIONS'])
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
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return Response(f'{{"error": "{str(e)}"}}', status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run()
