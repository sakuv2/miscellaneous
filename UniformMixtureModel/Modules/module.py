# encoding:utf-8
"""
よく使うかもしれない関数を置いておくところ
"""
import numpy as np
import scipy.special as sp

def Instruction(condition):
    """ [関数] 指示関数引数が真なら1を偽なら0を返す
    condition: {bool}
    return: {int}
    """
    return 1 if condition else 0


def XZ(X, Z):
    """ [関数] XをZに合わせて仕分ける
    X: {list of float} データ集合(N次元)
    Z: {list of float} 潜在変数集合(N次元)
    return1: {list of list of float} XZ=[[],[],...]
    return2: {list of float} n=[n0,n1,...]
    """
    K = max(Z) + 1
    XZ = [[] for i in xrange(K)]
    n = [0 for i in xrange(K)]
    for i in xrange(len(Z)):
        XZ[Z[i]].append(X[i])
        n[Z[i]] += 1
    return XZ, n

def NZ(Z):
    """ [関数] Zから各クラスの所属数を計算
    Z: {list of float} 潜在変数集合(N次元)
    return: {list of float} n=[n0,n1,...]
    """
    K = max(Z) + 1
    n = [0 for i in xrange(K)]
    for i in xrange(len(Z)):
        n[Z[i]] += 1
    return n
    
def Ewln(Z,a):
    """ [関数] イーウェンスの抽出公式の対数
    Z: {list of float} 潜在変数集合(N次元)
    a: {float} 集中度パラメータ
    return: {float} 確率値
    """
    n = NZ(Z)
    K = len(n)
    N = len(Z)
    
    p1 = sum([sp.gammaln(nk) for nk in n])
    p2 = sum([np.log(a + i) for i in xrange(N)])
    return K * np.log(a) + p1 - p2
    