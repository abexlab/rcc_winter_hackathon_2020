# -*- coding:utf-8 -*-
import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal
from pylab import *


def autocorr(x, nlags=None):
    """自己相関関数を求める
    x:     信号
    nlags: 自己相関関数のサイズ（lag=0からnlags-1まで）
           引数がなければ（lag=0からlen(x)-1まですべて）
    """
    N = len(x)
    if nlags == None: nlags = N
    r = np.zeros(nlags)
    for lag in range(nlags):
        for n in range(N - lag):
            r[lag] += x[n] * x[n + lag]
    return r

def LevinsonDurbin(r, lpcOrder):
    """Levinson-Durbinのアルゴリズム
    k次のLPC係数からk+1次のLPC係数を再帰的に計算して
    LPC係数を求める"""
    # LPC係数（再帰的に更新される）
    # a[0]は1で固定のためlpcOrder個の係数を得るためには+1が必要
    a = np.zeros(lpcOrder + 1)
    e = np.zeros(lpcOrder + 1)

    # k = 1の場合
    a[0] = 1.0
    a[1] = - r[1] / r[0]
    e[1] = r[0] + r[1] * a[1]
    lam = - r[1] / r[0]

    # kの場合からk+1の場合を再帰的に求める
    for k in range(1, lpcOrder):
        # lambdaを更新
        lam = 0.0
        for j in range(k + 1):
            lam -= a[j] * r[k + 1 - j]
        lam /= e[k]

        # aを更新
        # UとVからaを更新
        U = [1]
        U.extend([a[i] for i in range(1, k + 1)])
        U.append(0)

        V = [0]
        V.extend([a[i] for i in range(k, 0, -1)])
        V.append(1)

        a = np.array(U) + lam * np.array(V)

        # eを更新
        e[k + 1] = e[k] * (1.0 - lam * lam)

    return a, e[-1]


class Identifer(object):
    def __init__(self):
        ## ----*----- コンストラクタ -----*----- ##
        self.rate = 8000


    def read_wavfile(self, file):
        ## -----*----- 音声ファイル読み込み -----*----- ##
        wf = wave.open(file, 'r')
        fs = wf.getframerate()
        x = wf.readframes(wf.getnframes())
        x = np.frombuffer(x, dtype="int16") / 32768.0  # (-1, 1)に正規化
        wf.close()
        return x, float(fs)


    def preEmphasis(self, signal, p):
        ## -----*----- プリエンファシスィルタ -----*----- ##
        # 係数 (0.97, -p) のFIRフィルタを作成
        return scipy.signal.lfilter([1.0, -p], 1, signal)

    def spectrum(self, s, a, e, fs, file):
        ## -----*----- LPC係数の振幅スペクトルを求める -----*----- ##
        fscale = np.fft.fftfreq(self.rate, d=1.0 / fs)[:self.rate // 2]
        # オリジナル信号の対数スペクトル
        spec = np.abs(np.fft.fft(s, self.rate))
        logspec = 20 * np.log10(spec)

        # LPC対数スペクトル
        w, h = scipy.signal.freqz(np.sqrt(e), a, self.rate, "whole")
        lpcspec = np.abs(h)
        loglpcspec = 20 * np.log10(lpcspec)

        # バンドパスフィルタ
        loglpcspec = loglpcspec[100:1000]

        ret = {
            'argrelmax': scipy.signal.argrelmax(loglpcspec)[0],
            'argrelmin': scipy.signal.argrelmin(loglpcspec)[0],
            'max': np.amax(loglpcspec),
            'min': np.amin(loglpcspec),
            'lpc': loglpcspec
        }

        return ret


    def lpc_spectral_envelope(self, file):
        ## -----*----- 音声をロード -----*----- ##
        wav, fs = self.read_wavfile(file)
        t = np.arange(0.0, len(wav) / fs, 1 / fs)
        # 音声波形の中心部分を切り出す
        center = len(wav) / 2  # 中心のサンプル番号
        cuttime = 0.04  # 切り出す長さ [s]
        s = wav[int(center - cuttime / 2 * fs): int(center + cuttime / 2 * fs)]
        # プリエンファシスフィルタをかける
        p = 0.97  # プリエンファシス係数
        s = self.preEmphasis(s, p)
        # ハミング窓をかける
        hammingWindow = np.hamming(len(s))
        s = s * hammingWindow
        # LPC係数を求める
        #    lpcOrder = 12
        lpcOrder = 32
        r = autocorr(s, lpcOrder + 1)
        a, e = LevinsonDurbin(r, lpcOrder)

        return self.spectrum(s, a, e, fs, file)


if __name__ == "__main__":
    obj = Identifer()
    print(obj.lpc_spectral_envelope('tmp/source.wav'))
    print(obj.lpc_spectral_envelope('audio/フリーザ.wav'))
    exit(0)
