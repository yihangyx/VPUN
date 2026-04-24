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
    <title>奕涵</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0F172A;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: #F8FAFC;
        }

        .card {
            background: #1E293B;
            border-radius: 20px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            border: 1px solid #334155;
        }

        .card-header {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            padding: 32px 24px;
            text-align: center;
        }

        .card-header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #fff;
        }

        .card-header p {
            font-size: 14px;
            opacity: 0.9;
            color: rgba(255, 255, 255, 0.9);
        }

        .card-body {
            padding: 32px 28px;
        }

        .form-group {
            margin-bottom: 24px;
        }

        .form-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
            font-size: 14px;
            color: #E2E8F0;
        }

        .form-input {
            width: 100%;
            padding: 14px 16px;
            background: #0F172A;
            border: 1px solid #475569;
            border-radius: 12px;
            font-size: 15px;
            color: #F8FAFC;
            transition: all 0.2s ease;
        }

        .form-input:focus {
            outline: none;
            border-color: #818CF8;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        .form-input::placeholder {
            color: #94A3B8;
        }

        .mode-group {
            display: flex;
            gap: 12px;
            margin-top: 8px;
        }

        .mode-item {
            flex: 1;
            padding: 14px;
            background: #0F172A;
            border: 1px solid #475569;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
            color: #CBD5E1;
        }

        .mode-item:hover {
            border-color: #64748B;
        }

        .mode-item.active {
            background: #4F46E5;
            border-color: #4F46E5;
            color: white;
        }

        .mode-item input {
            display: none;
        }

        .btn {
            width: 100%;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }

        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-secondary {
            background: #334155;
            color: #E2E8F0;
            margin-top: 12px;
        }

        .btn-secondary:hover {
            background: #475569;
        }

        /* 加载 */
        .loading {
            display: none;
            text-align: center;
            padding: 30px 0;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #334155;
            border-top-color: #818CF8;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 16px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* 日志 */
        .log-box {
            margin-top: 24px;
            background: #0F172A;
            border-radius: 12px;
            padding: 16px;
            height: 260px;
            overflow-y: auto;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            line-height: 1.6;
            color: #10B981;
            border: 1px solid #334155;
            display: none;
        }

        .log-entry {
            margin-bottom: 4px;
        }

        /* 结果卡片 */
        .result-card {
            margin-top: 24px;
            background: #1E293B;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #475569;
            display: none;
        }

        .result-success {
            border-color: #10B981;
            background: rgba(16, 185, 129, 0.05);
        }

        .result-error {
            border-color: #EF4444;
            background: rgba(239, 68, 68, 0.05);
        }

        .result-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .result-item {
            margin-bottom: 16px;
        }

        .result-label {
            font-size: 12px;
            color: #94A3B8;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-value {
            background: #0F172A;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px 14px;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            color: #F8FAFC;
            word-break: break-all;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .copy-btn {
            background: #4F46E5;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 11px;
            cursor: pointer;
            flex-shrink: 0;
            margin-left: 8px;
            transition: all 0.2s;
        }

        .copy-btn.copied {
            background: #10B981 !important;
        }

        /* 弹窗 */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.8);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 999;
            padding: 20px;
        }

        .modal.show {
            display: flex;
        }

        .modal-content {
            background: #1E293B;
            border-radius: 20px;
            width: 100%;
            max-width: 420px;
            padding: 32px;
            border: 1px solid #334155;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .modal-header {
            text-align: center;
            margin-bottom: 28px;
        }

        .modal-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #4F46E5, #7C3AED);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            font-size: 30px;
            color: white;
        }

        .modal-title {
            font-size: 22px;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 6px;
        }

        .modal-subtitle {
            color: #94A3B8;
            font-size: 14px;
        }

        .modal-item {
            margin-bottom: 18px;
        }

        .modal-item-label {
            font-size: 12px;
            color: #94A3B8;
            margin-bottom: 8px;
        }

        .modal-item-value {
            background: #0F172A;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 14px;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            color: #F8FAFC;
            word-break: break-all;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap:10px;
        }

        .modal-footer {
            display: flex;
            justify-content: center;
            margin-top: 28px;
        }

        .modal-btn-close {
            width:100%;
            padding: 14px;
            border-radius: 12px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            background: #334155;
            color: #E2E8F0;
        }

        .footer {
            text-align: center;
            margin-top: 24px;
            font-size: 12px;
            color: #64748B;
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="card-header">
            <h1>奕涵</h1>
            <p>一键自动注册 · 安全稳定</p>
        </div>

        <div class="card-body">
            <form id="registerForm">
                <div class="form-group">
                    <label class="form-label">📧 注册邮箱</label>
                    <input type="text" class="form-input" id="login_email" placeholder="自动生成" readonly>
                </div>

                <div class="form-group">
                    <label class="form-label">🔐 登录密码</label>
                    <input type="text" class="form-input" id="login_pwd" placeholder="自动生成" readonly>
                </div>

                <div class="form-group">
                    <label class="form-label">📱 设备模式</label>
                    <div class="mode-group">
                        <label class="mode-item active">
                            <input type="radio" name="mode" value="ios" checked> iOS
                        </label>
                        <label class="mode-item">
                            <input type="radio" name="mode" value="windows"> Windows
                        </label>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary" id="submitBtn">
                    🚀 开始自动注册
                </button>
            </form>

            <!-- 加载 -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在处理中，请稍候...</p>
            </div>

            <!-- 日志 -->
            <div class="log-box" id="log_box"></div>

            <!-- 结果 -->
            <div class="result-card" id="result_card">
                <div class="result-title" id="result_title">✅ 注册成功</div>

                <div class="result-item">
                    <div class="result-label">免费时长</div>
                    <div class="result-value" id="res_free"></div>
                </div>

                <div class="result-item">
                    <div class="result-label">到期时间</div>
                    <div class="result-value" id="res_end"></div>
                </div>

                <div class="result-item">
                    <div class="result-label">J-Token (登录凭证)</div>
                    <div class="result-value" id="res_token">
                        <span id="token_text"></span>
                        <button class="copy-btn" onclick="copyToken()">复制</button>
                    </div>
                </div>

                <button class="btn btn-secondary" onclick="resetForm()">🔄 重新注册</button>
            </div>

            <div class="footer">© 2026 奕涵 - 仅供学习使用</div>
        </div>
    </div>

    <!-- 成功弹窗 -->
    <div class="modal" id="successModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-icon">✅</div>
                <div class="modal-title">注册成功！</div>
                <div class="modal-subtitle">请妥善保存账号信息</div>
            </div>

            <div class="modal-item">
                <div class="modal-item-label">邮箱</div>
                <div class="modal-item-value">
                    <span id="modalEmailText"></span>
                    <button class="copy-btn" onclick="copyEmail()">复制</button>
                </div>
            </div>

            <div class="modal-item">
                <div class="modal-item-label">密码</div>
                <div class="modal-item-value">
                    <span id="modalPwdText"></span>
                    <button class="copy-btn" onclick="copyPwd()">复制</button>
                </div>
            </div>

            <div class="modal-footer">
                <button class="modal-btn-close" onclick="closeModal()">关闭</button>
            </div>
        </div>
    </div>

    <script>
        let sessionId = '';
        let pollInterval = null;
        let currentData = null;

        // 设备模式切换
        document.querySelectorAll('.mode-item').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.mode-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                item.querySelector('input').checked = true;
            });
        });

        // 表单提交
        document.getElementById('registerForm').addEventListener('submit', e => {
            e.preventDefault();
            startRegister();
        });

        // 生成密码
        function generatePassword() {
            const chars = 'ABCDEFGHJKLMNPQRSTWXYZabcdefghjkmnpqrstwxyz23456789';
            let pwd = '';
            for (let i = 0; i < 12; i++) {
                pwd += chars[Math.floor(Math.random() * chars.length)];
            }
            return pwd;
        }

        // 开始注册
        function startRegister() {
            const config = {
                pwd: generatePassword(),
                mode: document.querySelector('input[name="mode"]:checked').value
            };

            document.getElementById('loading').style.display = 'block';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('result_card').style.display = 'none';
            document.getElementById('log_box').style.display = 'block';
            document.getElementById('log_box').innerHTML = '';

            // 自动跳转到日志区域
            document.getElementById('log_box').scrollIntoView({ behavior: 'smooth', block: 'center' });

            fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    sessionId = data.session_id;
                    pollInterval = setInterval(pollStatus, 600);
                }
            });
        }

        // 轮询状态
        function pollStatus() {
            fetch(`/api/status/${sessionId}`)
            .then(res => res.json())
            .then(data => {
                updateLogs(data.logs);

                if (data.done) {
                    clearInterval(pollInterval);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('submitBtn').disabled = false;

                    if (data.success) {
                        showResult(data.result);
                        showModal(data.result);
                    } else {
                        showError(data.error);
                    }
                }
            });
        }

        // 更新日志
        function updateLogs(logs) {
            const box = document.getElementById('log_box');
            box.innerHTML = logs.map(l => `<div class="log-entry">${l}</div>`).join('');
            box.scrollTop = box.scrollHeight;
        }

        // 显示成功结果
        function showResult(result) {
            currentData = result;
            document.getElementById('login_email').value = result.email;
            document.getElementById('login_pwd').value = result.pwd;

            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.className = 'result-card result-success';
            document.getElementById('result_title').innerHTML = '✅ 注册成功';

            document.getElementById('res_free').innerText = result.free_time;
            document.getElementById('res_end').innerText = result.end_time;
            document.getElementById('token_text').innerText = result.token;
        }

        // 显示错误
        function showError(err) {
            const card = document.getElementById('result_card');
            card.style.display = 'block';
            card.className = 'result-card result-error';
            document.getElementById('result_title').innerHTML = '❌ 注册失败';
            document.getElementById('res_free').innerText = err;
            document.getElementById('res_end').innerText = '';
            document.getElementById('token_text').innerText = '';
        }

        // 弹窗
        function showModal(result) {
            document.getElementById('modalEmailText').innerText = result.email;
            document.getElementById('modalPwdText').innerText = result.pwd;
            document.getElementById('successModal').classList.add('show');
        }

        function closeModal() {
            document.getElementById('successModal').classList.remove('show');
        }

        // 复制通用效果
        function copyWithEffect(btn, text) {
            navigator.clipboard.writeText(text);
            btn.classList.add('copied');
            btn.innerText = "已复制";
            setTimeout(() => {
                btn.classList.remove('copied');
                btn.innerText = "复制";
            }, 1500);
        }

        // 单个复制
        function copyEmail(){
            let btn = event.currentTarget;
            let text = document.getElementById('modalEmailText').innerText;
            copyWithEffect(btn, text);
        }
        function copyPwd(){
            let btn = event.currentTarget;
            let text = document.getElementById('modalPwdText').innerText;
            copyWithEffect(btn, text);
        }
        function copyToken() {
            let btn = event.currentTarget;
            let text = document.getElementById('token_text').innerText;
            copyWithEffect(btn, text);
        }

        // 重置
        function resetForm() {
            document.getElementById('result_card').style.display = 'none';
            document.getElementById('log_box').style.display = 'none';
            document.getElementById('login_email').value = '';
            document.getElementById('login_pwd').value = '';
            currentData = null;
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
        req.add_header('x-sign', sign);
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
            self.log(f'[5/6] 注册 ({email}) ...', logs)
            self.log(f'密码: {pwd_raw}', logs)

            reg_pwd = None
            reg_result = None
            for pwd_attempt, label in [(pwd_md5, 'MD5'), (pwd_raw, '明文')]:
                result = self.api_call('user/signup', method='POST',
                                      body={'email': email, 'password': pwd_attempt,
                                            'repassword': pwd_attempt, 'code': code},
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
    print('奕涵 注册器启动中...')
    print('请在浏览器中访问: http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
