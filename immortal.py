#!/usr/bin/env python

from math import cosh, exp
from pprint import pprint

def count(m, n, loss, max):
    total = 0

    for i in range(m):
        for j in range(n):
            total += i ^ j

    return total


def explore(m, n):
    total = 0

    for i in range(m):
        total += (i ^ n)

    return total
'''
for m in range(15):
    print(explore(m, 0), explore(m, 1), explore(m, 2), explore(m, 3), explore(m, 4), explore(m, 5), explore(m, 6))


a = [[explore(m, n) for n in range(20)] for m in range(10)]

for row in a:
    print(*(str(i).rjust(4, ' ') for i in row))


for x in range(2, 10):
    #print(count(x, 2, None, None))
    #print(x*(x + 2)*exp(x) + cosh(x))
    #(1 + 3*x^2)/((1 - x)^3 * (1 + x))
    a = (1 + (3 * (x * x))) / ( ( (1-x) ** 3 ) * (1+x) )
    print(a)'''

#0->1, 1->2, 2->4, 3->4, 4->8, 5->8, 6->8, 7->8, 8->16

def heighest_bit(n): 
    if (n == 0): 
        return 1
  
    msb = 0
    while (n > 0): 
        n = int(n / 2)
        msb += 1
  
    return (1 << msb)

#total_for_row = quick_sum(n, multiple of heighest_bit(n)) + slow_sum(starting at remainder to end)

def quick_sum(x):
    return x * (x-1) // 2

def slow_sum(start, end, n):
    if end < start:
        return 0

    total = 0

    for i in range(start, end):
        total += i ^ n

    return total

def get_sum(m, n):
    high_bit = heighest_bit(n)
    multiple = (m // high_bit) * high_bit

    bulk = quick_sum(multiple)
    remainder = slow_sum(multiple, m, n)

    return bulk + remainder


def count_faster(m, n):
    total = 0

    for i in range(n):
        total += get_sum(m, i)

    return total

for i in range(10):
    print(count_faster(i, 2))