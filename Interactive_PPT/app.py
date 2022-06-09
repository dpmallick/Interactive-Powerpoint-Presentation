# from gesture import *
from audio import *
from Gesture_2 import *
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

# @app.route('/gesture')
# def gesture():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture')
def gesture():
    return Response(Gesture(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio')
def audio():
    audio_call()
    return render_template('audio.html')

if __name__=="__main__":
    app.run(debug=True)