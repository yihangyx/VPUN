from flask import Flask, Response
import requests
import re

app = Flask(__name__)

@app.route('/api/find-delete', methods=['GET'])
def find_delete():
    results = []
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 先创建邮箱
    s.get('https://beeinbox.com/', headers=headers)
    r = s.get('https://beeinbox.com/', headers=headers)
    
    const_match = re.search(r"const email = '([^']+)'", r.text)
    email = const_match.group(1)
    results.append(f"初始邮箱: {email}")
    
    # 找deleteEmail相关的内容
    results.append("\n=== deleteEmail相关 ===")
    for match in re.finditer(r'deleteEmail', r.text):
        start = max(0, match.start()-100)
        end = min(len(r.text), match.end()+100)
        results.append(r.text[start:end])
        results.append("---")
    
    # 找wire:click的元素
    results.append("\n=== wire:click元素 ===")
    click_els = re.findall(r'<[^>]*wire:click="([^"]+)"[^>]*>', r.text)
    for c in click_els:
        results.append(c)
    
    # 找Livewire的token或者csrf
    csrf_match = re.search(r'name="csrf-token" content="([^"]+)"', r.text)
    if csrf_match:
        results.append(f"\nCSRF token: {csrf_match.group(1)}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
