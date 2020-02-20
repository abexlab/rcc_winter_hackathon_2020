# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, abort, make_response, request
from engine import comparison

api = Flask(__name__)


@api.route('/voice/calc', methods=['POST'])
def audio_similarity():
    ## -----*---- 音声の類似度を算出 -----*----- ##
    file = 'audio/%s.wav' % request.form['name']
    wav = request.files['wavFile']

    # 類似度を算出
    score = comparison(file, wav)

    result = {'score': score}
    return make_response(jsonify(result))


@api.route('/voice/delete', methods=['DELETE'])
def audio_delete():
    ## -----*---- キャラクターを削除 -----*----- ##
    file = 'audio/%s.wav' % request.form['character']
    os.remove(file)

    return make_response(jsonify({}))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
