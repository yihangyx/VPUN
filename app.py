from flask import Flask, request, Response
import requests
import hmac
import hashlib

app = Flask(__name__)

SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'

def make_sign(path):
    return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

@app.route('/api/beeinbox/', defaults={'target_path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/api/beeinbox/<path:target_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_beeinbox(target_path):
    if request.method == 'OPTIONS':
        return ('', 204)
    
    query_string = request.query_string.decode()
    url = f'https://amades.site/{target_path}'
    if query_string:
        url += '?' + query_string
    
    resp = requests.request(
        method=request.method,
        url=url,
        headers={
            'User-Agent': request.headers.get('User-Agent', ''),
            'Accept': request.headers.get('Accept', '*/*'),
            'Referer': 'https://amades.site/',
        },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True,
    )
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'host']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    response = Response(resp.content, resp.status_code, headers)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/vpn/', defaults={'target_path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
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
    headers['device-name'] = request.headers.get('device-name', 'iPhone 15 Pro')
    
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
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JumperVPN 自动注册</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif; background: #1C1C1E; color: #fff; height: 100vh; display: flex; flex-direction: column; }
        .header { background: #000; padding: 12px 20px; display: flex; align-items: center; gap: 12px; }
        .dots { display: flex; gap: 6px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot.red { background: #FF5F57; }
        .dot.yellow { background: #FEBC2E; }
        .dot.green { background: #28C840; }
        .title { font-size: 14px; font-weight: 600; color: #8E8E93; }
        .status { margin-left: auto; font-size: 13px; color: #30D158; }
        .main { flex: 1; display: flex; overflow: hidden; }
        .sidebar { width: 320px; background: #2C2C2E; padding: 20px; display: flex; flex-direction: column; gap: 16px; overflow-y: auto; }
        .content { flex: 1; display: flex; flex-direction: column; background: #1C1C1E; }
        .card { background: #2C2C2E; border-radius: 12px; padding: 16px; }
        .card-title { font-size: 14px; font-weight: 600; margin-bottom: 12px; }
        .btn { background: #BF5AF2; color: white; border: none; padding: 12px 20px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; width: 100%; }
        .btn:disabled { background: #48484A; cursor: not-allowed; }
        .email-box { background: #1C1C1E; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 13px; color: #64D2FF; word-break: break-all; margin-top: 8px; }
        .code-box { background: #1C1C1E; border-radius: 8px; padding: 16px; font-family: monospace; font-size: 28px; font-weight: 700; color: #30D158; text-align: center; letter-spacing: 4px; margin-top: 8px; }
        .log { background: #1C1C1E; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 12px; overflow-y: auto; max-height: 200px; line-height: 1.6; }
        .log .ok { color: #30D158; }
        .log .err { color: #FF453A; }
        .log .info { color: #8E8E93; }
        .log .run { color: #0A84FF; }
        .log .warn { color: #FF9F0A; }
        .iframe-container { flex: 1; background: #fff; margin: 16px; border-radius: 12px; overflow: hidden; }
        .iframe-container iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
        <div class="title">JumperVPN 自动注册工具</div>
        <div class="status" id="status">● 就绪</div>
    </div>
    <div class="main">
        <div class="sidebar">
            <div class="card">
                <div class="card-title">🚀 一键注册</div>
                <button class="btn" id="btn-start" onclick="startFullFlow()">开始自动注册</button>
            </div>
            <div class="card">
                <div class="card-title">📧 临时邮箱</div>
                <div class="email-box" id="email">等待创建邮箱...</div>
            </div>
            <div class="card">
                <div class="card-title">🔢 验证码</div>
                <div class="code-box" id="code">----</div>
            </div>
            <div class="card">
                <div class="card-title">📋 运行日志</div>
                <div class="log" id="log"></div>
            </div>
        </div>
        <div class="content">
            <div class="iframe-container">
                <iframe id="mailFrame" src="/api/beeinbox/" onload="onFrameLoad()"></iframe>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
    <script>
        let state = { email: '', code: '', imei: '', deviceToken: '', running: false };
        
        function log(msg, type='info') {
            const t = new Date().toLocaleTimeString();
            document.getElementById('log').innerHTML += `<div class="${type}">[${t}] ${msg}</div>`;
            document.getElementById('log').scrollTop = 99999;
        }
        function setStatus(msg, color='#30D158') {
            document.getElementById('status').textContent = '● ' + msg;
            document.getElementById('status').style.color = color;
        }
        
        function extractEmail() {
            try {
                const iframe = document.getElementById('mailFrame');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const els = doc.querySelectorAll('*');
                for (let el of els) {
                    const data = el.getAttribute('wire:initial-data');
                    if (data && data.includes('frontend.actions')) {
                        const email = JSON.parse(data).serverMemo.data.email;
                        if (email && email !== state.email) {
                            state.email = email;
                            document.getElementById('email').textContent = email;
                            log('📧 邮箱: ' + email, 'ok');
                        }
                        return email;
                    }
                }
            } catch(e) {}
        }
        
        function extractCode() {
            try {
                const iframe = document.getElementById('mailFrame');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const iframes = doc.querySelectorAll('iframe');
                for (let i of iframes) {
                    try {
                        const text = (i.contentDocument || i.contentWindow.document).body.innerText;
                        const match = text.match(/\\b(\\d{4,6})\\b/);
                        if (match) {
                            const code = match[1];
                            if (code !== state.code) {
                                state.code = code;
                                document.getElementById('code').textContent = code;
                                log('🔢 验证码: ' + code, 'ok');
                            }
                            return code;
                        }
                    } catch(e) {}
                }
            } catch(e) {}
        }
        
        setInterval(() => { extractEmail(); extractCode(); }, 2000);
        function onFrameLoad() { log('📬 邮箱页面加载完成', 'info'); }
        
        async function vpnApi(path, method='GET', body=null, token=null, imei=null) {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['j-token'] = token;
            if (imei) headers['imei'] = imei;
            const resp = await fetch('/api/vpn/' + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
            return resp.json();
        }
        
        function generateUUID() {
            return '{' + 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
                const r = Math.random()*16|0;
                return (c==='x' ? r : (r&0x3|0x8)).toString(16).toUpperCase();
            }) + '}';
        }
        
        async function startFullFlow() {
            if (state.running) return;
            state.running = true;
            document.getElementById('btn-start').disabled = true;
            setStatus('注册中...', '#FF9F0A');
            
            try {
                log('=== 开始自动注册 ===', 'run');
                state.imei = generateUUID();
                log('📱 IMEI: ' + state.imei, 'info');
                
                log('🔄 device/init ...', 'run');
                const initRes = await vpnApi('device/init', 'GET', null, null, state.imei);
                if (initRes.code !== 200) {
                    log('❌ device/init 失败: ' + JSON.stringify(initRes), 'err');
                    return;
                }
                state.deviceToken = initRes.data.user_info.token;
                log('✅ device token 获取成功', 'ok');
                
                log('⏳ 等待临时邮箱创建...', 'run');
                let wait = 0;
                while (!state.email && wait < 30) { await new Promise(r=>setTimeout(r,1000)); wait++; }
                if (!state.email) { log('❌ 邮箱创建超时', 'err'); return; }
                
                log('📤 发送验证码到 ' + state.email + ' ...', 'run');
                const sendRes = await vpnApi('user/send_email_code', 'POST', { email: state.email, type: 10 }, state.deviceToken, state.imei);
                if (sendRes.code !== 200) {
                    log('❌ 发送失败: ' + JSON.stringify(sendRes), 'err');
                    return;
                }
                log('✅ 验证码已发送', 'ok');
                
                log('⏳ 等待接收验证码...', 'run');
                wait = 0;
                while (!state.code && wait < 30) { await new Promise(r=>setTimeout(r,1000)); wait++; }
                if (!state.code) { log('❌ 等待验证码超时', 'err'); return; }
                
                const pwdRaw = Math.random().toString(36).slice(-8) + Math.random().toString(36).slice(-8);
                const pwdMd5 = CryptoJS.MD5(pwdRaw).toString();
                log('📝 注册账号 | 密码: ' + pwdRaw, 'run');
                
                const signupRes = await vpnApi('user/signup', 'POST', { email: state.email, password: pwdMd5, repassword: pwdMd5, code: state.code }, state.deviceToken, state.imei);
                
                if (signupRes.code === 200) {
                    const free = signupRes.data.user_info.free_remaining_time;
                    const h = Math.floor(free/3600), m = Math.floor((free%3600)/60);
                    log('✅ 注册成功! 剩余 ' + h + '小时' + m + '分', 'ok');
                    log('🔑 密码: ' + pwdRaw, 'warn');
                    setStatus('✅ 注册成功 | ' + h + 'h' + m + 'm', '#30D158');
                } else {
                    log('❌ 注册失败: ' + signupRes.message, 'err');
                }
            } catch (e) {
                log('❌ 异常: ' + e.message, 'err');
                setStatus('错误', '#FF453A');
            } finally {
                state.running = false;
                document.getElementById('btn-start').disabled = false;
            }
        }
    </script>
</body>
</html>'''
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    app.run()
