// api/beeinbox/[...path].js
// 反向代理 beeinbox.com，解决跨域问题

export default async function handler(req, res) {
    const { path = [] } = req.query;
    const targetPath = Array.isArray(path) ? path.join('/') : path;
    const targetUrl = `https://beeinbox.com/${targetPath}${req.url.includes('?') ? '?' + req.url.split('?')[1] : ''}`;

    try {
        const response = await fetch(targetUrl, {
            method: req.method,
            headers: {
                ...req.headers,
                host: 'beeinbox.com',
            },
            body: ['GET', 'HEAD'].includes(req.method) ? undefined : JSON.stringify(req.body),
        });

        // 复制响应头
        const headers = {};
        response.headers.forEach((value, key) => {
            // 不复制跨域相关的头，我们自己设置
            if (!['access-control-', 'content-security-policy', 'x-frame-options'].some(h => key.toLowerCase().startsWith(h))) {
                headers[key] = value;
            }
        });

        // 设置CORS头
        headers['access-control-allow-origin'] = '*';
        headers['access-control-allow-methods'] = 'GET, POST, PUT, DELETE, OPTIONS';
        headers['access-control-allow-headers'] = 'Content-Type, Authorization';

        const body = await response.text();
        
        res.status(response.status);
        Object.entries(headers).forEach(([k, v]) => res.setHeader(k, v));
        res.send(body);
    } catch (error) {
        res.status(500).json({ error: 'Proxy error', message: error.message });
    }
}
