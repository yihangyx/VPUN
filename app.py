from flask import Flask, Response
import requests
import re

app = Flask(__name__)

@app.route('/api/find-domain-switch', methods=['GET'])
def find_switch():
    s = requests.Session()
    s.get('https://beeinbox.com/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    r = s.get('https://beeinbox.com/', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    
    text = r.text
    results = []
    
    # 找所有域名相关的
    results.append("=== 包含domain的内容 ===")
    for match in re.finditer(r'domain', text, re.IGNORECASE):
        start = max(0, match.start()-50)
        end = min(len(text), match.end()+50)
        results.append(text[start:end])
        results.append("---")
    
    # 找所有wire:click相关的
    results.append("\n=== wire:click 方法 ===")
    clicks = re.findall(r'wire:click="([^"]+)"', text)
    for c in clicks:
        results.append(c)
    
    # 找所有select相关的
    results.append("\n=== select选项 ===")
    selects = re.findall(r'<select[^>]*>(.*?)</select>', text, re.DOTALL)
    for sel in selects:
        options = re.findall(r'<option[^>]*>([^<]+)</option>', sel)
        results.append(f"选项: {options}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
