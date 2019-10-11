#!/usr/bin/env python

from pprint import pprint

cycles_of_last_digit = [
    [0],        #0
    [1],        #1
    [6,2,4,8],  #2
    [1,3,9,7],  #3
    [6,4],      #4              
    [5],        #5
    [6],        #6       
    [1,7,9,3],  #7
    [6,8,4,2],  #8
    [1, 9],     #9
]

digits = {
    (0, 2): [0],
    (0, 4): [0],
    (1, 2): [1],
    (1, 4): [1],
    (2, 2): [0],
    (2, 4): [0, 2],
    (3, 2): [1],
    (3, 4): [1, 3],
    (4, 2): [0],
    (4, 4): [0],
    (5, 2): [1],
    (5, 4): [1],
    (6, 2): [0],
    (6, 4): [0, 2],
    (7, 2): [1],
    (7, 4): [1, 3],
    (8, 2): [0],
    (8, 4): [0],
    (9, 2): [1],
    (9, 4): [1]
}

def last_digit(arr):

    clean, return_val = clean_arr(arr)
    if return_val is not None:
        return return_val

    base, exponents = split_arr(clean)

    return multi_pow(base, exponents, 10)

def clean_arr(arr):
    if len(arr) == 0:
        return None, 1
    elif arr[0] == 1:
        return None, 1

    no_ones = []
    no_ones.append(arr[0] % 10)

    #first pass: get everything until first 1 (not including), everything after is irrelevant
    for exp in arr[1:]:
        if exp == 1:
            break
        no_ones.append(exp)

    #only 1 element -> done cleaning
    if len(no_ones) == 1:
        return no_ones, None

    #otherwise we now handle 0's
    
    clean = []
    
    #Phase 1: trim everything after first string of 0's, they are irrelevant
    found_zero = False
    for value in no_ones:
        if not found_zero and value != 0:
            clean.append(value)
        elif not found_zero and value == 0:
            clean.append(value)
            found_zero = True
        elif found_zero and value == 0:
            clean.append(value)
        elif found_zero and value != 0:
            break

    #Phase 2: evaluate any 0's at end of list
    while len(clean) > 1:
        right = clean.pop()
        left = clean.pop()

        if left == 0 and right == 0:
            clean.append(1)
        elif left != 0 and right == 0:
            clean.append(1)
        elif left == 0 and right != 0:
            clean.append(0)
        elif left != 0 and right != 0:
            clean.append(left)
            clean.append(right)
            break
    
    #Phase 3: Remove any 1's at the end
    while len(clean) > 1 and clean[-1] == 1:
        clean.pop()

    #if only 1 value left, thats our answer % 10
    if len(clean) == 1:
        return None, clean[0] % 10

    return clean, None

def split_arr(exponents):
    return exponents[0], exponents[1:]

def multi_pow(base, exponents, mod):
    
    if len(exponents) == 0:
        return base % mod

    #initial call -> base already gauarenteed to be 0 <= base <= 9
    if mod == 10:
        assert 0 <= base <= 9

        cycle_length = len(cycles_of_last_digit[base])

        #Case: only 1 option for last digit -> return it
        if cycle_length == 1:
            return cycles_of_last_digit[base][0]

        #Case: 2 or 4 cycle
        if cycle_length == 2 or cycle_length == 4:
            cycle_offset = multi_pow(*split_arr(exponents), cycle_length)

            return cycles_of_last_digit[base][cycle_offset]

    #Case: mod is 2 -> only one option for return
    if mod == 2:
        return digits[(base % 10, 2)][0]

    #Case: mod is 4 -> two options for 3,7 and 2,6, one option for the rest
    if mod == 4:
        base %= 4

        #Case: base is 3 or 7 -> need cycle offset
        if base in [3,7]:
            cycle_offset = multi_pow(*split_arr(exponents), 2)

            return digits[(base, 4)][cycle_offset]

        #Case: base is 2 or 6 -> return is 2 only if exponent tower evals to 1, all other values result in 0
        if base in [2,6]:
            if is_one(exponents):
                return 2
            else:
                return 0

        #Case: base is anything else -> only 1 option -> return it
        return digits[(base, 4)][0]

    #should never be here
    assert False
            
def is_one(exponents):
    if len(exponents) == 0:
        return True

    if exponents[0] == 1:
        return True

    return False


def main():
    
    pprint(cycles_of_last_digit)
    pprint(digits)
    print("\n\n")
    
    for i in range(0, 10):
        print(pow(11, i, 4))
    
    a = [2, 11, 3]
    print(f"final digit: {last_digit(a)}")

    '''
    for i in range(20):
        for j in range(12):
            for k in range(4):
                if (i ** (j ** k)) % 10 != last_digit([i, j, k]):
                    print(i, j, k)
    '''

def last_digit2(lst):
    n = 1
    for x in reversed(lst):
        n = x ** (n if n < 4 else n % 4 + 4)
    return n % 10

if __name__ == '__main__':
    #main()
    test_data = [
        ([], 1),
        ([0, 0], 1),
        ([0, 0, 0], 0),
        ([1, 2], 1),
        ([3, 4, 5], 1),
        ([4, 3, 6], 4),
        ([7, 6, 21], 1),
        ([12, 30, 21], 6),
        ([2, 2, 2, 0], 4),
        ([937640, 767456, 981242], 0),
        ([123232, 694022, 140249], 6),
        ([499942, 898102, 846073], 6)
    ]

    for test_input, test_output in test_data:
        assert last_digit2(test_input) == test_output