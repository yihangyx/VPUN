from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test():
    if request.method == 'OPTIONS':
        return ('', 204)
    return Response(json.dumps({'status': 'ok', 'message': 'API works'}), mimetype='application/json')

@app.route('/api/beeinbox/', defaults={'target_path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/api/beeinbox/<path:target_path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy_beeinbox(target_path):
    if request.method == 'OPTIONS':
        return ('', 204)
    return Response(json.dumps({'path': target_path, 'method': request.method}), mimetype='application/json')

if __name__ == '__main__':
    app.run()
