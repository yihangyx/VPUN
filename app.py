#!/usr/bin/env python3

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
    <title>Jumper 注册工具</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }

        .card {
            width: 100%;
            max-width: 520px;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card-header {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 30px 24px;
            text-align: center;
        }

        .card-header h1 {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .card-header p {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 400;
        }

        .card-body {
            padding: 30px 28px;
        }

        .form-group {
            margin-bottom: 22px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 15px;
            color: #1e293b;
        }

        .form-input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            font-size: 15px;
            transition: all 0.25s ease;
            background: #fafbfc;
        }

        .form-input:focus {
            outline: none;
            border-color: #3b82f6;
            background: white;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15);
        }

        .radio-group {
            display: flex;
            gap: 12px;
            margin-top: 6px;
        }

        .radio-item {
            flex: 1;
            padding: 14px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: #fafbfc;
        }

        .radio-item:hover {
            border-color: #cbd5e1;
        }

        .radio-item.active {
            border-color: #3b82f6;
            background: #eff6ff;
            color: #1d4ed8;
        }

        .radio-item input {
            display: none;
        }

        .btn {
            width: 100%;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .btn-secondary {
            background: #f1f5f9;
            color: #334155;
            margin-top: 12px;
        }

        .btn-secondary:hover {
            background: #e2e8f0;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 30px 0;
        }

        .spinner {
            width: 44px;
            height: 44px;
            border: 4px solid #f1f5f9;
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 16px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .log-box {
            display: none;
            margin-top: 24px;
            background: #0f172a;
            color: #10b981;
            padding: 18px;
            border-radius: 12px;
            font-family: Consolas, monospace;
            font-size: 13px;
            max-height: 280px;
            overflow-y: auto;
            line-height: 1.6;
        }

        .log-entry {
            margin-bottom: 4px;
        }

        .result {
            display: none;
            margin-top: 24px;
            padding: 22px;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            animation: slideUp 0.3s ease;
        }

        .result.success {
            border-color: #10b981;
            background: #f0fdf4;
        }

        .result.error {
            border-color: #ef4444;
            background: #fef2f2;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-title {
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .info-row {
            margin-bottom: 14px;
        }

        .info-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        .info-value {
            font-size: 15px;
            font-weight: 500;
            color: #1e293b;
            word-break: break-all;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }

        .copy-btn {
            padding: 6px 10px;
            background: #f1f5f9;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            color: #334155;
            cursor: pointer;
            transition: 0.2s;
        }

        .copy-btn:hover {
            background: #e2e8f0;
        }

        .token-display {
            flex: 1;
            padding-right: 8px;
        }

        .toggle-btn {
            background: none;
            border: none;
            color: #3b82f6;
            font-size: 13px;
            cursor: pointer;
            padding: 0 8px;
        }
    </style>
</head>

<body>
    <div class="card">
        <div class="card-header">
            <h1>🚀 Jumper 注册工具</h1>
            <p>一键注册 · 自动获取Token</p>
        </div>

        <div class="card-body">
            <form id="registerForm">
                <div class="form-group">
                    <div class="form-label">📧 邮箱</div>
                    <input type="text" id="login_email" class="form-input" placeholder="自动生成" readonly>
                </div>

                <div class="form-group">
                    <div class="form-label">🔐 密码</div>
                    <input type="text" id="login_pwd" class="form-input" placeholder="自动生成" readonly>
                </div>

                <div class="form-group">
                    <div class="form-label">🎫 邀请码</div>
                    <input type="text" id="invite" class="form-input" value="9QGE5V" placeholder="请输入邀请码">
                </div>

                <div class="form-group">
                    <div class="form-label">⚙️ 设备模式</div>
                    <div class="radio-group">
                        <label class="radio-item active">
                            <input type="radio" name="mode" value="ios" checked> iOS
                        </label>
                        <label class="radio-item">
                            <input type="radio" name="mode" value="windows"> Windows
                        </label>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary" id="submitBtn">✨ 开始注册</button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在处理中，请稍候...</p>
            </div>

            <div class="log-box" id="log_box"></div>

            <div class="result" id="result_card">
                <div class="result-title" id="result_title">✅ 注册成功</div>

                <div class="info-row">
                    <div class="info-label">邮箱</div>
                    <div class="info-value">
                        <span id="res_email"></span>
                        <button class="copy-btn" onclick="copyText('res_email')">复制</button>
                    </div>
                </div>

                <div class="info-row">
                    <div class="info-label">密码</div>
                    <div class="info-value">
                        <span id="res_pwd"></span>
                        <button class="copy-btn" onclick="copyText('res_pwd')">复制</button>
                    </div>
                </div>

                <div class="info-row">
                    <div class="info-label">免费时长</div>
                    <div class="info-value" id="res_free"></div>
                </div>

                <div class="info-row">
                    <div class="info-label">到期时间</div>
                    <div class="info-value" id="res_end"></div>
                </div>

                <div class="info-row">
                    <div class="info-label">JWT Token</div>
                    <div class="info-value">
                        <span class="token-display" id="res_token">••••••••••••</span>
                        <button class="toggle-btn" onclick="toggleToken()">显示</button>
                        <button class="copy-btn" onclick="copyText('res_token')">复制</button>
                    </div>
                </div>

                <button class="btn btn-secondary" onclick="resetForm()">🔄 重新注册</button>
            </div>
        </div>
    </div>

    <script>
        let sessionId = '';
        let pollInterval;
        let tokenHidden = true;
        let currentResult = null;

        document.querySelectorAll('.radio-item').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.radio-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                item.querySelector('input').checked = true;
            });
        });

        document.getElementById('registerForm').addEventListener('submit', e => {
            e.preventDefault();
            startRegister();
        });

        function startRegister() {
            const config = {
                invite: document.getElementById('invite').value.trim(),
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
                    showError(data.error || '请求失败');
                }
            }).catch(err => {
                showError('网络错误：' + err.message);
            });
        }

        function pollStatus() {
            fetch('/api/status/' + sessionId)
                .then(r => r.json())
                .then(data => {
                    updateLogs(data.logs);
                    if (data.done) {
                        clearInterval(pollInterval);
                        document.getElementById('loading').style.display = 'none';
                        document.getElementById('submitBtn').disabled = false;
                        data.success ? showResult(data.result) : showError(data.error);
                    }
                });
        }

        function updateLogs(logs) {
            const box = document.getElementById('log_box');
            box.innerHTML = logs.map(l => `<div class="log-entry">${l}</div>`).join('');
            box.scrollTop = box.scrollHeight;
        }

        function showResult(result) {
            currentResult = result;
            tokenHidden = true;
            document.getElementById('login_email').value = result.email;
            document.getElementById('login_pwd').value = result.pwd;
            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.className = 'result success';
            document.getElementById('result_title').innerHTML = '✅ 注册成功';
            document.getElementById('res_email').textContent = result.email;
            document.getElementById('res_pwd').textContent = result.pwd;
            document.getElementById('res_free').textContent = result.free_time;
            document.getElementById('res_end').textContent = result.end_time;
            document.getElementById('res_token').textContent = '••••••••••••';
        }

        function showError(msg) {
            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.className = 'result error';
            document.getElementById('result_title').innerHTML = '❌ 注册失败';
            document.getElementById('res_email').textContent = msg;
            document.getElementById('res_pwd').textContent = '';
            document.getElementById('res_free').textContent = '';
            document.getElementById('res_end').textContent = '';
            document.getElementById('res_token').textContent = '';
        }

        function toggleToken() {
            if (!currentResult) return;
            const el = document.getElementById('res_token');
            const btn = document.querySelector('.toggle-btn');
            if (tokenHidden) {
                el.textContent = currentResult.token;
                btn.textContent = '隐藏';
            } else {
                el.textContent = '••••••••••••';
                btn.textContent = '显示';
            }
            tokenHidden = !tokenHidden;
        }

        function copyText(id) {
            let text = id === 'res_token' && tokenHidden ? currentResult?.token || '' : document.getElementById(id).textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const ori = btn.textContent;
                btn.textContent = '已复制';
                setTimeout(() => btn.textContent = ori, 1500);
            });
        }

        function resetForm() {
            document.getElementById('result_card').style.display = 'none';
            document.getElementById('log_box').style.display = 'none';
            currentResult = null;
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
    print('注册器启动中...')
    print('请在浏览器中访问: http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
