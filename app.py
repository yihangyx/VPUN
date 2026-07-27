#!/usr/bin/env python3
"""奕涵 - JumperVPN 自动注册 v5 — 代理收件箱 (Vercel-ready, cookies in state)"""

import json, hashlib, hmac, uuid, re, random, base64, traceback, time
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
.btn-primary{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:white}
.btn-primary:hover:not(:disabled){transform:translateY(-2px)}
.btn-primary:disabled{opacity:0.4;cursor:not-allowed}
.btn-outline{background:transparent;border:1px solid #4F46E5;color:#818CF8;margin-top:8px}
.btn-success{background:#10B981;color:white;margin-top:10px}
.info-card{background:#0F172A;border:1px solid #334155;border-radius:12px;padding:16px;margin:16px 0}
.info-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1E293B}
.info-row:last-child{border-bottom:none}
.info-label{color:#94A3B8;font-size:13px}
.info-value{color:#F8FAFC;font-family:monospace;font-size:13px;word-break:break-all;text-align:right;max-width:60%}
.info-value-sm{color:#F8FAFC;font-family:monospace;font-size:11px;word-break:break-all;text-align:right;max-width:65%}
.alert{border-radius:12px;padding:14px 16px;margin:12px 0;text-align:center;font-size:14px}
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
.hidden{display:none!important}
.inbox-panel{background:#0F172A;border:1px solid #10B981;border-radius:0 0 12px 12px;overflow:hidden;max-height:360px;overflow-y:auto}
.inbox-header{background:rgba(16,185,129,0.1);padding:10px 14px;font-size:13px;color:#10B981;display:flex;justify-content:space-between;align-items:center;border:1px solid #334155;border-radius:12px 12px 0 0}
.inbox-msg{padding:12px 14px;border-bottom:1px solid #1E293B;font-size:13px}
.inbox-from{color:#818CF8;font-size:12px}
.inbox-subj{color:#F8FAFC;margin:4px 0;font-weight:500}
.inbox-code{font-size:22px;font-weight:700;color:#10B981;letter-spacing:3px;margin-top:4px}
.inbox-empty{text-align:center;padding:40px 20px;color:#64748B;font-size:14px}
.code-highlight{background:#10B981;color:white;padding:4px 12px;border-radius:8px;font-size:20px;letter-spacing:4px;font-weight:700;display:inline-block;margin:8px 0}
</style>
</head>
<body>
<div class="card">
<div class="card-header"><h1>奕涵</h1><p>JumperVPN 自动注册</p></div>
<div class="card-body">
<div id="page1"><div class="form-group"><div class="form-label">📱 设备模式</div><div class="mode-group">
<div class="mode-btn active" data-mode="ios">iOS</div>
<div class="mode-btn" data-mode="windows">Windows</div></div></div>
<button class="btn btn-primary" id="btnStart" onclick="doStart()">🚀 开始注册</button>
<div class="hint">自动创建邮箱 + 发送验证码 + 监控收件箱</div></div>
<div id="page2" class="hidden"><div class="loading"><div class="spinner"></div><p id="loadMsg">正在创建邮箱...</p></div></div>
<div id="page3" class="hidden"><div id="page3body"></div></div>
<div class="footer">© 2026 奕涵</div></div></div>
<script>
var gMode='ios',gState='',gEmail='',gPollId=null,gCount=0;
document.querySelectorAll('.mode-btn').forEach(function(b){b.onclick=function(){
document.querySelectorAll('.mode-btn').forEach(function(x){x.classList.remove('active')});b.classList.add('active');gMode=b.getAttribute('data-mode');}});
function show(id){document.getElementById('page1').classList.add('hidden');document.getElementById('page2').classList.add('hidden');document.getElementById('page3').classList.add('hidden');document.getElementById(id).classList.remove('hidden');}
function doStart(){show('page2');document.getElementById('loadMsg').innerText='正在创建临时邮箱...';
fetch('/api/create_and_send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:gMode})})
.then(function(r){return r.json()}).then(function(d){if(d.success){gState=d.state;gEmail=d.email;showStep3();}else{showError('创建失败: '+(d.error||'?'));}}).catch(function(e){showError('网络错误: '+e.message);});}
function showStep3(){show('page3');
var h='<div class="alert alert-success">✅ 验证码已发送到 <b>'+gEmail+'</b></div>';
h+='<div class="inbox-header" style="margin-top:12px">📬 收件箱 <span id="pst" style="font-size:12px;opacity:0.7">等待邮件...</span></div>';
h+='<div class="inbox-panel" id="ip"><div class="inbox-empty">等待 JumperVPN 验证码邮件...</div></div>';
h+='<div class="form-group" style="margin-top:20px"><div class="form-label">🔢 输入验证码</div><input type="text" id="ci" class="form-input" style="font-size:24px;text-align:center;letter-spacing:4px" placeholder="000000" maxlength="6" inputmode="numeric" oninput="onCi()" autocomplete="off"></div>';
h+='<button class="btn btn-success" id="br" disabled onclick="doReg()">✅ 完成注册</button><button class="btn btn-outline" onclick="location.reload()">🔄 重新开始</button>';
document.getElementById('page3body').innerHTML=h;startPoll();}
function onCi(){var i=document.getElementById('ci');if(!i)return;var v=i.value.replace(/\\D/g,'').slice(0,6);i.value=v;var b=document.getElementById('br');if(b)b.disabled=v.length!==6;}
function startPoll(){gCount=0;if(gPollId)clearInterval(gPollId);gPollId=setInterval(pollInbox,4000);pollInbox();}
function pollInbox(){gCount+=4;var s=document.getElementById('pst');if(s)s.innerText=gCount+'s';
fetch('/api/check_inbox',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({state:gState})})
.then(function(r){return r.json()}).then(function(d){
if(d.msgs&&d.msgs.length>0){clearInterval(gPollId);gPollId=null;var p=document.getElementById('ip');if(!p)return;
var l='';d.msgs.forEach(function(m){l+='<div class="inbox-msg"><div class="inbox-from">发件人: '+(m.f||'?')+'</div><div class="inbox-subj">'+(m.s||'(无)')+'</div>'+(m.c?'<div class="code-highlight">'+m.c+'</div>':'')+'</div>';});p.innerHTML=l;if(s)s.innerText='✅ 收到邮件!';
if(d.code&&document.getElementById('ci')){document.getElementById('ci').value=d.code;onCi();}}
else if(d.wait){var p=document.getElementById('ip');if(p&&d.wait!=='ok')p.innerHTML='<div class="inbox-empty">'+d.wait+'</div>';}
}).catch(function(){});}
function doReg(){var ci=document.getElementById('ci');if(!ci)return;var c=ci.value.replace(/\\D/g,'');if(c.length!==6)return;
show('page2');document.getElementById('loadMsg').innerText='正在注册...';if(gPollId){clearInterval(gPollId);gPollId=null;}
fetch('/api/finish_register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({state:gState,code:c})})
.then(function(r){return r.json()}).then(function(d){if(d.success){showR(d.result);}else{showError(d.error||'注册失败');}}).catch(function(e){showError(e.message);});}
function showR(r){show('page3');document.getElementById('page3body').innerHTML=
'<div class="alert alert-success">🎉 注册成功!</div><div class="info-card">'+
'<div class="info-row"><span class="info-label">📧 邮箱</span><span class="info-value">'+r.email+'</span></div>'+
'<div class="info-row"><span class="info-label">🔐 密码</span><span class="info-value">'+r.pwd+'</span></div>'+
'<div class="info-row"><span class="info-label">⏱ 时长</span><span class="info-value">'+r.free_time+'</span></div>'+
'<div class="info-row"><span class="info-label">📅 到期</span><span class="info-value">'+r.end_time+'</span></div>'+
'<div class="info-row"><span class="info-label">🔑 Token</span><span class="info-value-sm" id="tok">'+r.token+'</span></div></div>'+
'<button class="btn btn-primary" onclick="copyTok()">📋 Token</button><button class="btn btn-outline" onclick="location.reload()">🔄 再注册一个</button>';}
function copyTok(){var t=document.getElementById('tok').innerText;navigator.clipboard.writeText(t).then(function(){alert('Token 已复制!')}).catch(function(){prompt('Token:',t)});}
function showError(m){if(gPollId){clearInterval(gPollId);gPollId=null;}show('page3');document.getElementById('page3body').innerHTML='<div class="alert alert-error">❌ '+m+'</div><div class="hint" style="margin:12px 0">请重试</div><button class="btn btn-primary" onclick="doStart()">🔄 重试</button><button class="btn btn-outline" onclick="location.reload()">🏠 返回</button>';}
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

def serialize_cookies(cj):
    """序列化 cookie jar 为 base64"""
    cookies = []
    for c in cj:
        if c.name in ('XSRF-TOKEN', 'zemail_session', 'laravel_session'):
            cookies.append({'n': c.name, 'v': c.value, 'd': c.domain or '', 'p': c.path or '/'})
    return base64.b64encode(json.dumps(cookies).encode()).decode()

def restore_cookies(b64):
    """从 base64 恢复 cookie jar"""
    cj = http.cookiejar.CookieJar()
    try:
        cookies = json.loads(base64.b64decode(b64).decode())
        for c in cookies:
            ck = http.cookiejar.Cookie(
                version=0, name=c['n'], value=c['v'],
                port=None, port_specified=False,
                domain=c['d'], domain_specified=bool(c['d']),
                domain_initial_dot=c['d'].startswith('.'),
                path=c['p'], path_specified=True,
                secure=True, expires=None, discard=False,
                comment=None, comment_url=None, rest={}, rfc2109=False)
            cj.set_cookie(ck)
    except:
        pass
    return cj


# ====== Core ======

def create_zemail_mailbox():
    ctx = ssl._create_unverified_context()
    cj = http.cookiejar.CookieJar()
    zop = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx), urllib.request.HTTPCookieProcessor(cj))

    req = urllib.request.Request(f'{ZEMAIL}/mailbox',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    resp = zop.open(req, timeout=25)
    html = resp.read().decode('utf-8', 'replace')

    import html as _h
    snap_raw = re.search(r'wire:snapshot="([^"]*)"', html)
    if not snap_raw:
        raise Exception('No snapshot found')
    snapshot = json.loads(_h.unescape(snap_raw.group(1)))
    xsrf = next((urllib.request.unquote(c.value) for c in cj if c.name == 'XSRF-TOKEN'), '')

    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest', 'X-XSRF-TOKEN': xsrf,
        'Origin': ZEMAIL, 'Referer': f'{ZEMAIL}/mailbox'
    }
    payload = {"components": [{"snapshot": json.dumps(snapshot), "updates": {}, "calls": [{"path": "", "method": "createMailbox", "params": []}]}]}
    req2 = urllib.request.Request(f'{ZEMAIL}/livewire/update', data=json.dumps(payload).encode(), method='POST', headers=headers)
    result = json.loads(zop.open(req2, timeout=25).read().decode())

    eff = result['components'][0].get('effects', {}).get('html', '')
    combined = eff + json.dumps(result, ensure_ascii=False)
    emails = list(set(re.findall(r'([\w.+-]+@[\w.-]+\.\w+)', combined)))
    email = None
    for e in emails:
        if e.count('@') == 1 and 'zemail' not in e.lower() and 'weml' not in e.lower() and 'example' not in e.lower():
            email = e; break
    if not email: raise Exception('Cannot parse email')
    return email, serialize_cookies(cj)


def check_inbox_with_cookies(cookie_b64):
    cj = restore_cookies(cookie_b64)
    ctx = ssl._create_unverified_context()
    zop = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx), urllib.request.HTTPCookieProcessor(cj))

    req = urllib.request.Request(f'{ZEMAIL}/mailbox',
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        resp = zop.open(req, timeout=20)
        html = resp.read().decode('utf-8', 'replace')
    except Exception as e:
        return [], None

    import html as _h
    msgs, code = [], None

    # Try to find email data in wire:data attributes
    wire_blocks = re.findall(r'wire:data="([^"]*)"', html)
    seen = set()
    for wb in wire_blocks:
        try:
            decoded = _h.unescape(wb)
            # Check for email fields
            has_from = '"from"' in decoded or '"mail_from"' in decoded
            has_subj = '"subject"' in decoded or '"mail_subject"' in decoded
            if not (has_from and has_subj): continue
            data = json.loads(decoded)
            if not isinstance(data, dict): continue
            f = data.get('from') or data.get('mail_from') or ''
            s = data.get('subject') or data.get('mail_subject') or ''
            b = data.get('body') or data.get('text') or data.get('preview') or ''
            key = f + s
            if key in seen: continue
            seen.add(key)
            m = {'f': str(f), 's': str(s)}
            codes = re.findall(r'\b(\d{6})\b', str(s) + ' ' + str(b))
            if codes:
                m['c'] = codes[0]
                if not code: code = codes[0]
            if f or s: msgs.append(m)
        except: pass

    # Fallback: grep the whole HTML unescaped text
    if not msgs:
        text = _h.unescape(html)
        codes = re.findall(r'\b(\d{6})\b', text)
        if codes:
            code = codes[0]
            msgs = [{'f': 'JumperVPN', 's': 'Verification Code', 'c': code}]

    return msgs, code


# ====== Routes ======

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
        email, cookies_b64 = create_zemail_mailbox()
        imei = '{' + str(uuid.uuid4()).upper() + '}'
        dr = api_call('device/init', imei=imei, mode=mode)
        if dr.get('code') != 200:
            return jsonify({'success': False, 'error': '初始化失败: '+str(dr.get('message',dr.get('msg','?')))})
        dt = dr['data']['user_info']['token']
        sr = api_call('user/send_email_code', method='POST',
                      body={'email': email, 'type': 10}, token=dt, imei=imei, mode=mode)
        if sr.get('code') not in (200, 0):
            return jsonify({'success': False, 'error': '发送验证码失败: '+str(sr.get('message',sr.get('msg','?')))})
        state = base64.b64encode(json.dumps({
            'e': email, 'p': pwd_raw, 'i': imei, 't': dt, 'm': mode, 'c': cookies_b64
        }, ensure_ascii=False).encode()).decode()
        return jsonify({'success': True, 'email': email, 'state': state})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)[:300]})

@app.route('/api/check_inbox', methods=['POST'])
def api_check():
    try:
        data = request.get_json(silent=True) or {}
        s = json.loads(base64.b64decode(data.get('state', '')).decode())
    except:
        return jsonify({'wait': '状态错误'})

    try:
        msgs, code = check_inbox_with_cookies(s['c'])
        if not msgs:
            return jsonify({'wait': '等待邮件中...'})
        return jsonify({'msgs': msgs, 'code': code})
    except Exception as e:
        return jsonify({'wait': str(e)[:200]})

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
        free, end = ud.get('free_remaining_time', 0), ud.get('free_end_time', '')
        h, mn = free // 3600, (free % 3600) // 60
        ft = t
        for pw in [p_md5, p]:
            lr = api_call('user/signin', method='POST',
                         body={'email': e, 'password': pw}, token=t, imei=i, mode=m)
            if lr.get('code') in (200, 0):
                tk = lr.get('data', {}).get('user_info', {}).get('token', '')
                if tk: ft = tk; break
        return jsonify({'success': True, 'result': {
            'email': e, 'pwd': p, 'free_time': f'{h}时{mn}分', 'end_time': end, 'token': ft
        }})
    except Exception as ex:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(ex)[:300]})

if __name__ == '__main__':
    print('http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
