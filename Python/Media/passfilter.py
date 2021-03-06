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


def myshow(x, y1, y2, y3, X1, X2, X3, fs):
    """ [関数] グラフで結果をみる
    """
    N = len(x)    # FFTのサンプル数

    X = np.fft.fft(x)
    freqList = np.fft.fftfreq(N, d=1.0 / fs)

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
    amplitudeSpectrum1 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X1]
    amplitudeSpectrum2 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X2]
    amplitudeSpectrum3 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X3]

    fig = figure(figsize=(10,10))

    # 波形を描画
    subplot(421)
    plot(range(0, N), x)
    axis([0, N, -0.5, 0.5])
    ylim(-0.05, 0.05)
    # xlabel("time [sample]")
    # ylabel("amplitude")
    
    # 振幅スペクトルを描画
    subplot(422)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum[:n], linestyle='-')
    axis([0, fs / 2, 0, 2])
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum[FFT]")

    # 波形を描画
    subplot(423)
    plot(range(0, N), y1)
    title("LPF")
    axis([0, N, -0.5, 0.5])
    ylim(-0.05, 0.05)
    # xlabel("time [sample]")
    # ylabel("amplitude")

    # 振幅スペクトルを描画
    subplot(424)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum1[:n], linestyle='-')
    title("LPF")
    axis([0, fs / 2, 0, 2])
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum[DFT]")
    
    # 波形を描画
    subplot(425)
    plot(range(0, N), y2)
    title("HPF")
    axis([0, N, -0.5, 0.5])
    ylim(-0.05, 0.05)
    # xlabel("time [sample]")
    # ylabel("amplitude")

    # 振幅スペクトルを描画
    subplot(426)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum2[:n], linestyle='-')
    title("HPF")
    axis([0, fs / 2, 0, 2])
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum[DFT]")
    
    # 波形を描画
    subplot(427)
    plot(range(0, N), y3)
    title("BPF")
    axis([0, N, -0.5, 0.5])
    ylim(-0.05, 0.05)
    xlabel("time [sample]")
    # ylabel("amplitude")

    # 振幅スペクトルを描画
    subplot(428)
    n = len(freqList) / 2  # FFTの結果は半分まで見ればOK
    plot(freqList[:n], amplitudeSpectrum3[:n], linestyle='-')
    title("BPF")
    axis([0, fs / 2, 0, 2])
    xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum[DFT]")

    #figure(figsize=(10, 7))
    fig.tight_layout()
    
    savefig('zu1.eps', format='eps', dpi=1000)


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
    F = [1] * K + [0] * (N - 2 * K) + [1] * K
    Y = [i * j for i, j in zip(X, F)]
    return Y


def hpf(X, threshold, fs):
    """ ﾊｲﾊﾟｽﾌｨﾙﾀｰ
    X: 周波数領域の奴
    threshold: 閾値[Hz]
    fs: サンプリング周波数
    """
    N = len(X)
    K = int(threshold * N / fs)
    F = [0] * K + [1] * (N - 2 * K) + [0] * K
    Y = [i * j for i, j in zip(X, F)]
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
    L = int(S * N / fs)
    H = int(G * N / fs)
    F = [0] * L + [1] * (H - L) + [0] * (N - 2 * H) + [1] * (H - L) + [0] * L
    Y = [i * j for i, j in zip(X, F)]
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
    x = x[8000:8512]  # 1s[16000]
    # DFT
    X = dft(x)

    # Filter
    Y1 = lpf(X, 1000, fs)
    Y2 = hpf(X, 4000, fs)
    Y3 = bpf(X, 1000, 4000, fs)

    # IFFT
    y1 = ifft(Y1)
    y2 = ifft(Y2)
    y3 = ifft(Y3)

    # plot
    myshow(x, y1, y2, y3, Y1, Y2, Y3, fs)


def testFFT():
    # 音声読み込み
    # fsサンプリング周波数16000[Hz], len(x)160000(10[s])
    x, fs = openWave("record.wav")
    x = x[:2**17]  # 8.19[s]だけ変換する

    # FFT
    X = fft(x)

    # Filter
    Y1 = lpf(X, 1000, fs)
    Y2 = hpf(X, 4000, fs)
    Y3 = bpf(X, 1000, 4000, fs)

    # IFFT
    y1 = ifft(Y1)
    y2 = ifft(Y2)
    y3 = ifft(Y3)

    # 音声を保存
    saveWave(y1, fs, 16, "lpf.wav")
    saveWave(y2, fs, 16, "hpf.wav")
    saveWave(y3, fs, 16, "bpf.wav")


if __name__ == '__main__':
    testDFT()
    testFFT()
