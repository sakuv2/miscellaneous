# coding:utf-8
"""""""""""""""""""""""""""
p-median問題における動的計画法
"""""""""""""""""""""""""""
# define(テストデータ)
w = [5, 1, 4, 2, 7, 3, 6, 3, 9, 5]
l = [1, 2, 2, 1, 3, 7, 3, 2, 1]
#w = [2, 1, 2, 1, 2]
#l = [2, 1, 2, 2]
#w = [2, 1, 2]
#l = [2, 1]
n = len(w)
k = 5

# d(iからjまでの距離)の計算
# d = []
# f = lambda i, j: d[i][j - 1] + \
#     l[j - 1] if i < j else (0 if i == j else d[j][i])
# for i in xrange(n):
#     d.append([])
#     for j in xrange(n):
#         d[i].append(f(i, j))
# 上記の処理を無理やり1行？で書いたもの ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
d = [(q.append([]), [(q[i].append(
    q[i][j - 1] + l[j - 1] if i < j else (0 if i == j else q[j][i])),
    q[i][j])[1] for j in xrange(n)])[1] for q in [[]] for i in xrange(n)]

# 全探索アルゴリズム ==============================================================


def search_f(i, j, s):  # 順方向探索
    # 終了条件
    if i == n:
        return 0
    if j == n:
        return 1e99
    if s == 0:
        return sum([w[x] * d[x][j] for x in xrange(i, n)])
    # 再帰条件
    if i <= j:  # 下に行くならi=j+1まで、右にいくならj=j+1
        return min(search_f(j + 1, j, s - 1) + sum([w[x] * d[x][j] for x in xrange(i, j)]),
                   search_f(i, j + 1, s))
    elif i > j:  # 下に行くならi=i+1、右にいくならj=iまで
        return min(search_f(i + 1, j, s) + w[i] * d[i][j], search_f(i, i, s))


def search_b(i, j, s):  # 逆方向探索
    # 終了条件
    if i < 0:
        return 0;
    if j < 0:
        return 1e99
    if s == 0:
        return sum([w[x] * d[x][j] for x in xrange(0, i + 1)])
    # 再帰条件
    if i >= j:  # 上に行くならi=j-1まで、左にいくならj=j-1
        return min(search_b(j - 1, j, s - 1) + sum([w[x] * d[x][j] for x in xrange(j + 1, i + 1)]),
                   search_b(i, j - 1, s))
    elif i < j:  # 上に行くならi=i-1、左にいくならj=iまで
        return min(search_b(i - 1, j, s) + w[i] * d[i][j], search_b(i, i, s))


# 漸化式を考える ================================================================
"""
c(i, j, s): 出発地i~nで、s個の施設を施設候補地j~nへ設置した時の最小コスト
c(i, j, s)をc(j+1, j, s- ), c(i, j+1, s), c(i+1, j, s), c(i, i, s)で表す？
"""

# 約n*n*kの行列を埋める


def DynamicPrograming():
    # 初期化
    dp = [[[None for s in xrange(k + 1)] for j in xrange(n + 1)]
          for i in xrange(n + 1)]
          
    # メインループ
    for i in reversed(xrange(n + 1)):
        for j in reversed(xrange(n + 1)):
            for s in xrange(k + 1):
                if i >= n:
                    dp[i][j][s] = 0
                elif j >= n or (s <= 0 and i <= j):
                    dp[i][j][s] = 1e99
                elif i <= j and s > 0:  # 上三角行列
                    dp[i][j][s] = min(dp[j + 1][j][s - 1] +
                                      sum([w[x] * d[x][j]
                                           for x in xrange(i, j)]),
                                      dp[i][j + 1][s])
                elif i > j:  # 下三角行列
                    dp[i][j][s] = min(dp[i + 1][j][s] + w[i] * d[i][j],
                                      dp[i][i][s])
    return dp[0][0][k]

print search_f(0, 0, k)
print search_b(n - 1, n - 1, k)
print DynamicPrograming()
