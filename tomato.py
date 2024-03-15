# -*- coding: utf-8 -*-
import datetime
from flask import Flask, request, jsonify, make_response
from celery import Celery
from task import play_music
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
    if data.get('bizname') and data.get('focus') == '番茄钟':
        response_content = {
            "versionid": "1.0",
            "is_end": False,
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": "Welcome to the Pomodoro Technique. You can start a 25-minute focus session by saying 'Start the timer'.",
                        "type": "1"
                    }
                ]
            }
        }
    elif data.get('start'):
        if start_time is None:  # 仅在start_time未初始化时设置它
            start_time = time.time()
        # Start playing music asynchronously for 25 minutes
        play_music('Study and Relax.mp3') 
        # play_music_async.delay('Study and Relax.mp3')  # Adjust the path as necessary
        response_content = {
            "versionid": "1.0",
            "is_end": False,
            "sequence": seq,
            "timestamp": int(time.time() * 1000),
            "directive": {
                "directive_items": [
                    {
                        "content": "You have focued for 25 minutes. Do you want to take a 5 minutes break?",
                        "type": "1"
                    }
                ]
            }
        }
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
                            "content": "You have focused for {} minutes.".format(int(time_lapse)),
                            "type": "1"
                        }
                    ]
                }
            }
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
                            "content": "Timer has not started. Please start the timer first",
                            "type": "1"
                        }
                    ]
                }
            }
    elif data.get('stop') and data.get('focus') == '番茄钟':
            response_content = {
                "versionid": "1.0",
                "is_end": True,  # 根据逻辑调整是否结束会话
                "sequence": seq,
                "timestamp": int(time.time() * 1000),
                "directive": {
                    "directive_items": [
                        {
                            "content": "I'll quit",
                            "type": "1"
                        }
                    ]
                }
            }
    response = make_response(jsonify(response_content))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080, threaded=True)


