#!/usr/bin/env python3
"""JumperVPN 纯API注册版 - 可部署"""
import json, time, hashlib, hmac, uuid, base64, re, random, string
import urllib.request, urllib.error, ssl
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
import threading

BASE = 'https://api.jumperservice.com/v1/'
SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14'
MAIL_TM = 'https://api.mail.tm'
PC_NAME = 'DESKTOP-Web'

ctx = ssl.create_default_context()
no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler, urllib.request.HTTPSHandler(context=ctx))
opener.addheaders = []

app = Flask(__name__)

# 会话存储（内存中，重启会丢失）
sessions = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JumperVPN 注册器</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
            min-height: 100vh; 
            padding: 40px 20px;
        }
        .container { 
            max-width: 500px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            border-radius: 20px; 
            box-shadow: 0 25px 80px rgba(0,0,0,0.25); 
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 32px 24px; 
            text-align: center;
            position: relative;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.5;
        }
        .header-content {
            position: relative;
            z-index: 1;
        }
        .header h1 { 
            font-size: 32px; 
            margin-bottom: 8px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .header p {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 500;
        }
        .content { 
            padding: 28px 24px; 
        }
        .form-group { 
            margin-bottom: 20px; 
        }
        label { 
            display: block; 
            font-weight: 600; 
            color: #374151; 
            margin-bottom: 8px; 
            font-size: 14px;
        }
        .input-wrapper {
            position: relative;
        }
        input[type="text"], input[type="password"] { 
            width: 100%; 
            padding: 14px 16px; 
            border: 2px solid #e5e7eb; 
            border-radius: 12px; 
            font-size: 15px; 
            transition: all 0.3s;
            background: #f9fafb;
        }
        input[type="text"]:focus, input[type="password"]:focus { 
            outline: none; 
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        .toggle-btn {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            color: #6b7280;
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 6px;
            transition: all 0.2s;
        }
        .toggle-btn:hover {
            background: #f3f4f6;
            color: #374151;
        }
        .radio-group { 
            display: flex; 
            gap: 12px; 
            margin-top: 8px; 
        }
        .radio-item { 
            flex: 1;
            display: flex; 
            align-items: center; 
            justify-content: center;
            gap: 8px;
            padding: 14px;
            background: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .radio-item:hover {
            border-color: #c7d2fe;
        }
        .radio-item input {
            margin: 0;
            accent-color: #667eea;
        }
        .radio-item.selected {
            border-color: #667eea;
            background: #eff6ff;
        }
        .btn { 
            width: 100%; 
            padding: 16px; 
            border: none; 
            border-radius: 12px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: 600; 
            transition: all 0.3s;
        }
        .btn:disabled { 
            opacity: 0.6; 
            cursor: not-allowed;
        }
        .btn-primary { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-primary:hover:not(:disabled) { 
            transform: translateY(-2px); 
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }
        .btn-secondary {
            background: #f3f4f6;
            color: #374151;
            margin-top: 12px;
        }
        .btn-secondary:hover:not(:disabled) {
            background: #e5e7eb;
        }
        .result-card { 
            margin-top: 24px; 
            padding: 20px; 
            border-radius: 16px; 
            background: #f0fdf4; 
            border: 2px solid #86efac; 
            display: none;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .result-card.error { 
            background: #fef2f2; 
            border-color: #fca5a5; 
        }
        .result-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }
        .result-header h3 {
            font-size: 18px;
            color: #166534;
        }
        .result-card.error .result-header h3 {
            color: #991b1b;
        }
        .info-item { 
            display: flex; 
            flex-direction: column;
            padding: 12px; 
            background: white;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .info-label { 
            font-weight: 600; 
            color: #6b7280; 
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .info-value { 
            color: #1f2937; 
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            word-break: break-all;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .copy-btn {
            padding: 6px 10px;
            background: #f3f4f6;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            color: #6b7280;
            transition: all 0.2s;
            flex-shrink: 0;
        }
        .copy-btn:hover {
            background: #e5e7eb;
            color: #374151;
        }
        .token-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .token-display {
            flex: 1;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            word-break: break-all;
        }
        .log-box { 
            margin-top: 24px; 
            background: #1f2937; 
            color: #10b981; 
            padding: 16px; 
            border-radius: 12px; 
            font-family: 'Consolas', 'Monaco', monospace; 
            font-size: 13px; 
            height: 280px; 
            overflow-y: auto; 
            line-height: 1.7;
            display: none;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
        }
        .log-box::-webkit-scrollbar {
            width: 8px;
        }
        .log-box::-webkit-scrollbar-track {
            background: #374151;
            border-radius: 4px;
        }
        .log-box::-webkit-scrollbar-thumb {
            background: #6b7280;
            border-radius: 4px;
        }
        .log-entry { 
            margin-bottom: 4px;
        }
        .loading { 
            display: none; 
            text-align: center; 
            padding: 24px;
        }
        .spinner { 
            border: 4px solid #f3f4f6; 
            border-top: 4px solid #667eea; 
            border-radius: 50%; 
            width: 50px; 
            height: 50px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 16px;
        }
        @keyframes spin { 
            0% { transform: rotate(0deg); } 
            100% { transform: rotate(360deg); } 
        }
        .loading p {
            color: #374151;
            font-weight: 500;
        }
        .device-info {
            margin-top: 16px;
            padding: 12px;
            background: #fef3c7;
            border-radius: 10px;
            border: 1px solid #fcd34d;
            font-size: 13px;
            color: #92400e;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🚀 JumperVPN</h1>
                <p>一键注册 · 免费时长</p>
            </div>
        </div>
        <div class="content">
            <form id="registerForm">
                <div class="form-group">
                    <label>📧 邮箱（登录用）</label>
                    <div class="input-wrapper">
                        <input type="text" id="login_email" placeholder="注册成功后自动填充">
                    </div>
                </div>
                <div class="form-group">
                    <label>🔐 密码（登录用）</label>
                    <div class="input-wrapper">
                        <input type="text" id="login_pwd" placeholder="注册成功后自动填充">
                    </div>
                </div>
                <div class="form-group">
                    <label>🎫 邀请码</label>
                    <input type="text" id="invite" value="9QGE5V" placeholder="输入邀请码">
                </div>
                <div class="form-group">
                    <label>⚙️ 设备模式</label>
                    <div class="radio-group">
                        <label class="radio-item selected" id="radio_ios">
                            <input type="radio" name="mode" id="mode_ios" value="ios" checked>
                            iOS
                        </label>
                        <label class="radio-item" id="radio_windows">
                            <input type="radio" name="mode" id="mode_windows" value="windows">
                            Windows
                        </label>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary" id="submitBtn">✨ 开始注册</button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在注册中，请稍候...</p>
            </div>

            <div class="log-box" id="log_box"></div>

            <div class="result-card" id="result_card">
                <div class="result-header">
                    <h3 id="result_title">✅ 注册成功！</h3>
                </div>
                <div class="info-item">
                    <span class="info-label">邮箱</span>
                    <span class="info-value">
                        <span id="res_email"></span>
                        <button class="copy-btn" onclick="copyText('res_email')">复制</button>
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">密码</span>
                    <span class="info-value">
                        <span id="res_pwd"></span>
                        <button class="copy-btn" onclick="copyText('res_pwd')">复制</button>
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">免费时长</span>
                    <span class="info-value" id="res_free"></span>
                </div>
                <div class="info-item">
                    <span class="info-label">到期时间</span>
                    <span class="info-value" id="res_end"></span>
                </div>
                <div class="info-item">
                    <span class="info-label">JWT Token</span>
                    <span class="info-value">
                        <span class="token-wrapper" style="flex: 1;">
                            <span class="token-display" id="res_token"></span>
                            <button class="toggle-btn" onclick="toggleToken()" id="token_toggle">显示</button>
                        </span>
                        <button class="copy-btn" onclick="copyText('res_token')">复制</button>
                    </span>
                </div>
                <button class="btn btn-secondary" onclick="resetForm()">🔄 重新注册</button>
            </div>

            <div class="device-info">
                💡 每次注册都会使用新设备标识
            </div>
        </div>
    </div>

    <script>
        let sessionId = '';
        let pollInterval;
        let tokenHidden = true;
        let currentResult = null;

        // Radio button styling
        document.querySelectorAll('input[name="mode"]').forEach(radio => {
            radio.addEventListener('change', function() {
                document.querySelectorAll('.radio-item').forEach(item => {
                    item.classList.remove('selected');
                });
                this.parentElement.classList.add('selected');
            });
        });

        document.getElementById('registerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            startRegister();
        });

        function startRegister() {
            const config = {
                invite: document.getElementById('invite').value,
                pwd: document.getElementById('login_pwd').value || 'Xiangzi6681',
                mode: document.querySelector('input[name="mode"]:checked').value
            };

            document.getElementById('loading').style.display = 'block';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('result_card').style.display = 'none';
            document.getElementById('log_box').style.display = 'block';

            fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            }).then(r => r.json()).then(data => {
                if (data.success) {
                    sessionId = data.session_id;
                    pollInterval = setInterval(pollStatus, 500);
                } else {
                    showError(data.error);
                }
            }).catch(err => {
                showError('请求失败: ' + err);
            });
        }

        function pollStatus() {
            fetch('/api/status/' + sessionId).then(r => r.json()).then(data => {
                updateLogs(data.logs);
                
                if (data.done) {
                    clearInterval(pollInterval);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('submitBtn').disabled = false;
                    
                    if (data.success) {
                        showResult(data.result);
                    } else {
                        showError(data.error);
                    }
                }
            });
        }

        function updateLogs(logs) {
            const logBox = document.getElementById('log_box');
            logBox.innerHTML = logs.map(log => '<div class="log-entry">' + log + '</div>').join('');
            logBox.scrollTop = logBox.scrollHeight;
        }

        function showResult(result) {
            currentResult = result;
            tokenHidden = true;
            
            // 自动回填到登录输入框
            document.getElementById('login_email').value = result.email;
            document.getElementById('login_pwd').value = result.pwd;
            
            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.classList.remove('error');
            document.getElementById('result_title').textContent = '✅ 注册成功！';
            document.getElementById('res_email').textContent = result.email;
            document.getElementById('res_pwd').textContent = result.pwd;
            document.getElementById('res_free').textContent = result.free_time;
            document.getElementById('res_end').textContent = result.end_time;
            
            // Token默认隐藏
            document.getElementById('res_token').textContent = '••••••••••••••••••••';
            document.getElementById('token_toggle').textContent = '显示';
        }

        function showError(error) {
            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.classList.add('error');
            document.getElementById('result_title').textContent = '❌ 注册失败';
            document.getElementById('res_email').textContent = error;
            document.getElementById('res_pwd').textContent = '';
            document.getElementById('res_free').textContent = '';
            document.getElementById('res_end').textContent = '';
            document.getElementById('res_token').textContent = '';
        }

        function toggleToken() {
            const tokenEl = document.getElementById('res_token');
            const toggleBtn = document.getElementById('token_toggle');
            if (tokenHidden && currentResult) {
                tokenEl.textContent = currentResult.token;
                toggleBtn.textContent = '隐藏';
            } else {
                tokenEl.textContent = '••••••••••••••••••••';
                toggleBtn.textContent = '显示';
            }
            tokenHidden = !tokenHidden;
        }

        function copyText(elementId) {
            let text = '';
            if (elementId === 'res_token' && tokenHidden && currentResult) {
                text = currentResult.token;
            } else {
                text = document.getElementById(elementId).textContent;
            }
            
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const original = btn.textContent;
                btn.textContent = '已复制!';
                setTimeout(() => {
                    btn.textContent = original;
                }, 1500);
            }).catch(err => {
                alert('复制失败: ' + err);
            });
        }

        function resetForm() {
            document.getElementById('result_card').style.display = 'none';
            document.getElementById('log_box').style.display = 'none';
            document.getElementById('log_box').innerHTML = '';
            currentResult = null;
            tokenHidden = true;
        }
    </script>
</body>
</html>
'''

class JumperRegister:
    def __init__(self):
        pass

    def log(self, msg, logs):
        ts = datetime.now().strftime('%H:%M:%S')
        line = f'[{ts}] {msg}'
        logs.append(line)

    def md5(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def make_sign(self, path):
        return hmac.new(SIGN_KEY.encode(), path.encode(), hashlib.sha256).hexdigest()

    def api_call(self, path, method='GET', body=None, token=None, imei=None, mode='ios'):
        url = BASE + path.lstrip('/')
        sign = self.make_sign('/v1/' + path.lstrip('/'))
        data = json.dumps(body).encode('utf-8') if body else None
        req = urllib.request.Request(url, data=data, method=method)

        req.add_header('app-id', '2')
        req.add_header('version', '1.0.8')
        req.add_header('buildNumber', '3')
        req.add_header('x-sign', sign)
        req.add_header('Accept', '*/*')

        if mode == 'ios':
            req.add_header('os', 'ios')
            req.add_header('Content-Language', 'en-us')
            req.add_header('User-Agent',
                'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2')
            req.add_header('Accept-Language', 'zh-Hans-CN;q=1.0')
            req.add_header('Accept-Encoding', 'br;q=1.0, gzip;q=0.9, deflate;q=0.8')
        else:
            req.add_header('os', 'windows')
            req.add_header('Content-Language', 'zh-cn')
            req.add_header('User-Agent', 'JumperVPN/1.0.8')

        if imei:
            req.add_header('imei', imei.strip('{}'))
            req.add_header('device-name', PC_NAME)
        if token:
            req.add_header('j-token', token)
        if data:
            req.add_header('Content-Type', 'application/json')

        try:
            resp = opener.open(req, timeout=15)
            raw = resp.read()
            try: raw = __import__('gzip').decompress(raw)
            except: pass
            return json.loads(raw.decode('utf-8'))
        except urllib.error.HTTPError as e:
            raw = e.read()
            try: raw = __import__('gzip').decompress(raw)
            except: pass
            try: return json.loads(raw.decode('utf-8'))
            except: return {'code': e.code, 'msg': raw.decode('utf-8','replace')[:200]}
        except Exception as e:
            return {'code': -1, 'msg': str(e)[:200]}

    def http_get(self, url, headers=None):
        req = urllib.request.Request(url)
        if headers:
            for k, v in headers.items(): req.add_header(k, v)
        resp = opener.open(req, timeout=10)
        return json.loads(resp.read().decode('utf-8'))

    def http_post(self, url, body, headers=None):
        data = json.dumps(body).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items(): req.add_header(k, v)
        resp = opener.open(req, timeout=10)
        return json.loads(resp.read().decode('utf-8'))

    def create_temp_email(self, logs):
        self.log('创建临时邮箱 ...', logs)
        try:
            domains = self.http_get(f'{MAIL_TM}/domains')
            if isinstance(domains, list):
                domain = domains[0].get('domain', 'deltajohnsons.com')
            else:
                domain = domains.get('hydra:member', [{}])[0].get('domain', 'deltajohnsons.com')

            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email = f'{username}@{domain}'
            mail_pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

            self.http_post(f'{MAIL_TM}/accounts', {'address': email, 'password': mail_pwd})
            self.log(f'邮箱: {email}', logs)
        except urllib.error.HTTPError as e:
            err = e.read().decode('utf-8','replace')[:200]
            self.log(f'❌ 创建邮箱失败: {err}', logs)
            return None, None, None

        try:
            token_result = self.http_post(f'{MAIL_TM}/token', {'address': email, 'password': mail_pwd})
            mail_token = token_result.get('token', '')
            if not mail_token:
                self.log('❌ mail token 获取失败', logs)
                return None, None, None
        except urllib.error.HTTPError as e:
            self.log(f'❌ mail token 失败: {e.read().decode("utf-8","replace")[:200]}', logs)
            return None, None, None

        return email, mail_pwd, mail_token

    def wait_for_code(self, mail_token, logs, max_wait=90):
        self.log(f'等待验证码 (最多{max_wait}秒)...', logs)
        start = time.time()
        while time.time() - start < max_wait:
            try:
                messages = self.http_get(f'{MAIL_TM}/messages',
                    headers={'Authorization': f'Bearer {mail_token}'})
                msg_list = messages.get('hydra:member', []) if isinstance(messages, dict) else messages
                for msg in msg_list:
                    msg_id = msg.get('id', '')
                    if not msg_id: continue
                    detail = self.http_get(f'{MAIL_TM}/messages/{msg_id}',
                        headers={'Authorization': f'Bearer {mail_token}'})
                    body_text = detail.get('text', '') or detail.get('html', '') or ''
                    match = re.search(r'(?:验证码|code|Code|CODE)[：:\s]*(\d{4,6})', body_text)
                    if not match:
                        match = re.search(r'\b(\d{4,6})\b', body_text)
                    if match:
                        code = match.group(1)
                        self.log(f'✅ 验证码: {code}', logs)
                        return code
            except: pass
            time.sleep(3)
        self.log('❌ 等待验证码超时', logs)
        return None

    def register(self, config, session_data):
        logs = session_data['logs']
        try:
            self.log('[1/6] device/init ...', logs)
            imei = '{' + str(uuid.uuid4()).upper() + '}'
            result = self.api_call('device/init', imei=imei, mode=config['mode'])
            if result.get('code') != 200:
                self.log(f'❌ device/init 失败: {result}', logs)
                session_data['done'] = True
                session_data['success'] = False
                session_data['error'] = 'device/init 失败'
                return
            device_token = result['data']['user_info']['token']
            self.log(f'✅ device token OK', logs)

            self.log('[2/6] 创建临时邮箱 ...', logs)
            email, mail_pwd, mail_token = self.create_temp_email(logs)
            if not email:
                session_data['done'] = True
                session_data['success'] = False
                session_data['error'] = '创建邮箱失败'
                return

            self.log(f'[3/6] 发送验证码 → {email} ...', logs)
            result = self.api_call('user/send_email_code', method='POST',
                                  body={'email': email, 'type': 10},
                                  token=device_token, imei=imei, mode=config['mode'])
            if result.get('code') not in (200, 0):
                self.log(f'❌ 发送失败: {result}', logs)
                session_data['done'] = True
                session_data['success'] = False
                session_data['error'] = '发送验证码失败'
                return
            self.log('✅ 验证码已发送', logs)

            self.log('[4/6] 等待验证码 ...', logs)
            code = self.wait_for_code(mail_token, logs)
            if not code:
                session_data['done'] = True
                session_data['success'] = False
                session_data['error'] = '等待验证码超时'
                return

            pwd_raw = config['pwd']
            pwd_md5 = self.md5(pwd_raw)
            invite = config['invite']
            self.log(f'[5/6] 注册 ({email}) ...', logs)

            reg_pwd = None
            reg_result = None
            for pwd_attempt, label in [(pwd_md5, 'MD5'), (pwd_raw, '明文')]:
                result = self.api_call('user/signup', method='POST',
                                      body={'email': email, 'password': pwd_attempt,
                                            'repassword': pwd_attempt, 'code': code,
                                            'invite_code': invite},
                                      token=device_token, imei=imei, mode=config['mode'])
                if result.get('code') in (200, 0):
                    reg_pwd = pwd_attempt
                    reg_result = result
                    self.log(f'  ✅ 注册成功 (密码格式: {label})', logs)
                    break
                self.log(f'  {label}失败: {result.get("message","")}', logs)
            if not reg_pwd:
                self.log('❌ 两种密码格式都注册失败', logs)
                session_data['done'] = True
                session_data['success'] = False
                session_data['error'] = '注册失败'
                return

            data = reg_result.get('data', {})
            reg_user = data.get('user_info', {})
            free = reg_user.get('free_remaining_time', 0)
            end = reg_user.get('free_end_time', '')
            h, m = free // 3600, (free % 3600) // 60
            free_time = f'{h}小时{m}分'
            self.log(f'✅ 注册成功! {free_time} | 到期: {end}', logs)

            self.log('[6/6] 获取登录Token ...', logs)
            login_token = None
            for pwd_attempt, label in [(pwd_md5, 'MD5'), (pwd_raw, '明文')]:
                login_result = self.api_call('user/signin', method='POST',
                                            body={'email': email, 'password': pwd_attempt},
                                            token=device_token, imei=imei, mode=config['mode'])
                if login_result.get('code') in (200, 0):
                    login_token = login_result.get('data', {}).get('user_info', {}).get('token', '')
                    if login_token:
                        self.log(f'  ✅ 登录成功 (密码格式: {label})', logs)
                        break
            if not login_token:
                login_token = reg_user.get('token', device_token)
                self.log('  ⚠ 登录失败，用注册 token', logs)

            session_data['done'] = True
            session_data['success'] = True
            session_data['result'] = {
                'email': email,
                'pwd': pwd_raw,
                'free_time': free_time,
                'end_time': end,
                'token': login_token
            }

        except Exception as e:
            self.log(f'❌ 异常: {e}', logs)
            import traceback
            self.log(traceback.format_exc()[:500], logs)
            session_data['done'] = True
            session_data['success'] = False
            session_data['error'] = str(e)

jumper = JumperRegister()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def api_register():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'logs': [],
        'done': False,
        'success': False,
        'error': None,
        'result': None
    }
    config = request.json
    threading.Thread(target=jumper.register, args=(config, sessions[session_id]), daemon=True).start()
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/api/status/<session_id>')
def api_status(session_id):
    session_data = sessions.get(session_id, {
        'logs': [],
        'done': True,
        'success': False,
        'error': 'Session not found',
        'result': None
    })
    return jsonify({
        'logs': session_data['logs'],
        'done': session_data['done'],
        'success': session_data.get('success', False),
        'error': session_data.get('error'),
        'result': session_data.get('result')
    })

if __name__ == '__main__':
    print('JumperVPN 注册器启动中...')
    print('请在浏览器中访问: http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
