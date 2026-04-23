<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>奕涵 · JumperVPN 极光注册引擎</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Space Grotesk', 'Inter', system-ui, -apple-system, sans-serif;
            background: #0a0c15;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* 动态粒子背景 */
        body::before {
            content: '';
            position: fixed;
            width: 200%;
            height: 200%;
            top: -50%;
            left: -50%;
            background: radial-gradient(circle at 20% 40%, rgba(80, 70, 200, 0.2), rgba(0, 0, 0, 0.6));
            animation: slowDrift 28s infinite alternate;
            z-index: 0;
        }

        @keyframes slowDrift {
            0% { transform: translate(0%, 0%) rotate(0deg); }
            100% { transform: translate(5%, 8%) rotate(2deg); }
        }

        .nebula {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at 60% 30%, rgba(102,126,234,0.15), transparent 60%);
            pointer-events: none;
            z-index: 0;
        }

        .glass-orb {
            position: fixed;
            bottom: -100px;
            right: -80px;
            width: 380px;
            height: 380px;
            background: radial-gradient(circle, #764ba2, #2a1b4e);
            filter: blur(90px);
            opacity: 0.5;
            border-radius: 50%;
            z-index: 0;
        }

        .main-card {
            position: relative;
            z-index: 10;
            max-width: 580px;
            width: 100%;
            background: rgba(12, 18, 32, 0.68);
            backdrop-filter: blur(20px);
            border-radius: 56px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 40px 70px rgba(0, 0, 0, 0.6), 0 0 0 0.5px rgba(255, 255, 255, 0.1) inset;
            transition: transform 0.2s ease;
            overflow: hidden;
        }

        .accent-header {
            background: linear-gradient(105deg, rgba(102,126,234,0.9) 0%, rgba(148, 93, 214, 0.9) 100%);
            padding: 32px 28px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            padding: 5px 14px;
            border-radius: 60px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 1px;
            color: #eef5ff;
            margin-bottom: 16px;
        }

        .accent-header h1 {
            font-size: 2.3rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .accent-header p {
            color: rgba(255,255,255,0.85);
            font-size: 0.85rem;
            margin-top: 12px;
            font-weight: 500;
        }

        .form-panel {
            padding: 28px 26px 34px;
        }

        .input-row {
            margin-bottom: 22px;
        }

        .input-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #b9c8ff;
            margin-bottom: 8px;
            letter-spacing: 0.3px;
        }

        .input-label i {
            width: 20px;
            font-size: 0.9rem;
            color: #9b8cff;
        }

        .field {
            width: 100%;
            background: rgba(6, 10, 22, 0.7);
            border: 1.5px solid rgba(255,255,255,0.12);
            border-radius: 28px;
            padding: 14px 18px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #f0f3ff;
            font-family: inherit;
            transition: 0.2s;
        }

        .field:focus {
            outline: none;
            border-color: #8f9eff;
            background: rgba(10, 16, 30, 0.9);
            box-shadow: 0 0 0 3px rgba(143, 158, 255, 0.2);
        }

        .random-pwd-wrapper {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .random-pwd-wrapper .field {
            flex: 1;
        }

        .random-btn {
            background: #2a2f4b;
            border: none;
            border-radius: 40px;
            padding: 0 18px;
            height: 50px;
            font-weight: 600;
            color: #cddcff;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
        }

        .random-btn:hover {
            background: #3d4370;
            color: white;
        }

        .device-toggles {
            display: flex;
            gap: 14px;
            margin-top: 6px;
        }

        .device-opt {
            flex: 1;
            background: rgba(20, 28, 45, 0.7);
            border: 1.5px solid rgba(255,255,255,0.1);
            border-radius: 40px;
            padding: 12px 0;
            text-align: center;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-weight: 600;
            color: #b7c3e6;
            transition: all 0.2s;
        }

        .device-opt i {
            font-size: 1.1rem;
        }

        .device-opt.active {
            background: linear-gradient(115deg, #667eea, #9b6df5);
            border-color: transparent;
            color: white;
            box-shadow: 0 6px 14px rgba(102,126,234,0.35);
        }

        input[type="radio"] {
            display: none;
        }

        .glow-btn {
            width: 100%;
            background: linear-gradient(95deg, #5f6ef0, #b16cea);
            border: none;
            border-radius: 48px;
            padding: 16px;
            font-weight: 700;
            font-size: 1rem;
            color: white;
            margin-top: 18px;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 12px 25px -8px rgba(98, 91, 235, 0.5);
        }

        .glow-btn:disabled {
            opacity: 0.55;
            transform: scale(0.97);
            cursor: not-allowed;
        }

        .log-console {
            background: #03060ecc;
            border-radius: 32px;
            margin-top: 28px;
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(4px);
            display: none;
            overflow: hidden;
        }

        .log-title {
            padding: 12px 20px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #9aaef5;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .log-area {
            height: 220px;
            overflow-y: auto;
            padding: 12px 18px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #b3f0d5;
            line-height: 1.65;
        }

        .log-line {
            margin-bottom: 6px;
            border-left: 2px solid #5f6ef0;
            padding-left: 12px;
            opacity: 0.85;
        }

        .result-card {
            margin-top: 28px;
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(16px);
            border-radius: 38px;
            padding: 20px;
            border: 1px solid rgba(129, 140, 248, 0.5);
            display: none;
            animation: fadeSlide 0.35s ease;
        }

        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-success-header {
            display: flex;
            gap: 12px;
            align-items: center;
            font-weight: 700;
            font-size: 1.2rem;
            color: #7ef0ba;
            margin-bottom: 18px;
        }

        .info-block {
            background: rgba(10, 14, 26, 0.7);
            border-radius: 28px;
            padding: 12px 18px;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .info-label {
            font-size: 0.7rem;
            font-weight: 600;
            color: #9aabdf;
        }

        .info-value {
            font-family: monospace;
            font-weight: 500;
            word-break: break-all;
            color: #f0f3ff;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .copy-icon {
            background: #2a2f4b;
            border-radius: 30px;
            padding: 5px 14px;
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.2s;
        }

        .copy-icon:hover {
            background: #5f6ef0;
            color: white;
        }

        .reset-light {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.2);
            width: 100%;
            margin-top: 12px;
            border-radius: 40px;
            padding: 12px;
            font-weight: 600;
            color: #cdd9ff;
            cursor: pointer;
        }

        .loader-center {
            display: none;
            text-align: center;
            margin: 24px 0;
        }

        .spinner-ring {
            width: 48px;
            height: 48px;
            border: 3px solid rgba(102,126,234,0.2);
            border-top: 3px solid #b16cea;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 16px;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .toast-modal {
            position: fixed;
            top: 30%;
            left: 50%;
            transform: translate(-50%, -30%);
            background: #101624f2;
            backdrop-filter: blur(24px);
            border-radius: 48px;
            padding: 22px 28px;
            width: 320px;
            text-align: center;
            z-index: 1000;
            border: 1px solid rgba(255,215,0,0.4);
            box-shadow: 0 25px 40px rgba(0,0,0,0.5);
            animation: popModal 0.2s ease-out;
            display: none;
        }

        @keyframes popModal {
            0% { opacity: 0; scale: 0.9; }
            100% { opacity: 1; scale: 1; }
        }

        .toast-modal h4 {
            color: #ffe6b3;
            margin-bottom: 18px;
        }

        .toast-row {
            background: #0101014d;
            border-radius: 36px;
            padding: 12px;
            margin: 12px 0;
            word-break: break-all;
            font-size: 0.8rem;
        }

        .toast-actions {
            display: flex;
            gap: 12px;
            margin-top: 18px;
            justify-content: center;
        }

        .toast-btn {
            background: #5f6ef0;
            border: none;
            padding: 8px 18px;
            border-radius: 40px;
            font-weight: 600;
            cursor: pointer;
        }

        @media (max-width: 520px) {
            .main-card { border-radius: 40px; }
            .form-panel { padding: 20px; }
        }
    </style>
</head>
<body>
<div class="nebula"></div>
<div class="glass-orb"></div>

<div class="main-card">
    <div class="accent-header">
        <div class="chip"><i class="fas fa-gem"></i> 奕涵·专属通道</div>
        <h1><i class="fas fa-cloud-upload-alt"></i> JumperVPN</h1>
        <p>极光引擎 · 临时邮箱自动注册 + 随机密码生成</p>
    </div>
    <div class="form-panel">
        <div class="input-row">
            <div class="input-label"><i class="fas fa-envelope"></i> 注册邮箱 (自动)</div>
            <input type="text" id="showEmailField" class="field" placeholder="注册成功后将显示" readonly style="background:#0c1122cc">
        </div>
        <div class="input-row">
            <div class="input-label"><i class="fas fa-key"></i> 密码</div>
            <div class="random-pwd-wrapper">
                <input type="text" id="pwdInput" class="field" placeholder="可自定义或随机生成" value="Xiangzi6681">
                <button type="button" id="randomPwdBtn" class="random-btn"><i class="fas fa-dice-d6"></i> 随机</button>
            </div>
        </div>
        <div class="input-row">
            <div class="input-label"><i class="fas fa-ticket-alt"></i> 邀请码</div>
            <input type="text" id="inviteCode" class="field" value="9QGE5V">
        </div>
        <div class="input-row">
            <div class="input-label"><i class="fas fa-laptop-code"></i> 设备模式</div>
            <div class="device-toggles">
                <label class="device-opt" id="iosLabel">
                    <i class="fab fa-apple"></i> iOS
                    <input type="radio" name="platform" value="ios" checked>
                </label>
                <label class="device-opt" id="winLabel">
                    <i class="fab fa-windows"></i> Windows
                    <input type="radio" name="platform" value="windows">
                </label>
            </div>
        </div>
        <button class="glow-btn" id="startRegBtn"><i class="fas fa-bolt"></i> 开启极速注册</button>

        <div class="loader-center" id="loaderDiv">
            <div class="spinner-ring"></div>
            <p style="color:#a0b3f0; font-size:0.75rem;">正在部署隧道 & 获取验证码...</p>
        </div>

        <div class="log-console" id="logConsole">
            <div class="log-title"><i class="fas fa-code-branch"></i> 实时执行流</div>
            <div class="log-area" id="logArea"></div>
        </div>

        <div class="result-card" id="resultCard">
            <div class="result-success-header" id="resultHeaderIcon">
                <i class="fas fa-check-circle" style="font-size: 1.6rem;"></i> <span id="resultTitleText">注册成功</span>
            </div>
            <div class="info-block">
                <span class="info-label">📧 邮箱</span>
                <span class="info-value"><span id="resultEmail"></span> <span class="copy-icon" data-clip="email">复制</span></span>
            </div>
            <div class="info-block">
                <span class="info-label">🔐 密码</span>
                <span class="info-value"><span id="resultPwd"></span> <span class="copy-icon" data-clip="pwd">复制</span></span>
            </div>
            <div class="info-block">
                <span class="info-label">⏱️ 免费剩余</span>
                <span class="info-value"><span id="resultFree"></span></span>
            </div>
            <div class="info-block">
                <span class="info-label">📆 到期时间</span>
                <span class="info-value"><span id="resultEnd"></span></span>
            </div>
            <div class="info-block">
                <span class="info-label">🎫 JWT Token</span>
                <div class="info-value"><span id="resultToken" style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">••••••</span> 
                    <span class="copy-icon" data-clip="token">复制Token</span>
                    <span id="toggleTokenBtn" style="background:#2a2f4b; border-radius:30px; padding:5px 12px; font-size:0.7rem; cursor:pointer;">显示</span>
                </div>
            </div>
            <button class="reset-light" id="resetAllBtn"><i class="fas fa-undo-alt"></i> 重新注册</button>
        </div>
    </div>
</div>

<!-- 弹窗模态框 -->
<div id="successModal" class="toast-modal">
    <h4><i class="fas fa-gift"></i> 注册成功！账号信息已生成</h4>
    <div class="toast-row"><strong>📧 邮箱：</strong> <span id="modalEmail"></span></div>
    <div class="toast-row"><strong>🔑 密码：</strong> <span id="modalPwd"></span></div>
    <div class="toast-actions">
        <button class="toast-btn" id="copyAllInfo"><i class="fas fa-copy"></i> 一键复制(邮箱+密码)</button>
        <button class="toast-btn" id="closeModalBtn" style="background:#3a405b;">关闭</button>
    </div>
</div>

<script>
    // ---------- 交互逻辑 (完全保留后端API，仅UI+随机密码增强) ----------
    let currentSessionId = null;
    let pollInterval = null;
    let tokenHidden = true;
    let latestResult = null;

    // DOM 元素
    const startBtn = document.getElementById('startRegBtn');
    const loaderDiv = document.getElementById('loaderDiv');
    const logConsole = document.getElementById('logConsole');
    const logArea = document.getElementById('logArea');
    const resultCard = document.getElementById('resultCard');
    const pwdInput = document.getElementById('pwdInput');
    const randomBtn = document.getElementById('randomPwdBtn');
    const inviteInput = document.getElementById('inviteCode');
    const iosRadio = document.querySelector('input[value="ios"]');
    const winRadio = document.querySelector('input[value="windows"]');
    const iosLabel = document.getElementById('iosLabel');
    const winLabel = document.getElementById('winLabel');
    const resetAllBtn = document.getElementById('resetAllBtn');
    const showEmailField = document.getElementById('showEmailField');

    // 结果字段
    const resultEmailSpan = document.getElementById('resultEmail');
    const resultPwdSpan = document.getElementById('resultPwd');
    const resultFreeSpan = document.getElementById('resultFree');
    const resultEndSpan = document.getElementById('resultEnd');
    const resultTokenSpan = document.getElementById('resultToken');
    const toggleTokenBtnSpan = document.getElementById('toggleTokenBtn');
    const resultTitleText = document.getElementById('resultTitleText');

    // 模态框
    const modal = document.getElementById('successModal');
    const modalEmailSpan = document.getElementById('modalEmail');
    const modalPwdSpan = document.getElementById('modalPwd');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const copyAllBtn = document.getElementById('copyAllInfo');

    // 设备样式切换
    function updateDeviceUI() {
        if(iosRadio.checked) {
            iosLabel.classList.add('active');
            winLabel.classList.remove('active');
        } else {
            winLabel.classList.add('active');
            iosLabel.classList.remove('active');
        }
    }
    iosRadio.addEventListener('change', updateDeviceUI);
    winRadio.addEventListener('change', updateDeviceUI);
    updateDeviceUI();

    // 随机密码生成
    function generateRandomPassword(len = 12) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
        let result = '';
        for(let i = 0; i < len; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }
    randomBtn.addEventListener('click', () => {
        const newPwd = generateRandomPassword(12);
        pwdInput.value = newPwd;
    });

    // 日志追加
    function addLog(msg) {
        const line = document.createElement('div');
        line.className = 'log-line';
        line.textContent = msg;
        logArea.appendChild(line);
        line.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    function clearLogs() { logArea.innerHTML = ''; }

    function stopPoll() {
        if(pollInterval) { clearInterval(pollInterval); pollInterval = null; }
    }

    function resetUIState() {
        stopPoll();
        currentSessionId = null;
        latestResult = null;
        resultCard.style.display = 'none';
        logConsole.style.display = 'none';
        loaderDiv.style.display = 'none';
        startBtn.disabled = false;
        tokenHidden = true;
        resultTokenSpan.textContent = '••••••••';
        toggleTokenBtnSpan.textContent = '显示';
        showEmailField.value = '';
        clearLogs();
    }

    // 弹窗展示邮箱密码
    function showAccountModal(email, pwd) {
        modalEmailSpan.textContent = email;
        modalPwdSpan.textContent = pwd;
        modal.style.display = 'block';
        setTimeout(() => {
            // 自动消失？但保留让用户手动关闭，更友好
        }, 1);
    }

    function closeModal() { modal.style.display = 'none'; }
    closeModalBtn.addEventListener('click', closeModal);
    copyAllBtn.addEventListener('click', () => {
        if(latestResult) {
            const copyText = `邮箱: ${latestResult.email}\n密码: ${latestResult.pwd}`;
            navigator.clipboard.writeText(copyText).then(() => {
                alert('✅ 邮箱+密码已复制到剪贴板');
                closeModal();
            }).catch(() => alert('复制失败'));
        } else {
            closeModal();
        }
    });

    // 展示成功结果并弹窗
    function showFinalResult(data) {
        latestResult = data;
        resultCard.style.display = 'block';
        resultTitleText.textContent = '注册成功 🎉';
        resultEmailSpan.textContent = data.email;
        resultPwdSpan.textContent = data.pwd;
        resultFreeSpan.textContent = data.free_time;
        resultEndSpan.textContent = data.end_time;
        resultTokenSpan.textContent = '••••••••••••••';
        tokenHidden = true;
        toggleTokenBtnSpan.textContent = '显示';
        showEmailField.value = data.email;
        // 弹窗显示邮箱密码
        showAccountModal(data.email, data.pwd);
    }

    function showErrorResult(errMsg) {
        resultCard.style.display = 'block';
        resultTitleText.innerHTML = '<i class="fas fa-times-circle"></i> 注册失败';
        resultTitleText.style.color = '#ffa79e';
        resultEmailSpan.textContent = errMsg;
        resultPwdSpan.textContent = '—';
        resultFreeSpan.textContent = '—';
        resultEndSpan.textContent = '—';
        resultTokenSpan.textContent = '—';
        latestResult = null;
    }

    function pollStatus(sessionId) {
        fetch(`/api/status/${sessionId}`)
            .then(res => res.json())
            .then(data => {
                if(data.logs && data.logs.length) {
                    clearLogs();
                    data.logs.forEach(line => addLog(line));
                }
                if(data.done) {
                    stopPoll();
                    loaderDiv.style.display = 'none';
                    startBtn.disabled = false;
                    if(data.success && data.result) {
                        showFinalResult(data.result);
                    } else {
                        showErrorResult(data.error || '注册失败，请检查网络或重试');
                    }
                }
            })
            .catch(err => {
                stopPoll();
                loaderDiv.style.display = 'none';
                startBtn.disabled = false;
                showErrorResult('状态获取异常: ' + err);
            });
    }

    startBtn.addEventListener('click', () => {
        if(startBtn.disabled) return;
        let password = pwdInput.value.trim();
        if(password === '') password = 'Xiangzi6681';
        const invite = inviteInput.value.trim() || '9QGE5V';
        const mode = document.querySelector('input[name="platform"]:checked').value;

        const payload = {
            pwd: password,
            invite: invite,
            mode: mode
        };

        resetUIState();
        loaderDiv.style.display = 'block';
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
                throw new Error('无法创建注册会话');
            }
        })
        .catch(err => {
            loaderDiv.style.display = 'none';
            startBtn.disabled = false;
            addLog(`❌ 请求错误: ${err.message}`);
            showErrorResult('网络错误: ' + err.message);
        });
    });

    // 复制功能 (基于最新结果)
    document.querySelectorAll('.copy-icon').forEach(el => {
        el.addEventListener('click', (e) => {
            const type = el.getAttribute('data-clip');
            if(!latestResult) { alert('暂无数据'); return; }
            let copyStr = '';
            if(type === 'email') copyStr = latestResult.email;
            else if(type === 'pwd') copyStr = latestResult.pwd;
            else if(type === 'token') copyStr = latestResult.token;
            if(copyStr) {
                navigator.clipboard.writeText(copyStr).then(() => {
                    const original = el.innerText;
                    el.innerText = '已复制!';
                    setTimeout(() => { el.innerText = original; }, 1200);
                }).catch(() => alert('复制失败'));
            }
        });
    });

    // token 显示/隐藏
    toggleTokenBtnSpan.addEventListener('click', () => {
        if(!latestResult || !latestResult.token) { alert('无Token'); return; }
        if(tokenHidden) {
            resultTokenSpan.textContent = latestResult.token;
            toggleTokenBtnSpan.textContent = '隐藏';
        } else {
            resultTokenSpan.textContent = '••••••••••••••••';
            toggleTokenBtnSpan.textContent = '显示';
        }
        tokenHidden = !tokenHidden;
    });

    resetAllBtn.addEventListener('click', () => {
        resetUIState();
        resultCard.style.display = 'none';
        logConsole.style.display = 'none';
        pwdInput.value = 'Xiangzi6681';
        showEmailField.value = '';
        if(pollInterval) clearInterval(pollInterval);
        startBtn.disabled = false;
        latestResult = null;
        modal.style.display = 'none';
    });

    // 点击模态背景关闭简单处理
    window.onclick = (e) => { if(e.target === modal) modal.style.display = 'none'; };
</script>
</body>
</html>
