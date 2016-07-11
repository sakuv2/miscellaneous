# coding: utf-8
import wave
import struct
import numpy as np
from pylab import *



def openWave(path):
    """ [FUNCTION] waveを読み込む
    path: .wavファイルパス
    return x, fs: -1~1のデータ配列, サンプリング周波数
    """
    # waveファイルの読み込み
    wf = wave.open(path, "r")
    # フレーム数
    fs = wf.getframerate()
    # 全てのフレームをバイナリ読み込み
    x = wf.readframes(wf.getnframes())
    # int16で読み込み正規化
    x = frombuffer(x, dtype="int16") / 32768.0
    # 閉じる
    wf.close()
    return x, fs


def saveWave(x, fs, bit, path):
    """ [FUNCTION] データをwaveにして保存する
    x: データ配列{-1~1}
    fs: サンプリング周波数
    bit: bit
    path: 保存先パス 
    """
    y = [int(v * 32767.0) for v in x]
    y = struct.pack("h" * len(y), *y)
    wf = wave.open(path, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(y)
    wf.close()


def myshow(x, y, X2, fs):
    N = len(x)    # FFTのサンプル数

    X = np.fft.fft(x)
    freqList = np.fft.fftfreq(N, d=1.0 / fs)

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
    amplitudeSpectrum2 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X2]

    # 波形を描画
    subplot(411)
    plot(range(0, N), x)
    axis([0, N, -0.5, 0.5])
    # xlabel("time [sample]")
    ylabel("amplitude")

    # 波形を描画
    subplot(412)
    plot(range(0, N), y)
    axis([0, N, -0.5, 0.5])
    xlabel("time [sample]")
    ylabel("amplitude[LPF]")

    # 振幅スペクトルを描画
    subplot(413)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum[:n], linestyle='-')
    axis([0, fs / 2, 0, 2])
    # xlabel("frequency [Hz]")
    ylabel("amplitude spectrum[FFT]")

    # 振幅スペクトルを描画
    subplot(414)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum2[:n], linestyle='-')
    axis([0, fs / 2, 0, 2])
    xlabel("frequency [Hz]")
    ylabel("amplitude spectrum2[DFT]")

    show()


def dft(x):
    """ 離散フーリエ変換
    return X: list of complex
    """
    N = len(x)
    W = [[complex(np.cos(2 * np.pi * k * n / N), -np.sin(2 * np.pi * k * n / N))
          for n in xrange(N)]
         for k in xrange(N)]
    W = np.matrix(W)
    X = W * np.matrix(x).T
    return X.T.tolist()[0]


def idft(X):
    """ 逆離散フーリエ変換
    return x: list of float
    """
    N = len(X)
    W = [[complex(np.cos(2 * np.pi * k * n / N), np.sin(2 * np.pi * k * n / N))
          for k in xrange(N)]
         for n in xrange(N)]
    W = np.matrix(W)
    x = (1. / N) * W * np.matrix(X).T
    x = [v.real for v in x.T.tolist()[0]]
    return x


def lpf(X, threshold, fs):
    """ ﾛｰﾊﾟｽﾌｨﾙﾀｰ
    X: 周波数領域の奴
    threshold: 閾値[Hz]
    fs: サンプリング周波数
    """
    N = len(X)
    K = int(threshold * N / fs)
    Y = X[:K] + [complex(0, 0)] * (N - K)
    return Y
    

def bpf(X, S, G, fs):
    """ バンドパスフィルター
    S[Hz]からG[Hz]だけを切り出します
    X: 周波数領域の奴
    S: 切り出す最初
    G: 切り出す終わり
    fs: サンプリング周波数
    """
    N = len(X)
    s1 = int(S * N / fs)
    g1 = int(G * N / fs)
    Y = [complex(0.0)] * s1 + X[s1:g1] + [complex(0, 0)] * (N - g1)
    return Y


def fft(x):
    """ [FUNCTION] FFT
    return X: {list of complex}
    """
    n = len(x)
    y = [0] * n
    if n == 1:
        return x
    x0 = [x[2 * i + 0] for i in xrange(n / 2)]
    x1 = [x[2 * i + 1] for i in xrange(n / 2)]
    x0 = fft(x0)
    x1 = fft(x1)

    zeta = complex(np.cos(2 * np.pi / n), np.sin(2 * np.pi / n))
    pow_zeta = 1
    for i in xrange(n):
        y[i] = x0[i % (n / 2)] + pow_zeta * x1[i % (n / 2)]
        pow_zeta *= zeta
    return y


def ifft(X):
    """ [FUNCTION] FFT
    return x: {list of float}
    """
    def recursive(x):
        n = len(x)
        y = [0] * n
        if n == 1:
            return x
        x0 = [x[2 * i + 0] for i in xrange(n / 2)]
        x1 = [x[2 * i + 1] for i in xrange(n / 2)]
        x0 = recursive(x0)
        x1 = recursive(x1)

        zeta = complex(np.cos(2 * np.pi / n), -np.sin(2 * np.pi / n))
        pow_zeta = 1
        for i in xrange(n):
            y[i] = x0[i % (n / 2)] + pow_zeta * x1[i % (n / 2)]
            pow_zeta *= zeta
        return y
    N = len(X)
    y = recursive(X)
    y = [v.real * (1. / N) for v in y]
    return y


def testDFT():
    x, fs = openWave("record.wav")
    x = x[:512]  # 1s[16000]
    # DFT
    X = dft(x)

    # Low Pass Filter
    Y = lpf(X, 16000, fs)

    # IDFT
    y = idft(Y)

    # plot
    myshow(x, y, Y, fs)

    # 音声を保存
    saveWave(y, fs, 16, "test.wav")


def testFFT():
    x, fs = openWave("record.wav")
    x = x[:2**17]  # 5s

    # FFT
    X = fft(x)

    # Band Pass Filter
    Y = bpf(X, 1000, 4000, fs)

    # IFFT
    y = ifft(Y)

    # plot
    myshow(x, y, X, fs)

    # 音声を保存
    saveWave(y, fs, 16, "test.wav")


if __name__ == '__main__':
    testFFT()
