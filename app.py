from flask import Flask, Response
import requests
import re
import json

app = Flask(__name__)

@app.route('/api/test-set-domain', methods=['GET'])
def test_set_domain():
    results = []
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 第一次请求
    r1 = s.get('https://beeinbox.com/', headers=headers)
    results.append(f"第一次请求: {r1.status_code}")
    
    # 找frontend.actions组件的wire:id
    match = re.search(r'wire:initial-data="([^"]+)"', r1.text)
    if match:
        # 这个是HTML转义的，需要先反转义
        data_str = match.group(1).replace('&quot;', '"').replace('&amp;', '&')
        data = json.loads(data_str)
        results.append(f"组件名: {data.get('name')}")
        results.append(f"组件ID: {data.get('id')}")
        results.append(f"当前域名: {data.get('serverMemo', {}).get('data', {}).get('domain')}")
        results.append(f"可选域名: {data.get('serverMemo', {}).get('data', {}).get('domains')}")
        
        component_id = data.get('id')
        component_name = data.get('name')
    else:
        results.append("没找到组件")
        return Response("\n".join(results), mimetype='text/plain')
    
    # 第二次请求，生成邮箱
    r2 = s.get('https://beeinbox.com/', headers=headers)
    results.append(f"\n第二次请求: {r2.status_code}")
    
    # 找当前邮箱
    const_match = re.search(r"const email = '([^']+)'", r2.text)
    if const_match:
        results.append(f"当前邮箱: {const_match.group(1)}")
    
    # 尝试调用Livewire的setDomain方法
    # Livewire 3的更新接口
    livewire_data = {
        "components": [
            {
                "snapshot": json.dumps({
                    "memo": {
                        "id": component_id,
                        "name": component_name,
                        "path": "/",
                        "method": "GET",
                    },
                    "data": {
                        "domain": "beeinbox.com",
                        "domains": ["beeinbox.com", "amades.site"],
                    },
                }),
                "updates": [
                    {
                        "type": "callMethod",
                        "payload": {
                            "method": "setDomain",
                            "params": ["amades.site"],
                        }
                    }
                ],
                "calls": [
                    {
                        "path": "",
                        "method": "setDomain",
                        "params": ["amades.site"],
                    }
                ],
            }
        ]
    }
    
    results.append("\n尝试调用setDomain...")
    try:
        r = requests.post(
            'https://beeinbox.com/livewire/update',
            headers={
                **headers,
                'Content-Type': 'application/json',
                'X-Livewire': '1',
            },
            json=livewire_data,
        )
        results.append(f"状态码: {r.status_code}")
        results.append(f"响应: {r.text[:1000]}")
    except Exception as e:
        results.append(f"错误: {e}")
    
    return Response("\n".join(results), mimetype='text/plain')

if __name__ == '__main__':
    app.run()
