from flask import Flask, request, jsonify
from celery import Celery
from task import play_music

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
    data = request.json
    if data.get('bizname') == '狗狗去哪' and data.get('focus') == 'Puppy':
        # Start playing music asynchronously for 25 minutes
        play_music('Study and Relax.mp3') 
        # play_music_async.delay('Study and Relax.mp3')  # Adjust the path as necessary
        response = {"message": "Music playing for 25 minutes"}
    else:
        response = {"message": "Music not playing"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080, threaded=True)


