#!/usr/bin/env python3
"""奕涵 - JumperVPN 自动注册 v4"""

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
body{font-family:-apple-system,sans-serif;background:#0F172A;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;color:#F8FAFC}
.card{background:#1E293B;border-radius:20px;width:100%;max-width:500px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);border:1px solid #334155;overflow:hidden}
.card-header{background:linear-gradient(135deg,#4F46E5,#7C3AED);padding:28px 24px;text-align:center}
.card-header h1{font-size:26px;font-weight:700;margin-bottom:6px}
.card-header p{font-size:13px;opacity:0.9}
.card-body{padding:24px 28px}
.form-group{margin-bottom:18px}
.form-label{display:block;margin-bottom:8px;font-weight:500;font-size:14px;color:#E2E8F0}
.form-input{width:100%;padding:14px 16px;background:#0F172A;border:1px solid #475569;border-radius:12px;font-size:15px;color:#F8FAFC}
.form-input:focus{outline:none;border-color:#818CF8;box-shadow:0 0 0 3px rgba(79,70,229,0.2)}
.btn{width:100%;padding:16px;border-radius:12px;font-size:16px;font-weight:600;border:none;cursor:pointer;transition:all .2s;display:block;text-align:center}
.btn-primary{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:white;box-shadow:0 4px 12px rgba(79,70,229,0.3)}
.btn-primary:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 20px rgba(79,70,229,0.4)}
.btn-primary:disabled{opacity:0.4;cursor:not-allowed}
.btn-outline{background:transparent;border:1px solid #4F46E5;color:#818CF8;margin-top:8px}
.btn-success{background:#10B981;color:white;margin-top:10px}
.btn-danger{background:#EF4444;color:white;margin-top:8px}
.info-card{background:#0F172A;border:1px solid #334155;border-radius:12px;padding:16px;margin:16px 0}
.info-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1E293B}
.info-row:last-child{border-bottom:none}
.info-label{color:#94A3B8;font-size:13px}
.info-value{color:#F8FAFC;font-family:monospace;font-size:13px;word-break:break-all;text-align:right;max-width:60%}
.info-value-sm{color:#F8FAFC;font-family:monospace;font-size:11px;word-break:break-all;text-align:right;max-width:65%}
.alert{border-radius:12px;padding:14px 16px;margin:12px 0;text-align:center;font-size:14px}
.alert-info{background:#1E293B;border:1px solid #3B82F6;color:#3B82F6}
.alert-success{background:rgba(16,185,129,0.1);border:1px solid #10B981;color:#10B981}
.alert-error{background:rgba(239,68,68,0.1);border:1px solid #EF4444;color:#EF4444}
.spinner{width:36px;height:36px;border:3px solid #334155;border-top-color:#818CF8;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 14px}
@keyframes spin{to{transform:rotate(360deg)}}
.loading{padding:24px 0;text-align:center;color:#94A3B8}
.mode-group{display:flex;gap:10px}
.mode-btn{flex:1;padding:12px;background:#0F172A;border:2px solid #475569;border-radius:12px;text-align:center;cursor:pointer;font-weight:500;color:#CBD5E1;font-size:14px}
.mode-btn.active{background:#4F46E5;border-color:#6366F1;color:white}
.hint{font-size:12px;color:#64748B;text-align:center;margin-top:10px;line-height:1.6}
.footer{text-align:center;margin-top:16px;font-size:11px;color:#475569}
a{color:#818CF8;text-decoration:none}
.hidden{display:none}
</style>
</head>
<body>
<div class="card">
<div class="card-header"><h1>奕涵</h1><p>JumperVPN 自动注册</p></div>
<div class="card-body">

<div id="page1">
  <div class="form-group">
    <div class="form-label">📱 设备模式</div>
    <div class="mode-group">
      <div class="mode-btn active" data-mode="ios">iOS</div>
      <div class="mode-btn" data-mode="windows">Windows</div>
    </div>
  </div>
  <button class="btn btn-primary" id="btnStart" onclick="doStart()">🚀 开始注册</button>
  <div class="hint">自动创建临时邮箱 + 发送验证码</div>
</div>

<div id="page2" class="hidden">
  <div class="loading">
    <div class="spinner"></div>
    <p id="loadMsg">正在创建邮箱...</p>
  </div>
</div>

<div id="page3" class="hidden">
  <div id="page3body"></div>
</div>

<div class="footer">© 2026 奕涵</div>
</div></div>

<script>
var gMode = 'ios';
var gState = '';
var gEmail = '';

// Mode buttons
var mbtns = document.querySelectorAll('.mode-btn');
mbtns.forEach(function(b){
  b.onclick = function(){
    mbtns.forEach(function(x){x.classList.remove('active')});
    b.classList.add('active');
    gMode = b.getAttribute('data-mode');
  };
});

function show(id){
  document.getElementById('page1').classList.add('hidden');
  document.getElementById('page2').classList.add('hidden');
  document.getElementById('page3').classList.add('hidden');
  document.getElementById(id).classList.remove('hidden');
}

function doStart(){
  show('page2');
  document.getElementById('loadMsg').innerText = '正在创建临时邮箱...';
  document.getElementById('btnStart').disabled = true;

  fetch('/api/create_and_send', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({mode: gMode})
  }).then(function(r){return r.json()}).then(function(d){
    if(d.success){
      gState = d.state;
      gEmail = d.email;
      showStep3();
    } else {
      showError('创建失败: ' + (d.error || '未知错误'));
    }
  }).catch(function(e){
    showError('网络错误: ' + e.message);
  });
}

function showStep3(){
  show('page3');
  document.getElementById('page3body').innerHTML =
    '<div class="alert alert-success">✅ 验证码已发送到 <b>' + gEmail + '</b></div>' +
    '<a href="https://zemail.me/mailbox" target="_blank" rel="noopener"><button class="btn btn-primary" type="button">📬 打开收件箱查看验证码</button></a>' +
    '<div class="hint">点击上方按钮在新标签页打开收件箱<br>找到 JumperVPN 发来的6位数字验证码</div>' +
    '<div class="form-group" style="margin-top:20px"><div class="form-label">🔢 输入验证码</div>' +
    '<input type="text" id="codeInp" class="form-input" style="font-size:24px;text-align:center;letter-spacing:4px" placeholder="000000" maxlength="6" inputmode="numeric" oninput="onCodeInput()" autocomplete="off"></div>' +
    '<button class="btn btn-success" id="btnReg" disabled onclick="doRegister()">✅ 完成注册</button>' +
    '<button class="btn btn-outline" onclick="location.reload()">🔄 重新开始</button>';
}

function onCodeInput(){
  var inp = document.getElementById('codeInp');
  var v = inp.value.replace(/\\D/g,'').slice(0,6);
  inp.value = v;
  document.getElementById('btnReg').disabled = (v.length !== 6);
}

function doRegister(){
  var code = document.getElementById('codeInp').value.replace(/\\D/g,'');
  if(code.length !== 6) return;

  show('page2');
  document.getElementById('loadMsg').innerText = '正在注册账号...';

  fetch('/api/finish_register', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({state: gState, code: code})
  }).then(function(r){return r.json()}).then(function(d){
    if(d.success){
      showResult(d.result);
    } else {
      showError(d.error || '注册失败，验证码可能不正确');
    }
  }).catch(function(e){
    showError('网络错误: ' + e.message);
  });
}

function showResult(r){
  show('page3');
  document.getElementById('page3body').innerHTML =
    '<div class="alert alert-success">🎉 注册成功！</div>' +
    '<div class="info-card">' +
    '<div class="info-row"><span class="info-label">📧 邮箱</span><span class="info-value">' + r.email + '</span></div>' +
    '<div class="info-row"><span class="info-label">🔐 密码</span><span class="info-value">' + r.pwd + '</span></div>' +
    '<div class="info-row"><span class="info-label">⏱ 时长</span><span class="info-value">' + r.free_time + '</span></div>' +
    '<div class="info-row"><span class="info-label">📅 到期</span><span class="info-value">' + r.end_time + '</span></div>' +
    '<div class="info-row"><span class="info-label">🔑 Token</span><span class="info-value-sm" id="tok">' + r.token + '</span></div></div>' +
    '<button class="btn btn-primary" onclick="copyTok()">📋 复制 Token</button>' +
    '<button class="btn btn-outline" onclick="location.reload()">🔄 再注册一个</button>';
}

function copyTok(){
  var tok = document.getElementById('tok').innerText;
  navigator.clipboard.writeText(tok).then(function(){
    alert('Token 已复制到剪贴板!');
  }).catch(function(){
    prompt('请手动复制 Token:', tok);
  });
}

function showError(msg){
  show('page3');
  document.getElementById('page3body').innerHTML =
    '<div class="alert alert-error">❌ ' + msg + '</div>' +
    '<div class="hint" style="margin:12px 0">请检查后重试</div>' +
    '<button class="btn btn-primary" onclick="doStart()">🔄 重试(换新邮箱)</button>' +
    '<button class="btn btn-outline" onclick="location.reload()">🏠 返回首页</button>';
}
</script>
</body>
</html>'''


# ====== API helpers ======

def ms(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

def api_call(path, method='GET', body=None, token=None, imei=None, mode='ios'):
    ctx = ssl.create_default_context()
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
        resp = opener.open(req, timeout=30)
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

def create_zemail_mailbox():
    ctx = ssl._create_unverified_context()
    cj = http.cookiejar.CookieJar()
    zop = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cj))

    req = urllib.request.Request(f'{ZEMAIL}/mailbox',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
    resp = zop.open(req, timeout=30)
    html = resp.read().decode('utf-8', 'replace')

    import html as _h
    snap_raw = re.search(r'wire:snapshot="([^"]*)"', html)
    if not snap_raw:
        raise Exception('No snapshot found in page')
    snapshot = json.loads(_h.unescape(snap_raw.group(1)))
    xsrf = next((urllib.request.unquote(c.value) for c in cj if c.name == 'XSRF-TOKEN'), '')

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': xsrf,
        'Origin': ZEMAIL,
        'Referer': f'{ZEMAIL}/mailbox'
    }
    payload = {"components": [{"snapshot": json.dumps(snapshot), "updates": {}, "calls": [{"path": "", "method": "createMailbox", "params": []}]}]}
    req2 = urllib.request.Request(f'{ZEMAIL}/livewire/update', data=json.dumps(payload).encode(), method='POST', headers=headers)
    result = json.loads(zop.open(req2, timeout=30).read().decode())
    eff = result['components'][0].get('effects', {}).get('html', '')
    emails = list(set(re.findall(r'([\w.+-]+@[\w.-]+\.\w+)', eff + json.dumps(result, ensure_ascii=False))))
    for e in emails:
        if e.count('@') == 1 and 'zemail' not in e.lower() and 'weml' not in e.lower() and 'example' not in e.lower():
            return e
    raise Exception('Cannot parse email from response: ' + str(emails)[:200])


# ====== Routes ======

@app.route('/')
def index():
    return HTML

@app.route('/api/create_and_send', methods=['POST'])
def api_create():
    try:
        data = request.get_json(silent=True) or {}
        mode = data.get('mode', 'ios')
        pwd_raw = ''.join(__import__('random').choices('ABCDEFGHJKLMNPQRSTWXYZabcdefghjkmnpqrstwxyz23456789', k=12))

        email = create_zemail_mailbox()
        imei = '{' + str(uuid.uuid4()).upper() + '}'

        dr = api_call('device/init', imei=imei, mode=mode)
        if dr.get('code') != 200:
            return jsonify({'success': False, 'error': '设备初始化失败: ' + str(dr.get('message', dr.get('msg', '?')))})

        device_token = dr['data']['user_info']['token']
        sr = api_call('user/send_email_code', method='POST',
                      body={'email': email, 'type': 10},
                      token=device_token, imei=imei, mode=mode)
        if sr.get('code') not in (200, 0):
            return jsonify({'success': False, 'error': '发送验证码失败: ' + str(sr.get('message', sr.get('msg', '?')))})

        state_json = json.dumps({
            'email': email, 'pwd_raw': pwd_raw, 'imei': imei,
            'device_token': device_token, 'mode': mode
        }, ensure_ascii=False)
        state_b64 = base64.b64encode(state_json.encode()).decode()

        return jsonify({'success': True, 'email': email, 'state': state_b64})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:300]})

@app.route('/api/finish_register', methods=['POST'])
def api_finish():
    try:
        data = request.get_json(silent=True) or {}
        s = json.loads(base64.b64decode(data.get('state', '')).decode())
    except:
        return jsonify({'success': False, 'error': '状态过期，请重新开始'})

    code = data.get('code', '').strip()
    email, pwd_raw, imei, device_token, mode = s['email'], s['pwd_raw'], s['imei'], s['device_token'], s['mode']
    pwd_md5 = hashlib.md5(pwd_raw.encode()).hexdigest()

    try:
        reg_result = None
        for pw, _ in [(pwd_md5, 'MD5'), (pwd_raw, 'plain')]:
            rr = api_call('user/signup', method='POST',
                         body={'email': email, 'password': pw, 'repassword': pw, 'code': code},
                         token=device_token, imei=imei, mode=mode)
            if rr.get('code') in (200, 0):
                reg_result = rr; break
        if not reg_result:
            return jsonify({'success': False, 'error': '验证码不正确或已过期'})

        udata = reg_result.get('data', {}).get('user_info', {})
        free = udata.get('free_remaining_time', 0)
        end = udata.get('free_end_time', '')
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
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:300]})


if __name__ == '__main__':
    print('http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
