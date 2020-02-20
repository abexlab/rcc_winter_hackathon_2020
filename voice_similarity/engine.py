# -*- coding:utf-8 -*-

import numpy as np
from sklearn.metrics import r2_score
import rwave
import math
from lib.LPC import *


def similarity(v1, v2):
    ### -----*----- ベクトルの決定係数 -----*----- ##
    score = r2_score(v1, v2)
    if score < 0.0:
        score = 0.0

    return score


def cos_sim(v1, v2):
    ## -----*----- ベクトルのコサイン類似度 -----*----- ##
    if len(v1)==0 or len(v2)==0:
        return 0.0
    score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    return score


def convert_wave(ori_file, to_file, fs, sec):
    ## -----*----- 音声ファイルのサンプリングレート・時間を変換 -----*----- ##
    # ori_file：変換対象のファイルパス
    # to_file ：変換後のファイルパス

    wave, rate = rwave.read_wave(ori_file)
    wave, _    = rwave.convert_fs(wave, rate, fs)
    wave, _    = rwave.convert_sec(wave, rate, sec)

    rwave.write_wave(to_file, wave, fs)


def comparison(file1, file2):
    ## -----*----- 類似度を算出 -----*----- ##
    score = {'mfcc': 0.0, 'lpc': 0.0}
    RATE = 8000
    FILE = 'tmp/calc.wav'

    # サンプリングレート・秒数をキャスト
    w1, fs1 = rwave.read_wave(file1)
    w2, fs2 = rwave.read_wave(file2)
    sec1 = len(w1) / fs1
    sec2 = len(w2) / fs2
    if sec2 < sec1/4.0:
        return int(1000*np.random.rand()) / 100.0
    convert_wave(file2, FILE, RATE, sec1)

    ## ===== MFCCで比較 ====================================
    # MFCCに変換
    mfcc1 = rwave.nomalize(rwave.to_mfcc(file1, RATE)).T
    mfcc2 = rwave.nomalize(rwave.to_mfcc(FILE, RATE)).T

    scores = []
    score['mfcc'] = 1.0
    for i in range(len(mfcc1)-1):
        re_mfcc = np.roll(mfcc1, i)
        scores.append(similarity(re_mfcc.T, mfcc2.T))
    for i in range(len(mfcc1.T)-1):
        re_mfcc = np.roll(mfcc1.T, i)
        score['mfcc'] *= cos_sim(re_mfcc.flatten(), mfcc2.flatten())
    score['mfcc'] = (score['mfcc'] + max(scores)) / 2


    ## ===== LPC分析 ====================================
    extractor = Identifer()
    lpc1 = extractor.lpc_spectral_envelope(file1)
    lpc2 = extractor.lpc_spectral_envelope(file2)
    v1 = np.append(lpc1['max'], lpc1['argrelmax']),\
         np.append(lpc1['min'], lpc1['argrelmin'])
    v2 = np.append(lpc2['max'], lpc2['argrelmax']),\
         np.append(lpc2['min'], lpc2['argrelmin'])

    n_max = min(len(v1[0]), len(v2[0]))
    n_min = min(len(v1[1]), len(v2[1]))
    v1_max, v2_max = v1[0][:n_max], v2[0][:n_max]
    v1_min, v2_min = v1[1][:n_min], v2[1][:n_min]
    score['lpc'] = cos_sim(v1_max, v2_max) * cos_sim(v1_min, v2_min)
    score['lpc'] = score['lpc'] ** 5
    score['lpc'] = 1 / (1 + math.e ** -(10*score['lpc'] - 6.0))

    ret = (score['mfcc'] * score['lpc'])
    ret = (1 / (1 + math.e**-ret) - 0.5) * 4.3

    # 精度を調整
    if   ret > 0.75:
        ret += np.random.rand() * 0.3
    elif ret > 0.70:
        ret += np.random.rand() * 0.15
    elif ret > 0.65:
        ret += np.random.rand() * 0.10
    elif ret > 0.40 and ret <= 0.45:
        ret *= np.random.randint(5, 10) / 10.0
    elif ret < 0.40:
        ret *= np.random.rand()

    if score['lpc'] > 0.9:
        ret = score['lpc']
    if score['mfcc'] < 0.5:
        ret *= score['mfcc'] * 2

    if ret > 1.0:  ret = 1.0
    # 少数第２位まで求める [%]
    ret = int(10000*ret) / 100

    return ret


if  __name__ == '__main__':
    # 決定係数
    print('gyuho:     %4.2f' % comparison('audio/1.wav', 'tmp/gyuho.wav'))
    print('お天気:    %4.2f' % comparison('audio/1.wav', 'tmp/onesan.wav'))
    print('純音:      %4.2f' % comparison('audio/1.wav', 'tmp/pi--.wav'))
    print('フリーザ1: %4.2f' % comparison('audio/1.wav', 'tmp/freeza1.wav'))
    print('フリーザ2: %4.2f' % comparison('audio/1.wav', 'tmp/freeza2.wav'))
    print('フリーザ3: %4.2f' % comparison('audio/1.wav', 'tmp/freeza3.wav'))
    print('きょうさん:%4.2f' % comparison('audio/1.wav', 'tmp/kyo--.wav'))
    print('謎の曲:    %4.2f' % comparison('audio/1.wav', 'tmp/song.wav'))
