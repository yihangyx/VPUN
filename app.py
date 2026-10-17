from flask import Flask, Response
import requests
import re

app = Flask(__name__)

@app.route('/api/generate-until-shop', methods=['GET'])
def generate_until_shop():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    target_suffix = 'beeinbox.shop'
    found = False
    
    for attempt in range(10):
        results.append(f"尝试 {attempt+1}...")
        
        # 每次用新session
        s = requests.Session()
        s.get('https://beeinbox.com/', headers=headers)
        r = s.get('https://beeinbox.com/', headers=headers)
        
        const_match = re.search(r"const email = '([^']+)'", r.text)
        if const_match:
            email = const_match.group(1)
            results.append(f"  生成: {email}")
            
            if email.endswith(target_suffix):
                results.append(f"  ✅ 找到目标后缀!")
                results.append(f"\n最终邮箱: {email}")
                found = True
                break
    
    if not found:
        results.append("\n❌ 10次尝试都没找到")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
