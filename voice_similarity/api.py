# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, abort, make_response, request
from engine import comparison

api = Flask(__name__)


@api.route('/voice/calc', methods=['GET'])
def audio_similarity():
    ## -----*---- 音声の類似度を算出 -----*----- ##
    file = 'audio/%s.wav' % request.form['name']
    wav_link = request.form['url']
    dl_file = ''

    # 類似度を算出
    score = comparison(file, dl_file)

    result = {'score': score}
    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
