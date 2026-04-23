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

        /* 加载 */
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

        /* 日志 */
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

        /* 结果卡片 */
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

        .result-success .result-title {
            color: #166534;
        }

        .result-error .result-title {
            color: #991b1b;
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

            <!-- 加载 -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在处理中，请稍候...</p>
            </div>

            <!-- 日志 -->
            <div class="log-box" id="log_box"></div>

            <!-- 结果 -->
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

        // 单选切换
        document.querySelectorAll('.radio-item').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.radio-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                item.querySelector('input').checked = true;
            });
        });

        // 提交
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
