# coding:utf-8
"""
混合一様分布を仮定した確率密度推定
パラメータは一様分布の全体での位置を決定するものと
一様分布の幅を決定するものの二つ。
それぞれ、独立な0~1一様分布を事前分布とする。
"""
import numpy as np
import scipy.integrate as ig
from Modules import module as mo
from Modules import mcmc as mc


def model(x, m, r, A, V, h):
    """ [関数] モデル関数(一様分布関数)
    x: {flout} データ
    m: {float} 一様分布の位置のパラメータ(0~1)
    r: {float} 一様分布の幅のパラメータ(0~1)
    A: {float} 最小データ値
    V: {float} 最大データ値 - 最小データ値
    h: {flout} 一様分布の幅の最大値
    return: {float} 確率密度値
    """
    c = A + m * V - r * h <= x <= A + m * V + r * h
    return 1. / (2 * h) * mo.Instruction(c)


def likelifoodln(X, Z, m, r, A, V, h):
    """ [関数] 対数尤度関数
    X: {list of float} データ集合(N次元)
    Z: {list of float} 潜在変数集合(N次元)
    m: {list of float} パラメータ集合1(K次元)
    r: {list of float} パラメータ集合2(K次元)
    return: {float} 対数確率密度値
    """
    lp = sum([np.log(model(xi, m[zi], r[zi], A, V, h)
                     for xi, zi in zip(X, Z))])
    return lp


def posteriorln(X, Z, m, r, a, A, V, h):
    """ [関数] 対数事後確率(目的関数)
    X: {list of float} データ集合(N次元)
    Z: {list of float} 潜在変数集合(N次元)
    m: {list of float} パラメータ集合1(K次元)
    r: {list of float} パラメータ集合2(K次元)
    a: {float} CRPの集中度パラメータ
    return: {float} 対数事後確率値
    """
    return mo.Ewln(Z, a) + likelifoodln(X, Z, m, r, A, V, h)


def Sln(Xk, A, V, h):
    """ [関数] パラメータ消去の積分の値
    Xk: {list of float} データ集合のうちクラスkに所属するもの
    return: {float} 面積
    """
    xa = min(Xk)
    xb = max(Xk)
    n = len(Xk)
    f = 0 if n == 1 else (1 if n == 2 else 2)
    a = max(1. / V * (xb - A - h), 0.0)
    b = 1. / (2 * V) * (xa + xb - 2 * A)
    c = min(1. / V * (xa - A + h), 1.0)

    fa = lambda x: 1. / h * (V * x - (xa - A))
    fb = lambda x: -1. / h * (V * x - (xb - A))

    s = lambda x: -1. / (n - 1) * x ** -(n - 1)
    ta1 = lambda x: h / V * fa(x) * {np.log(fa(x)) - 1}
    ta2 = lambda x: -h / (V * (n - 1)) * np.log(fa(x))
    ta3 = lambda x: h / (V * (n - 1) * (n - 2)) * fa(x) ** -(n - 2)
    tb1 = lambda x: -h / V * fb(x) * {np.log(fb(x)) - 1}
    tb2 = lambda x: h / (V * (n - 1)) * np.log(fb(x))
    tb3 = lambda x: -h / (V * (n - 1) * (n - 2)) * fb(x) ** -(n - 2)
    ta = [ta1, ta2, ta3]
    tb = [tb1, tb2, tb3]
    sfa = lambda x: -1. / (n - 1) * fa(x) ** -(n - 1)
    sfb = lambda x: -1. / (n - 1) * fb(x) ** -(n - 1)

    ss = s(1) * (c - a) - (tb[f](b) - tb[f](a)) - (ta[f](c) - ta[f](b))

    return np.log(ss)


def likelifoodln2(X, Z, A, V, h):
    """ [関数] 対数尤度関数からパラメータを積分消去したもの
    X: {list of float} データ集合(N次元)
    Z: {list of float} 潜在変数集合(N次元)
    return: {float} 対数確率密度値
    """
    XZ = mo.XZ(X, Z)[0]
    N = len(X)
    return -N * np.log(2 * h) + sum([Sln(Xk, A, V, h) for Xk in XZ])


def posteriorln2(X, Z, a, A, V, h):
    """ [関数] 対数事後確率からパラメータを積分消去したもの(目的関数2)
    X: {list of float} データ集合(N次元)
    Z: {list of float} 潜在変数集合(N次元)
    a: {float} CRPの集中度パラメータ
    return: {float} 対数事後確率値
    """
    return mo.Ewln(Z, a) + likelifoodln2(X, Z, A, V, h)


def conditionalln(k, i, Z, X, m, r, a, A, V, h):
    """ [関数] 潜在変数一つの条件付き事後分布
    p(zi=k|Z_i,X,m,r,a) i番目のzがクラスkになる確率
    k: {int} クラス
    i: {int} 取り除くi番目
    Z: {list of int} 潜在変数集合
    X: {list of float} データ集合
    """
    if k <= max(Z):
        return np.log(model(X[i], m[k], r[k], A, V, h))
    else:
        return Sln([X[i]], A, V, h) - np.log(2 * h)


def conditionalln2(k, i, Z, X, a, A, V, h):
    """ [関数] 潜在変数一つの条件付き事後分布からパラメータを積分消去したもの
    p(zi=k|Z_i,X,a) i番目のzがクラスkになる確率
    k: {int} クラス
    i: {int} 取り除くi番目
    Z: {list of int} 潜在変数集合
    X: {list of float} データ集合
    """
    pass
