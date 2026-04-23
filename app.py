<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>奕涵 · JumperVPN 极速注册助手</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif;
            background: radial-gradient(circle at 10% 20%, rgba(15, 25, 45, 0.96), rgba(8, 12, 24, 0.98)),
                        repeating-linear-gradient(45deg, rgba(255,255,255,0.01) 0px, rgba(255,255,255,0.01) 2px, transparent 2px, transparent 8px);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            position: relative;
        }

        /* 动态光晕背景 */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.05) 50%, transparent 80%);
            animation: aurora 18s infinite alternate;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes aurora {
            0% { opacity: 0.4; transform: translate(0%, 0%) rotate(0deg);}
            100% { opacity: 1; transform: translate(5%, 5%) rotate(2deg);}
        }

        .glass-card {
            max-width: 580px;
            width: 100%;
            background: rgba(20, 28, 40, 0.75);
            backdrop-filter: blur(18px);
            border-radius: 48px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 30px 50px rgba(0,0,0,0.5), 0 0 0 0.5px rgba(255,255,255,0.1) inset;
            overflow: hidden;
            transition: all 0.3s ease;
            z-index: 2;
        }

        .card-header {
            background: linear-gradient(135deg, rgba(102,126,234,0.9) 0%, rgba(118,75,162,0.9) 100%);
            padding: 32px 28px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }

        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(4px);
            padding: 6px 14px;
            border-radius: 60px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
            color: white;
        }

        .card-header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            color: white;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .card-header h1 i {
            font-size: 2rem;
            filter: drop-shadow(0 2px 6px rgba(0,0,0,0.2));
        }

        .card-header p {
            color: rgba(255,255,255,0.85);
            margin-top: 12px;
            font-weight: 500;
            font-size: 0.9rem;
        }

        .card-body {
            padding: 28px 28px 32px;
        }

        .input-group {
            margin-bottom: 22px;
        }

        .input-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            color: #cdd9ff;
            margin-bottom: 8px;
            letter-spacing: 0.3px;
        }

        .input-label i {
            width: 20px;
            font-size: 0.9rem;
            color: #8b9eff;
        }

        .input-field {
            width: 100%;
            background: rgba(10, 15, 28, 0.7);
            border: 1.5px solid rgba(255,255,255,0.15);
            border-radius: 24px;
            padding: 14px 18px;
            font-size: 0.95rem;
            font-weight: 500;
            color: #f0f3ff;
            transition: all 0.25s;
            font-family: inherit;
        }

        .input-field:focus {
            outline: none;
            border-color: #8b9eff;
            background: rgba(15, 22, 40, 0.9);
            box-shadow: 0 0 0 4px rgba(139, 158, 255, 0.2);
        }

        .radio-container {
            display: flex;
            gap: 16px;
            margin-top: 8px;
        }

        .radio-option {
            flex: 1;
            background: rgba(10, 15, 28, 0.6);
            border: 1.5px solid rgba(255,255,255,0.1);
            border-radius: 28px;
            padding: 10px 0;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-weight: 600;
            color: #b9c7ff;
        }

        .radio-option i {
            font-size: 1rem;
        }

        .radio-option.active {
            background: linear-gradient(120deg, #667eea, #764ba2);
            border-color: transparent;
            color: white;
            box-shadow: 0 6px 14px rgba(102,126,234,0.4);
        }

        input[type="radio"] {
            display: none;
        }

        .btn-glow {
            width: 100%;
            background: linear-gradient(95deg, #667eea, #a777e3);
            border: none;
            padding: 16px;
            border-radius: 48px;
            font-weight: 700;
            font-size: 1rem;
            color: white;
            margin-top: 12px;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 8px 20px rgba(102,126,234,0.3);
        }

        .btn-glow:disabled {
            opacity: 0.55;
            transform: scale(0.98);
            cursor: not-allowed;
        }

        .btn-glow:active:not(:disabled) {
            transform: scale(0.97);
        }

        .log-console {
            background: #0a0e18;
            border-radius: 28px;
            margin-top: 24px;
            padding: 8px 0;
            border: 1px solid rgba(255,255,255,0.08);
            display: none;
            overflow: hidden;
        }

        .log-header {
            padding: 12px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.75rem;
            font-weight: 600;
            color: #8b9eff;
            letter-spacing: 1px;
        }

        .log-content {
            height: 240px;
            overflow-y: auto;
            padding: 12px 16px;
            font-family: 'JetBrains Mono', 'SF Mono', monospace;
            font-size: 0.75rem;
            line-height: 1.6;
            color: #a2f5d0;
        }

        .log-content div {
            margin-bottom: 6px;
            border-left: 2px solid #2a3a6e;
            padding-left: 12px;
            opacity: 0.9;
        }

        .result-card {
            margin-top: 28px;
            background: rgba(16, 24, 36, 0.8);
            border-radius: 32px;
            padding: 20px;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(102,126,234,0.4);
            display: none;
            animation: fadeUp 0.4s ease;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 800;
            font-size: 1.2rem;
            color: #6ef0b0;
            margin-bottom: 18px;
        }

        .info-row {
            background: rgba(0,0,0,0.35);
            border-radius: 24px;
            padding: 12px 16px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }

        .info-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            color: #9aa9cf;
        }

        .info-value {
            font-family: monospace;
            font-weight: 600;
            word-break: break-all;
            color: #f0f3ff;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .copy-badge {
            background: #2a3a6e;
            border-radius: 40px;
            padding: 4px 12px;
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.2s;
            font-weight: 500;
        }

        .copy-badge:hover {
            background: #4c6eb0;
        }

        .token-toggle {
            background: none;
            border: 1px solid #4c6eb0;
            border-radius: 30px;
            padding: 4px 12px;
            font-size: 0.7rem;
            cursor: pointer;
            color: #bbd1ff;
        }

        .btn-reset {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.2);
            width: 100%;
            margin-top: 12px;
            border-radius: 40px;
            padding: 12px;
            font-weight: 600;
            color: #cfdcff;
            transition: 0.2s;
        }

        .loader {
            display: none;
            text-align: center;
            margin: 24px 0;
        }

        .spinner-circle {
            width: 48px;
            height: 48px;
            border: 4px solid rgba(102,126,234,0.2);
            border-top: 4px solid #a777e3;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 16px;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .error-header {
            color: #ffb4a2;
        }

        ::-webkit-scrollbar {
            width: 5px;
        }
        ::-webkit-scrollbar-track {
            background: #11161f;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #4c6eb0;
            border-radius: 10px;
        }

        @media (max-width: 520px) {
            .glass-card { border-radius: 32px; }
            .card-body { padding: 20px; }
            .info-value { font-size: 0.75rem; }
        }
    </style>
