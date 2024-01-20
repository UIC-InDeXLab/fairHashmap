import math
from heapq import *
from ranking_util import basestuff


def initialize():
    global n, sweeper, Lp, L, is_first, discoveredAngles, Ui
    n = basestuff.n
    print(n)
    Lp = None  # Lp contains the current ranking
    L = None  # the reverse list that for every tuple i, returns its rank in the current ranking
    sweeper = None  # the sweeper heap (priority queue)
    discoveredAngles = None
    Ui = None
    is_first = True  # a temp variable


def GetNext():  # Updates the ranking to the next one
    # outputs the swap index (J) in the current ranking
    global n, sweeper, Lp, L, is_first
    if is_first:
        if Lp is None:  # initialization
            run_first()
        is_first = False
        return (
            Lp,
            -1,
            0,
        )  # negative one means that this is the first ranking and no rank-swap has yet happened
    if len(sweeper) > 0:
        (theta, i) = heappop(sweeper)
        j = L[i]  # the index of t[i] in the ordered list Lp
        # the following lines swap Lp[j] and Lp[j+1]
        L[
            Lp[j + 1]
        ] -= 1  # decrease the index of the item in position j+1 of the ordered list
        L[i] += 1
        # print("before",Lp[j],Lp[j + 1])
        Lp[j] = Lp[j + 1]
        Lp[j + 1] = i
        # print("after",Lp[j],Lp[j + 1])
        if j > 0:
            checkNadd(Lp[j - 1], Lp[j], Ui)
        if j + 2 < basestuff.n:
            checkNadd(Lp[j + 1], Lp[j + 2], Ui)
        return Lp, j, theta  # the index on which the rank-swap happened
    return None, None, None  # no more rankings


def checkNadd(
    i, j, Ui
):  # check if i and j swap rank later, and if so, add the swap angle to the heap
    global sweeper, discoveredAngles
    if (
        basestuff.dataset[i][0] < basestuff.dataset[j][0]
        or basestuff.dataset[i][1] < basestuff.dataset[j][1]
    ):
        theta = math.atan(
            (basestuff.dataset[j][0] - basestuff.dataset[i][0])
            / (basestuff.dataset[i][1] - basestuff.dataset[j][1])
        )
        if Ui[0] < theta < Ui[1]:
            if theta not in discoveredAngles:
                heappush(sweeper, (theta, i))
                discoveredAngles.add(theta)


def run_first(_Ui=None):
    global n, sweeper, discoveredAngles, Lp, L, Ui
    Ui = [0, math.pi / 2] if _Ui is None else _Ui
    discoveredAngles = set()
    sweeper = []  # the sweeper heap (priority queue)
    # Lp contains the ranking
    Lp = list(basestuff.rank([Ui[0]], isweight=False))
    L = [
        0 for i in range(basestuff.n)
    ]  # the reverse list that for every tuple i, returns its rank in the current ranking
    for i in range(basestuff.n):
        L[Lp[i]] = i
    for i in range(basestuff.n - 1):
        checkNadd(Lp[i], Lp[i + 1], Ui)
