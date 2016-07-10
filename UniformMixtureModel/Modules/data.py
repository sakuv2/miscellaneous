#coding:utf-8
"""
データを生成する
"""
import scipy.stats as ss
import numpy as np

def GMM(mix=[1.], loc=[0.], scale=[1.], size=1):
    """ [関数] ガウス混合分布に従ったデータを生成する
    mix: {list of float} 混合係数
    loc: {list of float} 平均
    scale: {list of float} 標準偏差
    size: 生成するデータ数
    """
    w = np.random.choice(len(mix), size=size, p=mix)
    return [ss.norm.rvs(loc=loc[i], scale=scale[i]) for i in w]
    
def Gauss(loc=0., scale=1., size=1):
    """ [関数] ガウス分布に従った乱数を生成する
    loc:
    scale:
    size:
    return: 
    """
    return ss.norm.rvs(loc=loc, scale=scale, size=size)
    
def DataSet1(size=100):
    """ [関数] ガウス混合分布のデータセットを手軽に生成
    """
    
if __name__ == '__main__':
    print GMM()
    print Gauss()
    