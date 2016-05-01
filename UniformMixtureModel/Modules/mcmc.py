# coding:utf-8
"""
簡単なMCMCをmodule化する
"""
import numpy as np


def discrete1mcmc(lnp, m, s, I=[-np.inf, np.inf], burn_in=100, num=1):
    """ [関数] 離散1次元のマルコフ連鎖モンテカルロ
    提案分布を一様分布qとしてサンプリングする
    qは平均を前のサンプル値、幅を2sとする

    lnp: {lambda x} サンプリングしたい正規化されていない確率分布の対数
    m: {int} 初期値
    s: {int} 提案分布の幅の半分
    I: {list of int} 定義域の設定
    burn_in: {int} 初めに廃棄するサンプル数
    num: {int} 出力するサンプル数
    return: {list of int} サンプル集合
    """
    z = []
    burn_count = 0
    z_o = m
    while len(z) < num :
        # 提案分布からの候補点サンプリング
        a = z_o - s if z_o - s >= I[0] else I[0]
        b = z_o + s if z_o + s <= I[1] else I[1]
        z_n = np.random.randint(a, b)
        # 棄却ステップ
        p = np.random.uniform(0, 1)
        if p <= min(1.0, np.exp(lnp(z_n) - lnp(z_o))):  # 受理
            if burn_in > burn_count
                burn_count += 1
            else:
                z.append(z_n)
            z_o = z_n
        else:
            if burn_in > burn_count
                burn_count += 1
            else:
                z.append(z_o)
            z_o = z_o
    return z