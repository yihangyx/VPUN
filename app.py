#!/usr/bin/env python3
"""
奕涵 - JumperVPN 自动注册器 v3 (Vercel Deploy)
流程: 创建临时邮箱 → 发送验证码 → 用户手动查收邮件 → 输入验证码 → 注册完成
"""

import json, time, hashlib, hmac, uuid, re, random
import urllib.request, urllib.error, ssl
import http.cookiejar
from flask import Flask, render_template_string, request, jsonify

BASE = 'https://api.jumperservice.com/v1/'
SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'
ZEMAIL = 'https://zemail.me'

ctx = ssl.create_default_context()
ctx_nv = ssl._create_unverified_context()

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>奕涵 - JumperVPN注册</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Inter',-apple-system,sans-serif;background:#0F172A;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;color:#F8FAFC}
        .card{background:#1E293B;border-radius:20px;width:100%;max-width:520px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);border:1px solid #334155;overflow:hidden}
        .card-header{background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 100%);padding:32px 24px;text-align:center}
        .card-header h1{font-size:28px;font-weight:700;margin-bottom:8px}
        .card-header p{font-size:14px;opacity:0.9}
        .card-body{padding:24px 28px}
        .step{display:none}
        .step.active{display:block}
        .form-group{margin-bottom:20px}
        .form-label{display:block;margin-bottom:8px;font-weight:500;font-size:14px;color:#E2E8F0}
        .form-input{width:100%;padding:14px 16px;background:#0F172A;border:1px solid #475569;border-radius:12px;font-size:15px;color:#F8FAFC}
        .form-input:focus{outline:none;border-color:#818CF8;box-shadow:0 0 0 3px rgba(79,70,229,0.2)}
        .btn{width:100%;padding:16px;border-radius:12px;font-size:16px;font-weight:600;border:none;cursor:pointer;transition:all .2s}
        .btn-primary{background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 100%);color:white;box-shadow:0 4px 12px rgba(79,70,229,0.3)}
        .btn-primary:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 20px rgba(79,70,229,0.4)}
        .btn:disabled{opacity:0.5;cursor:not-allowed}
        .btn-outline{background:transparent;border:1px solid #4F46E5;color:#818CF8;margin-top:8px}
        .btn-success{background:#10B981;color:white;margin-top:10px}
        .info-card{background:#0F172A;border:1px solid #334155;border-radius:12px;padding:16px;margin:16px 0}
        .info-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1E293B}
        .info-row:last-child{border-bottom:none}
        .info-label{color:#94A3B8;font-size:13px}
        .info-value{color:#F8FAFC;font-family:'Consolas',monospace;font-size:14px;word-break:break-all;text-align:right;max-width:60%}
        .info-value-sm{color:#F8FAFC;font-family:'Consolas',monospace;font-size:11px;word-break:break-all;text-align:right;max-width:65%}
        .alert{background:#1E293B;border:1px solid #f59e0b;border-radius:12px;padding:16px;margin:16px 0;text-align:center;color:#f59e0b;font-size:14px}
        .alert-success{border-color:#10B981;color:#10B981}
        .alert-error{border-color:#EF4444;color:#EF4444}
        .spinner{width:40px;height:40px;border:3px solid #334155;border-top-color:#818CF8;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 16px}
        @keyframes spin{to{transform:rotate(360deg)}}
        .loading{text-align:center;padding:30px 0;color:#94A3B8}
        .mode-group{display:flex;gap:12px}
        .mode-item{flex:1;padding:14px;background:#0F172A;border:1px solid #475569;border-radius:12px;text-align:center;cursor:pointer;font-weight:500;color:#CBD5E1}
        .mode-item:hover{border-color:#64748B}
        .mode-item.active{background:#4F46E5;border-color:#4F46E5;color:white}
        .mode-item input{display:none}
        .step-hint{font-size:12px;color:#64748B;text-align:center;margin-top:10px;line-height:1.6}
        .footer{text-align:center;margin-top:20px;font-size:12px;color:#64748B}
        a{color:#818CF8;text-decoration:none}
    </style>
</head>
<body>
<div class="card">
    <div class="card-header">
        <h1>奕涵</h1>
        <p>JumperVPN 自动注册</p>
    </div>
    <div class="card-body">
        <div class="step active" id="step1">
            <div class="form-group">
                <label class="form-label">📱 设备模式</label>
                <div class="mode-group">
                    <label class="mode-item active"><input type="radio" name="mode" value="ios" checked> iOS</label>
                    <label class="mode-item"><input type="radio" name="mode" value="windows"> Windows</label>
                </div>
            </div>
            <button class="btn btn-primary" onclick="step1Create()">🚀 开始注册</button>
            <div class="step-hint">自动创建临时邮箱并发送 JumperVPN 验证码</div>
        </div>
        <div class="step" id="step2">
            <div class="loading">
                <div class="spinner"></div>
                <p id="step2Msg">正在创建邮箱...</p>
            </div>
        </div>
        <div class="step" id="step3"><div id="step3Content"></div></div>
        <div class="step" id="step4">
            <div class="loading">
                <div class="spinner"></div>
                <p>正在注册账号...</p>
            </div>
        </div>
        <div class="footer">© 2026 奕涵 · 仅供学习使用</div>
    </div>
</div>
<script>
let encState='';
document.querySelectorAll('.mode-item').forEach(i=>i.addEventListener('click',()=>{
    document.querySelectorAll('.mode-item').forEach(x=>x.classList.remove('active'));
    i.classList.add('active');i.querySelector('input').checked=true
}));
function showStep(n){document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));document.getElementById('step'+n).classList.add('active')}
function step1Create(){
    showStep(2);document.getElementById('step2Msg').innerText='正在创建临时邮箱...';
    let mode=document.querySelector('input[name=mode]:checked').value;
    fetch('/api/create_and_send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode})})
    .then(r=>r.json()).then(d=>{
        if(!d.success){showStep(3);document.getElementById('step3Content').innerHTML='<div class="alert alert-error">❌ '+(d.error||'失败')+'</div><button class="btn btn-primary" onclick="showStep(1)">🔄 重试</button>';return}
        encState=d.state;showStep(3);
        document.getElementById('step3Content').innerHTML=
            '<div class="alert alert-success">✅ 验证码已发送到 <b>'+d.email+'</b></div>'+
            '<a href="https://zemail.me/mailbox" target="_blank" style="display:block"><button class="btn btn-primary" type="button">📬 打开收件箱查收验证码</button></a>'+
            '<div class="step-hint">点击上方按钮在新标签打开收件箱<br>找到 JumperVPN 的 6 位数字验证码</div>'+
            '<div class="form-group" style="margin-top:20px"><label class="form-label">🔢 输入验证码</label>'+
            '<input type="text" id="c" class="form-input" style="font-size:24px;text-align:center;letter-spacing:4px" placeholder="000000" maxlength="6" inputmode="numeric" oninput="ci()"></div>'+
            '<button class="btn btn-success" id="br" disabled onclick="reg()">✅ 完成注册</button>'+
            '<button class="btn btn-outline" onclick="showStep(1)">🔄 重新开始</button>'
    }).catch(e=>{showStep(3);document.getElementById('step3Content').innerHTML='<div class="alert alert-error">❌ 网络错误</div><button class="btn btn-primary" onclick="showStep(1)">🔄 重试</button>'})
}
function ci(){let v=document.getElementById('c').value.replace(/\D/g,'').slice(0,6);document.getElementById('c').value=v;document.getElementById('br').disabled=v.length!==6}
function reg(){
    let code=document.getElementById('c').value.replace(/\D/g,'');if(code.length!==6)return;showStep(4);
    fetch('/api/finish_register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({state:encState,code})})
    .then(r=>r.json()).then(d=>{
        showStep(3);
        if(d.success){let r=d.result;
            document.getElementById('step3Content').innerHTML=
                '<div class="alert alert-success">🎉 注册成功！</div>'+
                '<div class="info-card">'+
                '<div class="info-row"><span class="info-label">📧 邮箱</span><span class="info-value">'+r.email+'</span></div>'+
                '<div class="info-row"><span class="info-label">🔐 密码</span><span class="info-value">'+r.pwd+'</span></div>'+
                '<div class="info-row"><span class="info-label">⏱ 时长</span><span class="info-value">'+r.free_time+'</span></div>'+
                '<div class="info-row"><span class="info-label">📅 到期</span><span class="info-value">'+r.end_time+'</span></div>'+
                '<div class="info-row"><span class="info-label">🔑 Token</span><span class="info-value-sm">'+r.token+'</span></div></div>'+
                '<button class="btn btn-primary" onclick="navigator.clipboard.writeText(\''+r.token.replace(/'/g,"\\'")+'\');alert(\'Token 已复制!\')">📋 复制 Token</button>'+
                '<button class="btn btn-outline" onclick="showStep(1)">🔄 再注册一个</button>'
        }else{
            document.getElementById('step3Content').innerHTML='<div class="alert alert-error">❌ '+(d.error||'失败')+'<br><span style="font-size:12px">验证码可能不正确，请重试</span></div><button class="btn btn-primary" onclick="step1Create()">🔄 重试(新邮箱)</button>'
        }
    }).catch(e=>{showStep(3);document.getElementById('step3Content').innerHTML='<div class="alert alert-error">❌ 网络错误</div><button class="btn btn-primary" onclick="showStep(1)">🔄 重试</button>'})
}
</script>
</body>
</html>'''


def ms(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

def api_call(path, method='GET', body=None, token=None, imei=None, mode='ios'):
    url = BASE + path.lstrip('/')
    sign = ms('/v1/' + path.lstrip('/'))
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('app-id', '2')
    req.add_header('version', '1.0.8')
    req.add_header('buildNumber', '3')
    req.add_header('x-sign', sign)
    req.add_header('Accept', '*/*')
    if mode == 'ios':
        req.add_header('os', 'ios')
        req.add_header('Content-Language', 'en-us')
        req.add_header('User-Agent', 'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2')
    else:
        req.add_header('os', 'windows')
        req.add_header('User-Agent', 'JumperVPN/1.0.8')
    if imei:
        req.add_header('imei', imei.strip('{}'))
        req.add_header('device-name', 'DESKTOP-Web')
    if token:
        req.add_header('j-token', token)
    if data:
        req.add_header('Content-Type', 'application/json')
    no_proxy = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(no_proxy, urllib.request.HTTPSHandler(context=ctx))
    try:
        resp = opener.open(req, timeout=15)
        raw = resp.read()
        try: raw = __import__('gzip').decompress(raw)
        except: pass
        return json.loads(raw.decode())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try: raw = __import__('gzip').decompress(raw)
        except: pass
        try: return json.loads(raw.decode())
        except: return {'code': e.code, 'msg': raw.decode('utf-8','replace')[:200]}

def create_zemail_mailbox():
    cj = http.cookiejar.CookieJar()
    zop = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ctx_nv),
        urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request(f'{ZEMAIL}/mailbox',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    resp = zop.open(req, timeout=15)
    html = resp.read().decode('utf-8', 'replace')
    import html as _h
    snap_raw = re.search(r'wire:snapshot="([^"]*)"', html)
    if not snap_raw:
        raise Exception('No snapshot found')
    snapshot = json.loads(_h.unescape(snap_raw.group(1)))
    xsrf = next((urllib.request.unquote(c.value) for c in cj if c.name == 'XSRF-TOKEN'), None)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': xsrf or '',
        'Origin': ZEMAIL,
        'Referer': f'{ZEMAIL}/mailbox'
    }
    payload = {"components": [{"snapshot": json.dumps(snapshot), "updates": {}, "calls": [{"path": "", "method": "createMailbox", "params": []}]}]}
    req2 = urllib.request.Request(f'{ZEMAIL}/livewire/update', data=json.dumps(payload).encode(), method='POST', headers=headers)
    result = json.loads(zop.open(req2, timeout=15).read().decode())
    eff = result['components'][0].get('effects', {}).get('html', '')
    emails = list(set(re.findall(r'([\w.+-]+@[\w.-]+\.\w+)', eff + json.dumps(result, ensure_ascii=False))))
    for e in emails:
        if e.count('@') == 1 and 'zemail' not in e.lower() and 'weml' not in e.lower():
            return e
    raise Exception('Cannot parse email')


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/api/create_and_send', methods=['POST'])
def create_and_send():
    config = request.get_json(silent=True) or {}
    mode = config.get('mode', 'ios')
    pwd_raw = ''.join(random.choices('ABCDEFGHJKLMNPQRSTWXYZabcdefghjkmnpqrstwxyz23456789', k=12))
    try:
        email = create_zemail_mailbox()
        imei = '{' + str(uuid.uuid4()).upper() + '}'
        dr = api_call('device/init', imei=imei, mode=mode)
        if dr.get('code') != 200:
            return jsonify({'success': False, 'error': f'初始化失败: {dr.get("message","?")}'})
        device_token = dr['data']['user_info']['token']
        sr = api_call('user/send_email_code', method='POST',
                      body={'email': email, 'type': 10},
                      token=device_token, imei=imei, mode=mode)
        if sr.get('code') not in (200, 0):
            return jsonify({'success': False, 'error': f'发送验证码失败: {sr.get("message","?")}'})
        import base64
        state = base64.b64encode(json.dumps({
            'email': email, 'pwd_raw': pwd_raw, 'imei': imei,
            'device_token': device_token, 'mode': mode
        }, ensure_ascii=False).encode()).decode()
        return jsonify({'success': True, 'email': email, 'state': state})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:200]})


@app.route('/api/finish_register', methods=['POST'])
def finish_register():
    data = request.get_json(silent=True) or {}
    try:
        import base64
        s = json.loads(base64.b64decode(data.get('state', '')).decode())
    except:
        return jsonify({'success': False, 'error': '状态过期，请重新开始'})
    code = data.get('code', '').strip()
    email, pwd_raw, imei, device_token, mode = s['email'], s['pwd_raw'], s['imei'], s['device_token'], s['mode']
    pwd_md5 = hashlib.md5(pwd_raw.encode()).hexdigest()
    try:
        reg_result = None
        for pw, _ in [(pwd_md5, 'MD5'), (pwd_raw, '明文')]:
            rr = api_call('user/signup', method='POST',
                         body={'email': email, 'password': pw, 'repassword': pw, 'code': code},
                         token=device_token, imei=imei, mode=mode)
            if rr.get('code') in (200, 0):
                reg_result = rr; break
        if not reg_result:
            return jsonify({'success': False, 'error': '验证码不正确或已过期'})
        udata = reg_result.get('data', {}).get('user_info', {})
        free, end = udata.get('free_remaining_time', 0), udata.get('free_end_time', '')
        h, m = free // 3600, (free % 3600) // 60
        final_token = device_token
        for pw in [pwd_md5, pwd_raw]:
            lr = api_call('user/signin', method='POST',
                         body={'email': email, 'password': pw},
                         token=device_token, imei=imei, mode=mode)
            if lr.get('code') in (200, 0):
                t = lr.get('data', {}).get('user_info', {}).get('token', '')
                if t: final_token = t; break
        return jsonify({'success': True, 'result': {
            'email': email, 'pwd': pwd_raw,
            'free_time': f'{h}小时{m}分', 'end_time': end, 'token': final_token
        }})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:200]})


if __name__ == '__main__':
    print('奕涵 v3 — http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
