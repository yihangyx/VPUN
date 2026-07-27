#!/usr/bin/env python3
"""奕涵 - JumperVPN 注册 v6: iframe 代理收件箱"""

import json, hashlib, hmac, uuid, re, random, base64, traceback
import urllib.request, urllib.error, ssl
import http.cookiejar
from flask import Flask, request, jsonify

BASE = 'https://api.jumperservice.com/v1/'
SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'
ZEMAIL = 'https://zemail.me'
app = Flask(__name__)

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>奕涵</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,sans-serif;background:#0F172A;min-height:100vh;padding:12px;color:#F8FAFC}
.card{background:#1E293B;border-radius:20px;width:100%;max-width:520px;margin:0 auto;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);border:1px solid #334155;overflow:hidden}
.card-header{background:linear-gradient(135deg,#4F46E5,#7C3AED);padding:24px;text-align:center}
.card-header h1{font-size:24px;font-weight:700}
.card-header p{font-size:12px;opacity:0.9}
.card-body{padding:20px 24px}
.form-label{display:block;margin-bottom:6px;font-weight:500;font-size:13px;color:#E2E8F0}
.btn{width:100%;padding:14px;border-radius:12px;font-size:15px;font-weight:600;border:none;cursor:pointer;transition:all .2s;display:block;text-align:center}
.btn-primary{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:white}
.btn-primary:hover:not(:disabled){transform:translateY(-2px)}
.btn-primary:disabled{opacity:0.4;cursor:not-allowed}
.btn-outline{background:transparent;border:1px solid #4F46E5;color:#818CF8;margin-top:8px}
.btn-success{background:#10B981;color:white;margin-top:10px}
.info-card{background:#0F172A;border:1px solid #334155;border-radius:12px;padding:14px;margin:14px 0}
.info-row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #1E293B}
.info-row:last-child{border-bottom:none}
.info-label{color:#94A3B8;font-size:12px}
.info-value{color:#F8FAFC;font-family:monospace;font-size:12px;word-break:break-all;text-align:right;max-width:60%}
.alert{border-radius:12px;padding:12px 16px;margin:10px 0;text-align:center;font-size:13px}
.alert-success{background:rgba(16,185,129,0.1);border:1px solid #10B981;color:#10B981}
.alert-error{background:rgba(239,68,68,0.1);border:1px solid #EF4444;color:#EF4444}
.spinner{width:32px;height:32px;border:3px solid #334155;border-top-color:#818CF8;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 12px}
@keyframes spin{to{transform:rotate(360deg)}}
.loading{padding:20px 0;text-align:center;color:#94A3B8}
.mode-group{display:flex;gap:10px;margin-bottom:14px}
.mode-btn{flex:1;padding:10px;background:#0F172A;border:2px solid #475569;border-radius:10px;text-align:center;cursor:pointer;font-weight:500;color:#CBD5E1;font-size:13px}
.mode-btn.active{background:#4F46E5;border-color:#6366F1;color:white}
.hint{font-size:11px;color:#64748B;text-align:center;margin-top:8px;line-height:1.4}
.footer{text-align:center;margin-top:12px;font-size:10px;color:#475569}
.hidden{display:none!important}
.inbox-frame{width:100%;height:420px;border:1px solid #334155;border-radius:12px;background:#fff}
</style>
</head>
<body>
<div class="card">
<div class="card-header"><h1>奕涵</h1><p>JumperVPN 自动注册</p></div>
<div class="card-body">
<div id="page1"><div class="form-label" style="margin-bottom:6px">📱 设备模式</div><div class="mode-group">
<div class="mode-btn active" data-mode="ios">iOS</div>
<div class="mode-btn" data-mode="windows">Windows</div></div>
<button class="btn btn-primary" onclick="doStart()">🚀 开始注册</button>
<div class="hint">自动创建临时邮箱，下方显示收件箱</div></div>
<div id="page2" class="hidden"><div class="loading"><div class="spinner"></div><p id="loadMsg">正在创建...</p></div></div>
<div id="page3" class="hidden"><div id="page3body"></div></div>
<div class="footer">© 2026 奕涵</div></div></div>
<script>
var gM='ios',gS='',gE='',gK='';
document.querySelectorAll('.mode-btn').forEach(function(b){b.onclick=function(){
document.querySelectorAll('.mode-btn').forEach(function(x){x.classList.remove('active')});b.classList.add('active');gM=b.getAttribute('data-mode');}});
function show(id){document.getElementById('page1').classList.add('hidden');document.getElementById('page2').classList.add('hidden');document.getElementById('page3').classList.add('hidden');document.getElementById(id).classList.remove('hidden');}
function doStart(){show('page2');document.getElementById('loadMsg').innerText='正在创建邮箱...';
fetch('/api/create_and_send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:gM})})
.then(function(r){return r.json()}).then(function(d){if(d.success){gS=d.state;gE=d.email;gK=d.key;showStep3()}else{showErr('创建失败: '+(d.error||'?'))}}).catch(function(e){showErr('网络错误: '+e.message)})}
function showStep3(){show('page3');
document.getElementById('page3body').innerHTML=
'<div class="alert alert-success">✅ 验证码已发送到 <b>'+gE+'</b></div>'+
'<div class="form-label" style="margin-bottom:8px">📬 收件箱（你的临时邮箱）</div>'+
'<iframe class="inbox-frame" id="ifr" src="/proxy/inbox?key='+encodeURIComponent(gK)+'" sandbox="allow-scripts allow-same-origin"></iframe>'+
'<div class="form-group" style="margin-top:14px"><div class="form-label" style="font-size:11px">💡 在收件箱中查看 JumperVPN 验证码邮件</div></div>'+
'<a href="https://zemail.me/mailbox" target="_blank" style="display:block"><button class="btn btn-outline" type="button">🔗 如果没显示，点击打开外部收件箱</button></a>'+
'<button class="btn btn-outline" onclick="location.reload()" style="margin-top:8px">🔄 重新开始</button>';
}
function showErr(m){show('page3');document.getElementById('page3body').innerHTML='<div class="alert alert-error">❌ '+m+'</div><button class="btn btn-primary" onclick="doStart()">🔄 重试</button>'}
</script>
</body>
</html>'''


def ms(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

def api_call(path, method='GET', body=None, token=None, imei=None, mode='ios'):
    ctx = ssl.create_default_context()
    url = BASE + path.lstrip('/')
    sign = ms('/v1/' + path.lstrip('/'))
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('app-id', '2'); req.add_header('version', '1.0.8'); req.add_header('buildNumber', '3')
    req.add_header('x-sign', sign); req.add_header('Accept', '*/*')
    if mode == 'ios':
        req.add_header('os', 'ios'); req.add_header('Content-Language', 'en-us')
        req.add_header('User-Agent', 'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2')
    else:
        req.add_header('os', 'windows'); req.add_header('User-Agent', 'JumperVPN/1.0.8')
    if imei:
        req.add_header('imei', imei.strip('{}')); req.add_header('device-name', 'DESKTOP-Web')
    if token: req.add_header('j-token', token)
    if data: req.add_header('Content-Type', 'application/json')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))
    try:
        resp = opener.open(req, timeout=25)
        raw = resp.read()
        try: raw = __import__('gzip').decompress(raw)
        except: pass
        return json.loads(raw.decode())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: raw = __import__('gzip').decompress(raw)
        except: pass
        try: return json.loads(raw.decode())
        except: return {'code': e.code, 'msg': raw.decode('utf-8','replace')[:300]}

# Store cookies by key (for proxy)
import random as _random, string as _string
cookie_store = {}

def _make_key():
    return ''.join(_random.choices(_string.ascii_letters+_string.digits, k=24))

def create_zemail():
    ctx = ssl._create_unverified_context()
    cj = http.cookiejar.CookieJar()
    zop = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cj))

    r = urllib.request.Request(f'{ZEMAIL}/mailbox',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    html = zop.open(r, timeout=25).read().decode('utf-8', 'replace')

    import html as _h
    snap_raw = re.search(r'wire:snapshot="([^"]*)"', html)
    if not snap_raw: raise Exception('No snapshot')
    snapshot = json.loads(_h.unescape(snap_raw.group(1)))
    xsrf = next((urllib.request.unquote(c.value) for c in cj if c.name == 'XSRF-TOKEN'), '')

    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest', 'X-XSRF-TOKEN': xsrf,
        'Origin': ZEMAIL, 'Referer': f'{ZEMAIL}/mailbox'
    }
    payload = {"components": [{"snapshot": json.dumps(snapshot), "updates": {}, "calls": [{"path": "", "method": "createMailbox", "params": []}]}]}
    req2 = urllib.request.Request(f'{ZEMAIL}/livewire/update',
        data=json.dumps(payload).encode(), method='POST', headers=headers)
    result = json.loads(zop.open(req2, timeout=25).read().decode())
    eff = result['components'][0].get('effects', {}).get('html', '')
    combined = eff + json.dumps(result, ensure_ascii=False)
    emails = list(set(re.findall(r'([\w.+-]+@[\w.-]+\.\w+)', combined)))
    email = next((e for e in emails if e.count('@') == 1 and 'zemail' not in e.lower()), None)
    if not email: raise Exception('Cannot parse email')
    return email, cj


@app.route('/')
def index():
    return HTML

@app.route('/api/create_and_send', methods=['POST'])
def api_create():
    try:
        data = request.get_json(silent=True) or {}
        mode = data.get('mode', 'ios')
        chars = 'ABCDEFGHJKLMNPQRSTWXYZabcdefghjkmnpqrstwxyz23456789'
        pwd_raw = ''.join(__import__('random').choices(chars, k=12))

        email, cj = create_zemail()
        key = _make_key()
        cookie_store[key] = cj

        imei = '{' + str(uuid.uuid4()).upper() + '}'
        dr = api_call('device/init', imei=imei, mode=mode)
        if dr.get('code') != 200:
            return jsonify({'success': False, 'error': '初始化失败: ' + str(dr.get('message', dr.get('msg', '?')))})
        dt = dr['data']['user_info']['token']
        sr = api_call('user/send_email_code', method='POST',
                      body={'email': email, 'type': 10}, token=dt, imei=imei, mode=mode)
        if sr.get('code') not in (200, 0):
            return jsonify({'success': False, 'error': '发送验证码失败: ' + str(sr.get('message', sr.get('msg', '?')))})

        state = base64.b64encode(json.dumps({
            'e': email, 'p': pwd_raw, 'i': imei, 't': dt, 'm': mode
        }, ensure_ascii=False).encode()).decode()
        return jsonify({'success': True, 'email': email, 'state': state, 'key': key})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:300]})


@app.route('/proxy/inbox')
def proxy_inbox():
    """代理 zemail 收件箱页面"""
    key = request.args.get('key', '')
    cj = cookie_store.get(key)
    if not cj:
        return '<p style="padding:20px;color:red">Session expired. Please restart.</p>', 410

    ctx = ssl._create_unverified_context()
    zop = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cj))

    try:
        req = urllib.request.Request(f'{ZEMAIL}/mailbox',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        resp = zop.open(req, timeout=20)
        html = resp.read().decode('utf-8', 'replace')

        # Rewrite all zemail.me URLs to go through proxy
        html = html.replace('https://zemail.me', '')
        html = html.replace('http://zemail.me', '')
        html = html.replace('//zemail.me', '')
        html = html.replace('src="/', f'src="{ZEMAIL}/')
        html = html.replace('href="/', f'href="{ZEMAIL}/')

        # Also proxy Livewire requests to avoid CORS
        html = html.replace('"/livewire/', f'"{ZEMAIL}/livewire/')
        html = html.replace("'/livewire/", f"'{ZEMAIL}/livewire/")

        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return f'<p style="padding:20px;color:red">Error: {e}</p>', 500


@app.route('/api/finish_register', methods=['POST'])
def api_finish():
    try:
        data = request.get_json(silent=True) or {}
        s = json.loads(base64.b64decode(data.get('state', '')).decode())
    except:
        return jsonify({'success': False, 'error': '状态过期'})
    code = data.get('code', '').strip()
    e, p, i, t, m = s['e'], s['p'], s['i'], s['t'], s['m']
    p_md5 = hashlib.md5(p.encode()).hexdigest()
    try:
        rr = None
        for pw in [p_md5, p]:
            rr = api_call('user/signup', method='POST',
                         body={'email': e, 'password': pw, 'repassword': pw, 'code': code},
                         token=t, imei=i, mode=m)
            if rr.get('code') in (200, 0): break
        if not (rr and rr.get('code') in (200, 0)):
            return jsonify({'success': False, 'error': '验证码不正确'})
        ud = rr.get('data', {}).get('user_info', {})
        free, end_time = ud.get('free_remaining_time', 0), ud.get('free_end_time', '')
        h, mn = free // 3600, (free % 3600) // 60
        ft = t
        for pw in [p_md5, p]:
            lr = api_call('user/signin', method='POST',
                         body={'email': e, 'password': pw}, token=t, imei=i, mode=m)
            if lr.get('code') in (200, 0):
                tk = lr.get('data', {}).get('user_info', {}).get('token', '')
                if tk: ft = tk; break
        return jsonify({'success': True, 'result': {
            'email': e, 'pwd': p, 'free_time': f'{h}小时{mn}分', 'end_time': end_time, 'token': ft
        }})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(ex)[:300]})


if __name__ == '__main__':
    print('http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
