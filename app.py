from flask import Flask, request, Response
import requests
import traceback

app = Flask(__name__)

@app.route('/api/beeinbox/', defaults={'target_path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/api/beeinbox/<path:target_path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy_beeinbox(target_path):
    if request.method == 'OPTIONS':
        return ('', 204)
    
    try:
        query_string = request.query_string.decode()
        url = f'https://amades.site/{target_path}'
        if query_string:
            url += '?' + query_string
        
        resp = requests.request(
            method=request.method,
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
            },
            data=request.get_data(),
            allow_redirects=True,
            timeout=15,
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'host']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        response = Response(resp.content, resp.status_code, headers)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        error_msg = f"Error: {str(e)}\n\n{traceback.format_exc()}"
        return Response(error_msg, status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
