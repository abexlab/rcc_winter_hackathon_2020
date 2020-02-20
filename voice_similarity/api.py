# -*- coding: utf-8 -*-
import os
import urllib.error
import urllib.request
import librosa, rwave
from flask import Flask, jsonify, abort, make_response, request
from engine import comparison


def webDL(link, file, mkdir_ok=True):
    ## -----*----- Webからダウンロード -----*----- ##
    try:
        with urllib.request.urlopen(link) as web_file:
            data = web_file.read()

            if mkdir_ok:
                    os.makedirs(os.path.dirname(file), exist_ok=True)

            with open(file, mode='wb') as local_file:
                local_file.write(data)

    except urllib.error.URLError as e:
        print(e)


def wav_build(file):
    ## -----*----- wavをビルド -----*----- ##
    wave, fs = librosa.load(file)
    wave *= 10000
    wave, _  = rwave.convert_fs(wave, fs, 8000)

    rwave.write_wave(file, wave, 8000)


api = Flask(__name__)


@api.route('/voice/calc', methods=['GET'])
def audio_similarity():
    ## -----*---- 音声の類似度を算出 -----*----- ##
    # パラメータ取得
    char_id = request.args.get('char_id')
    wav_url = request.args.get('url')

    # 比較対象の音声ファイル
    correct_file = 'audio/%s.wav' % char_id
    # 録音されたファイルをダウンロード
    webDL(wav_url, 'tmp/source.wav')
    wav_build('tmp/source.wav')

    # 類似度を算出
    score = comparison(correct_file, 'tmp/source.wav')

    return make_response(jsonify({'score': score}))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
