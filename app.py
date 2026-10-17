from flask import Flask, Response
import requests
import traceback

app = Flask(__name__)

@app.route('/api/test-requests', methods=['GET'])
def test_requests():
    try:
        # 测试简单的网站
        r = requests.get('https://httpbin.org/get', timeout=10)
        return Response(f"OK! Status: {r.status_code}\nContent: {r.text[:500]}", mimetype='text/plain')
    except Exception as e:
        return Response(f"Error: {e}\n\n{traceback.format_exc()}", status=500, mimetype='text/plain')

@app.route('/api/test-amades', methods=['GET'])
def test_amades():
    try:
        r = requests.get('https://amades.site/', timeout=15)
        return Response(f"OK! Status: {r.status_code}\nLength: {len(r.text)}", mimetype='text/plain')
    except Exception as e:
        return Response(f"Error: {e}\n\n{traceback.format_exc()}", status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
