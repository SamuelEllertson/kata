#!/usr/bin/env python

from operator import itemgetter
from math import sqrt

def distance(tup1, tup2):
    return sqrt( (tup1[0] - tup2[0])**2 + (tup1[1] - tup2[1])**2)

def bruteforce(points):
    smallest = 10**10
    candidates = points[:2]

    for i, tup1 in enumerate(points):
        for j, tup2 in enumerate(points[i+1:]):
            dist = distance(tup1, tup2)

            if dist < smallest:
                smallest = dist
                candidates = tup1, tup2

    return candidates

def closest_pair(points):
    n = len(points)

    if n <= 3:
        return bruteforce(points)

    points = sorted(list(points), key=itemgetter(0))

    left, center, right = points[0:n//2], points[n//2], points[n//2:]

    closest_left, closest_right = closest_pair(left), closest_pair(right)
    dist_left, dist_right = distance(*(closest_left)), distance(*(closest_right))
    candidates1 = closest_left if dist_left < dist_right else closest_right
    upper_bound = min(dist_left, dist_right)

    strip = sorted([pair for pair in points if abs(pair[0] - center[0]) <= upper_bound], key=itemgetter(1))

    smallest = upper_bound

    for i in range(0, n):
        j = i + 1
        while j < len(strip) and ((strip[j][1] - strip[i][1]) < smallest):
            dist = distance(strip[j], strip[i])

            if dist < smallest:
                smallest = dist
                candidates2 = strip[j], strip[i]

            j += 1

    return candidates1 if upper_bound <= smallest else candidates2

points = (
  (2,2), # A
  (2,8), # B
  (5,5), # C
  (6,3), # D
  (6,7), # E
  (7,4), # F
  (7,9)  # G
)
a = closest_pair(points)

print(a)