# coding:utf-8
"""
データを生成する
ひたすら無駄にラップするライブラリ日本語化
"""
import scipy.stats as ss
import numpy as np


def MixtureGaussian(mix=[1.], loc=[0.], scale=[1.], size=1):
    """ [関数] 1次元混合ガウス分布に従ったデータを生成する
    MixtureGaussian(mix=[1.], loc=[0.], scale=[1.], size=1)
    mix: {list of float} 混合係数
    loc: {list of float} 平均
    scale: {list of float} 標準偏差
    size: {int} 生成するデータ数
    return: {list of float}
    """
    w = np.random.choice(len(mix), size=size, p=mix)
    return [ss.norm.rvs(loc=loc[i], scale=scale[i]) for i in w]


def Gaussian(loc=0., scale=1., size=1):
    """ [関数] 1次元ガウス分布に従った乱数を生成する
    Gauss(loc=0., scale=1., size=1)
    loc: {float} 平均
    scale: {float} 標準偏差
    size: {int} 生成するデータ数
    return: {list of float}
    """
    return ss.norm.rvs(loc=loc, scale=scale, size=size)


def Uniform(loc=0.5, scale=1., size=1):
    """ [関数] １次元連続一様分布に従った乱数を生成します
    Uniform(loc=0.5, scale=1., size=1)
    loc: {float} 中心位置(平均) 
    scale: {float} 幅
    size: {int} 生成するデータ数
    return: {list of float}
    """
    return ss.uniform.rvs(loc=loc - scale / 2., scale=scale, size=size)


def Choice(a=["ura", "omote"], p=[0.8, 0.2], size=10):
    """ [関数] 与えられた配列の中から任意の確率で選びます(カテゴリカル分布)
    Choice(a=["ura","omote"], p=[0.8,0.2], size=10)
    a: {list of anything} 選択するリスト
    p: {list of float} aを選択する確率(当然aと同数でなけらばならない，合計が1でなければならない)
    size: {int} 生成するデータ数
    return: {list of anything}
    """
    return np.random.choice(a, size=size, p=p)


def Bernoulli(p=0.5, size=10):
    """ [関数] ベルヌーイ分布にしたがった乱数を生成する
    Bernoulli(p=0.5, size=10)
    p: {float} 1を生成する確率
    size: {int} 生成するデータ数
    return: {list of 0or1}
    """
    return ss.bernoulli.rvs(p, size=size)


def Beta(a=2., b=2., size=10):
    """ [関数] ベータ分布に従う乱数を生成する
    Beta(a=2., b=2., size=10)
    a: {float} 形状母数(a>0)
    b: {float} 形状母数(b>0)
    size: {int} 生成するデータ数
    """
    return ss.beta.rvs(a, b, size=size)
    

def Gamma():
    """ [関数] ガンマ分布に従う乱数を生成する
    Beta(a=2., b=2., size=10)
    a: {float} 形状母数(a>0)
    b: {float} 形状母数(b>0)
    size: {int} 生成するデータ数
    """
    return ss.gamma.rvs()


def DataSet1(size=100):
    """ [関数] ガウス混合分布のデータセットを手軽に生成
    """

if __name__ == '__main__':
    print GMM()
    print Gauss(size=2)
    print Uniform(size=10)
    print Choice()
    print Bernoulli()
    print Beta()
