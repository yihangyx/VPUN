// api/vpn/[...path].js
// 代理 JumperVPN API，解决跨域问题

const crypto = require('crypto');

const SIGN_KEY = '000000000000000000018d91e471e0989cda27df505a453f2b7635294f2ddf23e3b122acc99c9e9f1e14';

function makeSign(path) {
    return crypto.createHmac('sha256', SIGN_KEY).update(path).digest('hex');
}

module.exports = async function handler(req, res) {
    const { path = [] } = req.query;
    const targetPath = Array.isArray(path) ? path.join('/') : path;
    const targetUrl = `https://api.jumperservice.com/v1/${targetPath}`;

    try {
        const headers = {
            'app-id': '2',
            'version': '1.0.8',
            'buildNumber': '3',
            'os': 'ios',
            'Content-Language': 'en-us',
            'User-Agent': 'JumperVPN/1.0.8 (com.jumper.net.solutions.vpn; build:3; iOS 18.6.0) Alamofire/5.10.2',
            'Accept-Language': 'zh-Hans-CN;q=1.0',
            'x-sign': makeSign(targetPath),
            'Content-Type': 'application/json',
        };

        if (req.headers['j-token']) headers['j-token'] = req.headers['j-token'];
        if (req.headers['imei']) headers['imei'] = req.headers['imei'];
        if (req.headers['device-name']) headers['device-name'] = req.headers['device-name'];

        const response = await fetch(targetUrl, {
            method: req.method,
            headers: headers,
            body: ['GET', 'HEAD'].includes(req.method) ? undefined : JSON.stringify(req.body),
        });

        const data = await response.json();
        
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(response.status);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'VPN API error', message: error.message });
    }
};
