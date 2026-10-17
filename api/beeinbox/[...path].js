// api/beeinbox/[...path].js
// 反向代理 beeinbox.com，解决跨域问题

module.exports = async function handler(req, res) {
    const { path = [] } = req.query;
    const targetPath = Array.isArray(path) ? path.join('/') : path;
    const queryString = req.url.includes('?') ? '?' + req.url.split('?')[1] : '';
    const targetUrl = `https://beeinbox.com/${targetPath}${queryString}`;

    try {
        const response = await fetch(targetUrl, {
            method: req.method,
            headers: {
                ...req.headers,
                host: 'beeinbox.com',
            },
            body: ['GET', 'HEAD'].includes(req.method) ? undefined : JSON.stringify(req.body),
        });

        const body = await response.text();
        
        res.status(response.status);
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        res.send(body);
    } catch (error) {
        res.status(500).json({ error: 'Proxy error', message: error.message });
    }
};
