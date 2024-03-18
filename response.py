from flask import jsonify
import time

# 定义全局变量response_content
response_content = {
    "versionid": "1.0",
    "is_end": False,
    "sequence": [],  # 你需要定义这个变量seq，或者传递它作为参数
    "timestamp": int(time.time() * 1000),
    "directive": {
        "directive_items": [
            {
                "content": "欢迎来到番茄钟，您可以说开启计时",
                "type": "1"
            }
        ]
    }
}

def update_res_content(s, seq):
    global response_content
    response_content['sequence'] = seq
    response_content['timestamp'] = int(time.time() * 1000)
    response_content['directive'] = {
        "directive_items": [
            {
                "content": s,
                "type": "1"
            }
        ]
    }
    return jsonify(response_content)
