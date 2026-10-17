from flask import Flask, Response
import requests
import re

app = Flask(__name__)

domains = ['beeinbox.com', 'ussteel.xyz', 'beeinbox.shop', 'beeinbox.space']

@app.route('/api/test-emails', methods=['GET'])
def test_emails():
    results = []
    for d in domains:
        try:
            s = requests.Session()
            # 第一次请求
            s.get(f'https://{d}/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            # 第二次请求生成邮箱
            r = s.get(f'https://{d}/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            
            # 找邮箱
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', r.text)
            unique_emails = []
            for e in emails:
                if 'beeinbox' not in e and 'medium' not in e and 'example' not in e and 'admin' not in e:
                    if e not in unique_emails:
                        unique_emails.append(e)
            
            # 也找const email =
            const_match = re.search(r"const email = '([^']+)'", r.text)
            const_email = const_match.group(1) if const_match else 'not found'
            
            results.append(f"{d}:")
            results.append(f"  const email: {const_email}")
            results.append(f"  其他邮箱: {unique_emails[:5]}")
            results.append("")
        except Exception as e:
            results.append(f"❌ {d}: {e}")
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
