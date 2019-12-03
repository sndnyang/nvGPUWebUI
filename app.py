import os
import json
from flask import Flask, request, render_template, jsonify, flash, redirect
from nvAPI import get_process_info

app = Flask(__name__)

version = 2.0


@app.route('/')
def index():
    process_list = get_process_info()

    meta = {'title': 'GPUs Web Monitor UI',
            'description': '',
            'keywords': ''}
    return render_template('index.html', meta=meta, version=version, p_list=process_list)


@app.route('/kill')
def kill_my_process():
    pid = request.json.get('pid')
    result = {'err_no': 0, 'err_msg': 'Success'}

    os.kill(pid)

    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5066)
