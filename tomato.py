# -*- coding: utf-8 -*-
import datetime
from flask import Flask, request, jsonify, make_response
from celery import Celery
from task import play_music, play_break, stop_music
import time
from response import update_res_content


app = Flask(__name__)


start_time = None

@app.route('/api', methods=['POST'])
def my_api():
    global start_time 
    data = request.json
    seq = data.get('sequence')

def current_time():
    time_lapse = time.time() - start_time
    time_lapse = time_lapse // 60
    return time_lapse

    # response_content = {
    #     "versionid": "1.0",
    #     "is_end": False,
    #     "sequence": seq,
    #     "timestamp": int(time.time() * 1000),
    #     "directive": {
    #         "directive_items": [
    #             {
    #                 "content": "欢迎来到番茄钟，您可以说开启计时",
    #                 "type": "1"
    #             }
    #         ]
    #     }
    # }

    # def update_res_content(s):
    #     response_content['directive'] = {
    #     "directive_items": [
    #         {
    #             "content": s,
    #             "type": "1"
    #         }
    #     ]
    # }
    #     return jsonify(response_content)
        

    # 开启番茄钟
    if data.get('bizname') and data.get('focus') == '番茄钟':
        update_res_content("欢迎来到番茄钟，您可以说开启计时")
    
    # 开启计时
    elif data.get('start') and data.get('timer'):
        if start_time is None:  # 仅在start_time未初始化时设置它
            start_time = time.time()
        # Start playing music asynchronously for 25 minutes
        play_music('Study and Relax.mp3', 1500) 
        # play_music_async.delay('Study and Relax.mp3')  # Adjust the path as necessary
        update_res_content("您已经专注了25分钟,可以适当休息5分钟。您可以选择说开始休息或者放弃休息",seq)

    # 询问专注时间
    elif data.get('focuses') and data.get('focus') == '番茄钟':
        if start_time is not None:
            time_lapse = time.time() - start_time
            time_lapse = time_lapse // 60
            formatted_content = "您已经专注了{}分钟".format(int(time_lapse))
            update_res_content(formatted_content, seq)
            #还没开启倒计时
        else:
            # 这里处理 start_time 为 None 的情况，比如返回一个错误消息
            update_res_content("还没有开启倒计时，您可以说开启倒计时来记录专注时间", seq)
            #放弃专注
    elif data.get('stop') and data.get('break') is None:
        if start_time is not None:
            time_lapse = time.time() - start_time
            time_lapse = time_lapse // 60
            s = "您已经专注了{}分钟,那我就先退出了".format(int(time_lapse))
        else:
            s = "没什么事我就先退出了"
        stop_music()
        response_content = {
            "versionid": "1.0",
            "is_end": True,  # 根据逻辑调整是否结束会话
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": s,
                        "type": "1"
                    }
                ]
            }
        }
    #放弃休息
    elif data.get('stop') and data.get('break'):
        stop_music()
        response_content = {
            "versionid": "1.0",
            "is_end": False,
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": "休息结束，您可以说“开启计时”或者放弃计时",
                        "type": "1"
                    }
                ]
            }
        }
        #开启休息
    elif data.get('start') and data.get('break'):
        play_break('Study and Relax.mp3')
        response_content = {
            "versionid": "1.0",
            "is_end": False,
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": "休息结束，您可以说“开启计时”或者放弃计时",
                        "type": "1"
                    }
                ]
            }
        }
    # 未识别的意图
    else:
            response_content = {
                "versionid": "1.0",
                "is_end": False,  # 根据逻辑调整是否结束会话
                "sequence": seq,
                "timestamp": int(time.time() * 1000),
                "directive": {
                    "directive_items": [
                        {
                            "content": "很抱歉，我听不懂您在说什么",
                            "type": "1"
                        }
                    ]
                },
                "repeat_directive": {}
            }
    response = make_response(jsonify(response_content))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080, threaded=True)


