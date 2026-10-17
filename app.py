from flask import Flask, Response
import requests
import traceback

app = Flask(__name__)

domains = [
    'beeinbox.com',
    'ussteel.xyz',
    'chinasteel.xyz',
    'visitlondon.live',
    'beeinbox.shop',
    'beeinbox.space',
]

@app.route('/api/test-domains', methods=['GET'])
def test_domains():
    results = []
    for d in domains:
        try:
            r = requests.get(f'https://{d}/', timeout=10)
            results.append(f"✅ {d}: {r.status_code} (length: {len(r.text)})")
        except Exception as e:
            results.append(f"❌ {d}: {type(e).__name__}")
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
