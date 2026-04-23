/**
 * JumperVPN Browser API Library
 * 纯浏览器端，直接调用 api.jumperservice.com
 */

const BASE = 'https://api.jumperservice.com/v1/';
const SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14';
const MAIL_TM = 'https://api.mail.tm';
const INVITE_CODE = '9QGE5V';

// ====== 工具函数 ======

function md5(text) {
  // 浏览器端 MD5 实现
  const md5cycle = (x, k) => {
    let a = x[0], b = x[1], c = x[2], d = x[3];
    a = ff(a, b, c, d, k[0], 7, -680876936); d = ff(d, a, b, c, k[1], 12, -389564586); c = ff(c, d, a, b, k[2], 17, 606105819); b = ff(b, c, d, a, k[3], 22, -1044525330);
    a = ff(a, b, c, d, k[4], 7, -176418897); d = ff(d, a, b, c, k[5], 12, 1200080426); c = ff(c, d, a, b, k[6], 17, -1473231341); b = ff(b, c, d, a, k[7], 22, -45705983);
    a = ff(a, b, c, d, k[8], 7, 1770035416); d = ff(d, a, b, c, k[9], 12, -1958414417); c = ff(c, d, a, b, k[10], 17, -42063); b = ff(b, c, d, a, k[11], 22, -1990404162);
    a = ff(a, b, c, d, k[12], 7, 1804603682); d = ff(d, a, b, c, k[13], 12, -40341101); c = ff(c, d, a, b, k[14], 17, -1502002290); b = ff(b, c, d, a, k[15], 22, 1236535329);
    a = gg(a, b, c, d, k[1], 5, -165796510); d = gg(d, a, b, c, k[6], 9, -1069501632); c = gg(c, d, a, b, k[11], 14, 643717713); b = gg(b, c, d, a, k[0], 20, -373897302);
    a = gg(a, b, c, d, k[5], 5, -701558691); d = gg(d, a, b, c, k[10], 9, 38016083); c = gg(c, d, a, b, k[15], 14, -660478335); b = gg(b, c, d, a, k[4], 20, -405537848);
    a = gg(a, b, c, d, k[9], 5, 568446438); d = gg(d, a, b, c, k[14], 9, -1019803690); c = gg(c, d, a, b, k[3], 14, -187363961); b = gg(b, c, d, a, k[8], 20, 1163531501);
    a = gg(a, b, c, d, k[13], 5, -1444681467); d = gg(d, a, b, c, k[2], 9, -51403784); c = gg(c, d, a, b, k[7], 14, 1735328473); b = gg(b, c, d, a, k[12], 20, -1926607734);
    a = hh(a, b, c, d, k[5], 4, -378558); d = hh(d, a, b, c, k[8], 11, -2022574463); c = hh(c, d, a, b, k[11], 16, 1839030562); b = hh(b, c, d, a, k[14], 23, -35309556);
    a = hh(a, b, c, d, k[1], 4, -1530992060); d = hh(d, a, b, c, k[4], 11, 1272893353); c = hh(c, d, a, b, k[7], 16, -155497632); b = hh(b, c, d, a, k[10], 23, -1094730640);
    a = hh(a, b, c, d, k[13], 4, 681279174); d = hh(d, a, b, c, k[0], 11, -358537222); c = hh(c, d, a, b, k[3], 16, -722521979); b = hh(b, c, d, a, k[6], 23, 76029189);
    a = hh(a, b, c, d, k[9], 4, -640364487); d = hh(d, a, b, c, k[12], 11, -421815835); c = hh(c, d, a, b, k[15], 16, 530742520); b = hh(b, c, d, a, k[2], 23, -995338651);
    a = ii(a, b, c, d, k[0], 6, -198630844); d = ii(d, a, b, c, k[7], 10, 1126891415); c = ii(c, d, a, b, k[14], 15, -1416354185); b = ii(b, c, d, a, k[5], 21, -57434055);
    a = ii(a, b, c, d, k[12], 6, 1700485571); d = ii(d, a, b, c, k[3], 10, -1894986606); c = ii(c, d, a, b, k[10], 15, -1051523); b = ii(b, c, d, a, k[1], 21, -2054922799);
    a = ii(a, b, c, d, k[8], 6, 1873313359); d = ii(d, a, b, c, k[15], 10, -30611744); c = ii(c, d, a, b, k[6], 15, -1560198380); b = ii(b, c, d, a, k[13], 21, 1309151649);
    a = ii(a, b, c, d, k[4], 6, -145523070); d = ii(d, a, b, c, k[11], 10, -1120210379); c = ii(c, d, a, b, k[2], 15, 718787259); b = ii(b, c, d, a, k[9], 21, -343485551);
    x[0] = add32(a, x[0]); x[1] = add32(b, x[1]); x[2] = add32(c, x[2]); x[3] = add32(d, x[3]);
  };
  const cmn = (q, a, b, x, s, t) => { a = add32(add32(a, q), add32(x, t)); return add32((a << s) | (a >>> (32 - s)), b); };
  const ff = (a, b, c, d, x, s, t) => cmn((b & c) | ((~b) & d), a, b, x, s, t);
  const gg = (a, b, c, d, x, s, t) => cmn((b & d) | (c & (~d)), a, b, x, s, t);
  const hh = (a, b, c, d, x, s, t) => cmn(b ^ c ^ d, a, b, x, s, t);
  const ii = (a, b, c, d, x, s, t) => cmn(c ^ (b | (~d)), a, b, x, s, t);
  const add32 = (a, b) => (a + b) & 0xFFFFFFFF;
  const md51 = (s) => {
    let n = s.length, state = [1732584193, -271733879, -1732584194, 271733878], i;
    for (i = 64; i <= n; i += 64) md5cycle(state, md5blk(s.substring(i - 64, i)));
    s = s.substring(i - 64);
    const tail = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0];
    for (i = 0; i < s.length; i++) tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
    tail[i >> 2] |= 0x80 << ((i % 4) << 3);
    if (i > 55) { md5cycle(state, tail); for (i = 0; i < 16; i++) tail[i] = 0; }
    tail[14] = n * 8;
    md5cycle(state, tail);
    return state;
  };
  const md5blk = (s) => {
    const md5blks = [];
    for (let i = 0; i < 64; i += 4) md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
    return md5blks;
  };
  const hex_chr = '0123456789abcdef'.split('');
  const rhex = (n) => { let s = ''; for (let j = 0; j < 4; j++) s += hex_chr[(n >> (j * 8 + 4)) & 0x0F] + hex_chr[(n >> (j * 8)) & 0x0F]; return s; };
  const hex = (x) => { for (let i = 0; i < x.length; i++) x[i] = rhex(x[i]); return x.join(''); };
  // UTF-8 encode
  const utf8encode = (str) => unescape(encodeURIComponent(str));
  return hex(md51(utf8encode(text)));
}