</head>
<body>

<div class="glass-card">
    <div class="card-header">
        <div class="badge"><i class="fas fa-bolt"></i> 一键智能注册 · 极速隧道</div>
        <h1><i class="fas fa-shield-alt"></i> JumperVPN <span style="font-weight: 500;">奕涵</span></h1>
        <p>临时邮箱 + 自动验证码 · 永久免费试用流</p>
    </div>
    <div class="card-body">
        <div class="input-group">
            <div class="input-label"><i class="fas fa-envelope"></i> 邮箱 (自动生成)</div>
            <input type="text" id="displayEmail" class="input-field" placeholder="注册后自动填充" readonly style="background: #0a0f1c; color:#9aa9cf;">
        </div>
        <div class="input-group">
            <div class="input-label"><i class="fas fa-lock"></i> 密码</div>
            <input type="text" id="userPwd" class="input-field" placeholder="留空使用默认密码 (Xiangzi6681)" value="Xiangzi6681">
        </div>
        <div class="input-group">
            <div class="input-label"><i class="fas fa-ticket-alt"></i> 邀请码</div>
            <input type="text" id="inviteCode" class="input-field" value="9QGE5V" placeholder="推荐码">
        </div>
        <div class="input-group">
            <div class="input-label"><i class="fas fa-mobile-alt"></i> 设备模式</div>
            <div class="radio-container">
                <label class="radio-option" id="radioIos">
                    <i class="fab fa-apple"></i> iOS
                    <input type="radio" name="deviceMode" value="ios" checked>
                </label>
                <label class="radio-option" id="radioWin">
                    <i class="fab fa-windows"></i> Windows
                    <input type="radio" name="deviceMode" value="windows">
                </label>
            </div>
        </div>
        <button class="btn-glow" id="startBtn"><i class="fas fa-rocket"></i> 极速注册</button>

        <div class="loader" id="loaderArea">
            <div class="spinner-circle"></div>
            <p style="color:#b9c7ff; font-size:0.8rem;">正在穿越云层 · 获取账号中</p>
        </div>

        <div class="log-console" id="logConsole">
            <div class="log-header"><i class="fas fa-terminal"></i> 实时日志流</div>
            <div class="log-content" id="logContent"></div>
        </div>

        <div class="result-card" id="resultCard">
            <div class="result-header" id="resultHeader">
                <i class="fas fa-check-circle"></i> <span id="resultTitle">注册成功</span>
            </div>
            <div class="info-row">
                <span class="info-label">📧 邮箱</span>
                <span class="info-value"><span id="resEmail"></span> <span class="copy-badge" data-copy="email">复制</span></span>
            </div>
            <div class="info-row">
                <span class="info-label">🔑 密码</span>
                <span class="info-value"><span id="resPwd"></span> <span class="copy-badge" data-copy="pwd">复制</span></span>
            </div>
            <div class="info-row">
                <span class="info-label">⏱️ 免费时长</span>
                <span class="info-value"><span id="resFree"></span></span>
            </div>
            <div class="info-row">
                <span class="info-label">📅 到期时间</span>
                <span class="info-value"><span id="resEnd"></span></span>
            </div>
            <div class="info-row">
                <span class="info-label">🎫 JWT Token</span>
                <div class="info-value" style="flex-direction: column; align-items: flex-start;">
                    <div style="display: flex; gap: 10px; flex-wrap: wrap; width: 100%;">
                        <span id="resToken" style="font-family: monospace; word-break: break-all;">••••••••</span>
                        <button class="token-toggle" id="toggleTokenBtn">显示</button>
                        <span class="copy-badge" data-copy="token">复制Token</span>
                    </div>
                </div>
            </div>
            <button class="btn-reset" id="resetBtn"><i class="fas fa-sync-alt"></i> 重新注册</button>
        </div>
    </div>
