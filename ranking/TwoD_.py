# Abolfazl Asudeh April 2018
# http://asudeh.github.io

import math
from heapq import *
from ranking import basestuff_

heap = None
sweeper = None
discoveredAngles = None


def GetNext(Ui=[0, math.pi / 2]):
    global heap
    if heap is None:
        FindRanges(Ui)
    if len(heap) == 0:
        return None, None, None
    S, (theta1, theta2) = heappop(heap)
    theta = (theta1 + theta2) / 2
    R = basestuff_.rank([theta], isweight=False)
    return -S, R, theta


# -------------------------Internal Private Functions and Variables-------------------------#
def FindRanges(Ui=None):  # tested
    if Ui is None:
        Ui = [0, math.pi / 2]
    global heap, sweeper, discoveredAngles
    n = basestuff_.n
    discoveredAngles = set()
    heap = []
    sweeper = []
    Lp = list(basestuff_.rank([Ui[0]], isweight=False)[0])
    L = [0 for i in range(basestuff_.n)]
    for i in range(basestuff_.n):
        L[Lp[i]] = i
    for i in range(n - 1):
        checkNadd(Lp[i], Lp[i + 1], Ui)
    thetap = Ui[0]
    while len(sweeper) > 0:
        (theta, i) = heappop(sweeper)
        heappush(heap, (-(theta - thetap) / (Ui[1] - Ui[0]), (thetap, theta)))
        j = L[i]  # the index of t[i] in the ordered list Lp
        L[Lp[j + 1]] -= 1  # decrease the index of the item in position j+1 of the ordered list
        L[i] += 1
        Lp[j] = Lp[j + 1]
        Lp[j + 1] = i
        if j > 0:
            checkNadd(Lp[j - 1], Lp[j], Ui)
        if j + 2 < n:
            checkNadd(Lp[j + 1], Lp[j + 2], Ui)
        thetap = theta
    heappush(heap, (Ui[1] - thetap, (thetap, Ui[1])))


def checkNadd(i, j, Ui):
    global sweeper, discoveredAngles
    if basestuff_.dataset[i][0] < basestuff_.dataset[j][0] or basestuff_.dataset[i][1] < basestuff_.dataset[j][1]:
        theta = math.atan(
            (basestuff_.dataset[j][0] - basestuff_.dataset[i][0]) / (basestuff_.dataset[i][1] - basestuff_.dataset[j][1]))
        if Ui[0] < theta < Ui[1]:
            if theta not in discoveredAngles:
                heappush(sweeper, (theta, i))
                discoveredAngles.add(theta)
