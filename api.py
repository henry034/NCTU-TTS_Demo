import os
import flask
from flask import request
from subprocess import check_output
import json
from flask_cors import *

app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
txt_path = './ntpu-tts/test.txt'
wav_path = './ntpu-tts/output.wav'
log_path = './logs/log.txt'
cmd = './run_gmm.sh'

def tts_log(data, stdout):
    log_str = '[TEXT] {} \t[SR] {}\n[STDOUT] {}\n'.format(
                data['text'], data['SR'], stdout)
    with open(log_path, 'a') as f:
        f.write(log_str)
        

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello</h1>"


@app.route('/tts', methods=['POST'])
def tts():
    if not request.json:
        abort(400)
    else:
        data = request.data
        data = json.loads(data)
        with open(txt_path, 'w') as f:
            f.write('{}'.format(data['text']))
        SR = float(data['SR'])
        ISR = 1/SR
        stdout = check_output([cmd, str(ISR)]).decode('utf-8')
        tts_log(data, stdout)	
        res = flask.send_file(
                wav_path, 
                mimetype="audio/wav", 
                #as_attachment=True, 
                #attachment_filename="output.wav",
                cache_timeout=0)
        
        return res


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')
