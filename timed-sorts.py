import random
import math
import time
import statistics


def bubblesorted(v):
    sv = v.copy()
    for i in range(len(sv) + 1):
        for j in range(i, len(sv)):
            if sv[i] > sv[j]:
                sv[i], sv[j] = sv[j], sv[i]
    return sv


def countsorted(v):
    sv = []
    if not v:
        return v

    maxvalue = max(v)
    minvalue = min(v)
    negative = False

    if minvalue < 0:
        negative = True
        posfreq = [0 for i in range(maxvalue + 1)]
        negfreq = [0 for i in range(-minvalue + 1)]
    else:
        freq = [0 for i in range(maxvalue + 1)]

    if negative:
        for i in range(len(v)):
            if v[i] < 0:
                negfreq[v[i]] = negfreq[v[i]] + 1
            else:
                posfreq[v[i]] = posfreq[v[i]] + 1
    else:
        for i in range(len(v)):
            freq[v[i]] = freq[v[i]] + 1

    if negative:
        for i in range(-minvalue, 0, -1):
            for j in range(negfreq[i]):
                sv.append(-i)
        for i in range(maxvalue + 1):
            for j in range(posfreq[i]):
                sv.append(i)
    else:
        for i in range(minvalue, maxvalue + 1):
            for j in range(freq[i]):
                sv.append(i)
    return sv


def radixsorted(v):
    global base

    if not v:
        return v

    minvalue = min(v)
    maxvalue = max(v)
    negative = False

    if minvalue < 0:
        negative = True
        negdigits = []
        posdigits = []
    else:
        digits = []
    if negative:
        for j in range(base):
            negdigits.append([])
            posdigits.append([])
    else:
        for j in range(base):
            digits.append([])
    nr = 0
    ord = max(maxvalue, -minvalue)

    while ord:
        nr = nr + 1
        ord = ord // base

    for i in range(1, nr + 1):

        for j in range(base):
            if negative:
                negdigits[j] = []
                posdigits[j] = []
            else:
                digits[j] = []
        for number in v:
            if negative:
                if number < 0:
                    d = -number % base ** i // base ** (i - 1)
                    negdigits[d].append(number)
                else:
                    d = number % base ** i // base ** (i - 1)
                    posdigits[d].append(number)
            else:
                d = number % base ** i // base ** (i - 1)
                digits[d].append(number)

        if negative:
            posv = []
            negv = []
            for j in range(len(negdigits)):
                negv = negv + negdigits[j]
            for j in range(len(posdigits)):
                posv = posv + posdigits[j]
        else:
            v = []
            for j in range(len(digits)):
                 v = v + digits[j]

        if negative:
            v = negv + posv
            if i == nr:
                v = negv[::-1] + posv

    return v


def quicksorted(v):

    if not v:
        return v

    p = sorted([v[0], v[len(v) - 1], v[(len(v) - 1) // 2]])[1]
    #p = statistics.median((v[0], v[len(v) - 1], v[(len(v) - 1) // 2]))

    lesser, equal, greater = [], [], []
    for i in v:
        if i == p:
            equal.append(i)
        elif i < p:
            lesser.append(i)
        else:
            greater.append(i)

    return quicksorted(lesser) + equal + quicksorted(greater)

def mergesorted(v):

    if len(v) == 1:
        return v

    if len(v) > 1:
        mid = len(v) // 2
        left = mergesorted(v[:mid])
        right = mergesorted(v[mid:])

        i = j = 0
        new = []

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                new.append(left[i])
                i = i + 1
            else:
                new.append(right[j])
                j = j + 1

        if i < len(left):
            return new + left[i:]
        if j < len(right):
            return new + right[j:]


def verifysort(v):
    if v == sorted(v):
        return True
    return False

def measure_time(sortname, v):
    tstart = time.perf_counter()
    sv = sortname(v)
    tfin = time.perf_counter()
    return tfin-tstart, verifysort(sv)


def randomarray():
    v = []
    for i in range(5*10**6):
        v.append(math.floor(random.uniform(-(10**14), 10**14)))
    return v

def randomarrayargs(n, max, min):
    v = []
    for i in range(n):
        v.append(math.floor(random.uniform(min, max)))
    return v

base = 10
Sortlist = [sorted, quicksorted, radixsorted, mergesorted]

print("Enable bubblesort? (really long running times) (Y/N)")
answer = input().upper()
if answer == "Y":
    Sortlist = [bubblesorted] + Sortlist
print("Enable countsort? (last test will break due to memory constraints) (Y/N)")
answer = input().upper()
if answer == "Y":
    Sortlist.append(countsorted)

#r = randomarray()
t = open("tests.txt", "r")
for line in t.readlines():
    data = line.split()
    r = randomarrayargs(int(data[0]), int(data[1]), int(data[2]))
    print("n:", data[0], "|| max:", data[1], "|| min: ", data[2])
    for sort in Sortlist:
        exectime, sortcheck = measure_time(sort, r)
        print(sort, "executed in", exectime, "- Sorted correctly:", sortcheck)
    print("\n")