</div>

<script>
    // 交互增强 & 轮询逻辑
    let currentSessionId = null;
    let pollInterval = null;
    let currentTokenHidden = true;
    let latestResultData = null;

    // 选择样式联动
    const radioIos = document.getElementById('radioIos');
    const radioWin = document.getElementById('radioWin');
    const iosRadioInput = document.querySelector('input[value="ios"]');
    const winRadioInput = document.querySelector('input[value="windows"]');

    function updateRadioUI() {
        if(iosRadioInput.checked) {
            radioIos.classList.add('active');
            radioWin.classList.remove('active');
        } else {
            radioWin.classList.add('active');
            radioIos.classList.remove('active');
        }
    }
    iosRadioInput.addEventListener('change', updateRadioUI);
    winRadioInput.addEventListener('change', updateRadioUI);
    updateRadioUI();

    // UI helpers
    const startBtn = document.getElementById('startBtn');
    const loaderArea = document.getElementById('loaderArea');
    const logConsole = document.getElementById('logConsole');
    const logContent = document.getElementById('logContent');
    const resultCard = document.getElementById('resultCard');
    const resEmailSpan = document.getElementById('resEmail');
    const resPwdSpan = document.getElementById('resPwd');
    const resFreeSpan = document.getElementById('resFree');
    const resEndSpan = document.getElementById('resEnd');
    const resTokenSpan = document.getElementById('resToken');
    const toggleTokenBtn = document.getElementById('toggleTokenBtn');
    const resetBtn = document.getElementById('resetBtn');
    const displayEmailField = document.getElementById('displayEmail');
    const userPwdInput = document.getElementById('userPwd');
    const inviteInput = document.getElementById('inviteCode');

    function addLog(msg) {
        const div = document.createElement('div');
        div.textContent = msg;
        logContent.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function clearLogs() {
        logContent.innerHTML = '';
    }

    function stopPolling() {
        if(pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
    }

    function resetUI() {
        stopPolling();
        currentSessionId = null;
        latestResultData = null;
        resultCard.style.display = 'none';
        logConsole.style.display = 'none';
        loaderArea.style.display = 'none';
        startBtn.disabled = false;
        currentTokenHidden = true;
        resTokenSpan.textContent = '••••••••';
        toggleTokenBtn.textContent = '显示';
        displayEmailField.value = '';
        clearLogs();
    }

    function showErrorResult(errMsg) {
        resultCard.style.display = 'block';
        document.getElementById('resultHeader').innerHTML = '<i class="fas fa-times-circle"></i>';
        document.getElementById('resultTitle').textContent = '注册失败';
        document.getElementById('resultHeader').style.color = '#ffb4a2';
        resEmailSpan.textContent = errMsg;
        resPwdSpan.textContent = '—';
        resFreeSpan.textContent = '—';
        resEndSpan.textContent = '—';
        resTokenSpan.textContent = '—';
        latestResultData = null;
    }

    function showSuccessResult(data) {
        resultCard.style.display = 'block';
        document.getElementById('resultHeader').innerHTML = '<i class="fas fa-check-circle"></i>';
        document.getElementById('resultTitle').textContent = '注册成功 🎉';
        document.getElementById('resultHeader').style.color = '#6ef0b0';
        resEmailSpan.textContent = data.email;
        resPwdSpan.textContent = data.pwd;
        resFreeSpan.textContent = data.free_time;
        resEndSpan.textContent = data.end_time;
        latestResultData = data;
        currentTokenHidden = true;
        resTokenSpan.textContent = '••••••••••••••••••••';
        toggleTokenBtn.textContent = '显示';
        displayEmailField.value = data.email;
        // 密码回填到输入框（便于手动）
        if(userPwdInput.value === 'Xiangzi6681' || userPwdInput.value === '') {
            userPwdInput.value = data.pwd;
        }
    }

    function pollStatus(sessionId) {
        fetch(`/api/status/${sessionId}`)
            .then(res => res.json())
            .then(data => {
                // 刷新日志
                if(data.logs && data.logs.length) {
                    clearLogs();
                    data.logs.forEach(line => addLog(line));
                }
                if(data.done) {
                    stopPolling();
                    loaderArea.style.display = 'none';
                    startBtn.disabled = false;
                    if(data.success && data.result) {
                        showSuccessResult(data.result);
                    } else {
                        showErrorResult(data.error || '注册流程失败，请重试');
                    }
                } else {
                    // 继续轮询
                }
            })
            .catch(err => {
                console.error(err);
                stopPolling();
                loaderArea.style.display = 'none';
                startBtn.disabled = false;
                showErrorResult('状态查询失败: ' + err);
            });
    }

    startBtn.addEventListener('click', () => {
        if(startBtn.disabled) return;
        const pwd = userPwdInput.value.trim();
        const finalPwd = pwd === '' ? 'Xiangzi6681' : pwd;
        const invite = inviteInput.value.trim() || '9QGE5V';
        const mode = document.querySelector('input[name="deviceMode"]:checked').value;

        const payload = {
            pwd: finalPwd,
            invite: invite,
            mode: mode
        };

        resetUI();
        loaderArea.style.display = 'block';
        logConsole.style.display = 'block';
        startBtn.disabled = true;

        fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(r => r.json())
        .then(res => {
            if(res.success && res.session_id) {
                currentSessionId = res.session_id;
                pollInterval = setInterval(() => pollStatus(currentSessionId), 800);
            } else {
                throw new Error('无法初始化注册会话');
            }
        })
        .catch(err => {
            loaderArea.style.display = 'none';
            startBtn.disabled = false;
            logConsole.style.display = 'block';
            addLog(`❌ 请求失败: ${err.message}`);
            showErrorResult('网络错误，请稍后重试');
        });
    });

    // 复制功能 (通用)
    document.addEventListener('click', (e) => {
        if(e.target.classList.contains('copy-badge')) {
            const target = e.target.getAttribute('data-copy');
            let textToCopy = '';
            if(target === 'email' && latestResultData) textToCopy = latestResultData.email;
            else if(target === 'pwd' && latestResultData) textToCopy = latestResultData.pwd;
            else if(target === 'token') {
                if(latestResultData && latestResultData.token) {
                    textToCopy = latestResultData.token;
                } else textToCopy = '';
            }
            if(textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const original = e.target.innerText;
                    e.target.innerText = '已复制!';
                    setTimeout(() => { e.target.innerText = original; }, 1200);
                }).catch(() => alert('复制失败'));
            } else {
                alert('无有效内容');
            }
        }
    });

    toggleTokenBtn.addEventListener('click', () => {
        if(!latestResultData || !latestResultData.token) {
            alert('暂无Token数据');
            return;
        }
        if(currentTokenHidden) {
            resTokenSpan.textContent = latestResultData.token;
            toggleTokenBtn.textContent = '隐藏';
        } else {
            resTokenSpan.textContent = '••••••••••••••••••••';
            toggleTokenBtn.textContent = '显示';
        }
        currentTokenHidden = !currentTokenHidden;
    });

    resetBtn.addEventListener('click', () => {
        resetUI();
        resultCard.style.display = 'none';
        logConsole.style.display = 'none';
        displayEmailField.value = '';
        userPwdInput.value = 'Xiangzi6681';
        if(pollInterval) clearInterval(pollInterval);
        startBtn.disabled = false;
        latestResultData = null;
        currentTokenHidden = true;
    });
</script>
</body>
</html>
