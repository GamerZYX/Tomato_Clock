# -*- coding: utf-8 -*-
import datetime
from flask import Flask, request, jsonify, make_response
from celery import Celery
from task import play_music, play_break, stop_music
import time


app = Flask(__name__)
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['result_backend'] = 'redis://localhost:6379/0'

start_time = None

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['result_backend'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#     return celery

# celery = make_celery(app)

# def play_music(file_path, play_time=1500):  # play_time in seconds, 1500s = 25min
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
    
#     # Wait for the specified play time (25 minutes here)
#     time.sleep(play_time)
    
#     # Stop the music after 25 minutes
#     pygame.mixer.music.stop()

# @celery.task
# def play_music_async(file_path, play_time=1500):
#     play_music(file_path, play_time)

@app.route('/api', methods=['POST'])
def my_api():
    global start_time 
    data = request.json
    seq = data.get('sequence')

    response_content = {
        "versionid": "1.0",
        "is_end": False,
        "sequence": seq,
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

    def update_res_content(s):
        response_content['directive'] = {
        "directive_items": [
            {
                "content": s,
                "type": "1"
            }
        ]
    }

    # 开启番茄钟
    if data.get('bizname') and data.get('focus') == '番茄钟':
        response_content['directive'] = {
                "directive_items": [
                    {
                        "content": "欢迎来到番茄钟，您可以说开启计时",
                        "type": "1"
                    }
                ]
        }
    
    # 开启计时
    elif data.get('start') and data.get('timer'):
        if start_time is None:  # 仅在start_time未初始化时设置它
            start_time = time.time()
        # Start playing music asynchronously for 25 minutes
        play_music('Study and Relax.mp3', 1500) 
        # play_music_async.delay('Study and Relax.mp3')  # Adjust the path as necessary
        response_content = {
            "versionid": "1.0",
            "is_end": False,
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": "您已经专注了25分钟,可以适当休息5分钟。您可以选择说开始休息或者放弃休息",
                        "type": "1"
                    }
                ]
            }
        }
    # 询问专注时间
    elif data.get('focuses') and data.get('focus') == '番茄钟':
        if start_time is not None:
            time_lapse = time.time() - start_time
            time_lapse = time_lapse // 60
            response_content = {
                "versionid": "1.0",
                "is_end": False,  # 根据逻辑调整是否结束会话
                "sequence": seq,
                "timestamp": int(time.time() * 1000),
                "directive": {
                    "directive_items": [
                        {
                            "content": "您已经专注了{}分钟".format(int(time_lapse)),
                            "type": "1"
                        }
                    ]
                }
            }
            #还没开启倒计时
        else:
            # 这里处理 start_time 为 None 的情况，比如返回一个错误消息
            response_content = {
                "versionid": "1.0",
                "is_end": False,  # 根据逻辑调整是否结束会话
                "sequence": seq,
                "timestamp": int(time.time() * 1000),
                "directive": {
                    "directive_items": [
                        {
                            "content": "还没有开启倒计时，您可以说开启倒计时来记录专注时间",
                            "type": "1"
                        }
                    ]
                }
            }
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