async function hmacSha256(key, message) {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(key);
  const msgData = encoder.encode(message);
  const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function generateIMEI() {
  return '{' + crypto.randomUUID().toUpperCase() + '}';
}

function decodeJWTPayload(token) {
  try {
    const parts = token.split('.');
    let payload = parts[1];
    payload += '='.repeat(4 - payload.length % 4);
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
  } catch { return null; }
}

// ====== API 调用 ======

async function apiCall(path, { method = 'GET', body = null, token = null, imei = null, os = 'ios' } = {}) {
  const url = BASE + path.replace(/^\//, '');
  const signPath = '/v1/' + path.replace(/^\//, '');
  const xSign = await hmacSha256(SIGN_KEY, signPath);

  const headers = {
    'app-id': '2',
    'version': '1.0.8',
    'buildNumber': '3',
    'x-sign': xSign,
    'Accept': '*/*',
  };

  if (os === 'ios') {
    headers['os'] = 'ios';
    headers['Content-Language'] = 'en-us';
    headers['User-Agent'] = 'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2';
    headers['Accept-Language'] = 'zh-Hans-CN;q=1.0';
    headers['Accept-Encoding'] = 'gzip, deflate, br';
  } else {
    headers['os'] = 'windows';
    headers['Content-Language'] = 'zh-cn';
    headers['User-Agent'] = 'JumperVPN/1.0.8';
  }

  if (imei) {
    headers['imei'] = imei.replace(/[{}]/g, '');
    headers['device-name'] = 'iPhone 15 Pro';
  }
  if (token) headers['j-token'] = token;
  if (body) headers['Content-Type'] = 'application/json';

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  try {
    const resp = await fetch(url, options);
    const text = await resp.text();
    try { return JSON.parse(text); }
    catch { return { code: resp.status, msg: text.substring(0, 200) }; }
  } catch (e) {
    return { code: -1, msg: e.message.substring(0, 200) };
  }
}

// ====== mail.tm 操作 ======

async function mailGet(url, token = null) {
  const headers = { 'Accept': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const resp = await fetch(url, { headers });
  return resp.json();
}

async function mailPost(url, body, token = null) {
  const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const resp = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
  return resp.json();
}

async function createTempEmail() {
  // 获取域名
  let domain = 'deltajohnsons.com';
  try {
    const domains = await mailGet(`${MAIL_TM}/domains`);
    if (Array.isArray(domains) && domains.length > 0) {
      domain = domains[0].domain || domain;
    } else if (domains['hydra:member'] && domains['hydra:member'].length > 0) {
      domain = domains['hydra:member'][0].domain || domain;
    }
  } catch (e) {
    console.warn('domains API failed, using fallback:', e);
  }

  // 生成随机用户名
  const username = Array.from({ length: 10 }, () => 'abcdefghijklmnopqrstuvwxyz0123456789'[Math.floor(Math.random() * 36)]).join('');
  const email = `${username}@${domain}`;
  const mailPwd = Array.from({ length: 16 }, () => 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[Math.floor(Math.random() * 62)]).join('');

  // 创建账户
  await mailPost(`${MAIL_TM}/accounts`, { address: email, password: mailPwd });

  // 获取 token
  const tokenResult = await mailPost(`${MAIL_TM}/token`, { address: email, password: mailPwd });
  const mailToken = tokenResult.token;
  if (!mailToken) throw new Error('mail token 获取失败');

  return { email, mailPwd, mailToken };
}

async function waitForCode(mailToken, maxWait = 90, onProgress = null) {
  const start = Date.now();
  while ((Date.now() - start) < maxWait * 1000) {
    try {
      const messages = await mailGet(`${MAIL_TM}/messages`, mailToken);
      const msgList = messages['hydra:member'] || (Array.isArray(messages) ? messages : []);
      for (const msg of msgList) {
        if (!msg.id) continue;
        const detail = await mailGet(`${MAIL_TM}/messages/${msg.id}`, mailToken);
        const bodyText = detail.text || detail.html || '';
        let match = bodyText.match(/(?:验证码|code|Code|CODE)[：:\s]*(\d{4,6})/);
        if (!match) match = bodyText.match(/\b(\d{4,6})\b/);
        if (match) return match[1];
      }
    } catch (e) {
      console.warn('poll error:', e);
    }
    if (onProgress) onProgress(Math.floor((Date.now() - start) / 1000));
    await new Promise(r => setTimeout(r, 3000));
  }
  return null;
}

// ====== 导出 ======

window.JumperAPI = {
  md5, hmacSha256, generateIMEI, decodeJWTPayload,
  apiCall, createTempEmail, waitForCode,
  INVITE_CODE, BASE, MAIL_TM
};
