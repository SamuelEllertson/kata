#!/usr/bin/env python

def generate_set(x, y, x_exr, y_exr):
    reachable = {x+y: f"({x_exr}+{y_exr})", x-y: f"({x_exr}-{y_exr})", y-x: f"({y_exr}-{x_exr})", x*y: f"({x_exr}*{y_exr})"}

    try:
        reachable[x/y] = f"({x_exr}/{y_exr})"
    except ZeroDivisionError:
        pass

    try:
        reachable[y/x] = f"({y_exr}/{x_exr})"
    except ZeroDivisionError:
        pass

    return reachable


def combine(reachable_1, reachable_2, starting_dict=None):

    combined = starting_dict if starting_dict is not None else {}

    for value1, expression1 in reachable_1.items():
        for value2, expression2 in reachable_2.items():

            combined.update(generate_set(value1, value2, expression1, expression2))

    return combined

def get_reachable(values):

    #Base case: return easily computable reachable dict 
    if len(values) == 1:
        return {values[0]: values[0]}
    elif len(values) == 2:
        return generate_set(values[0], values[1], values[0], values[1])

    reachable = {}

    for tup1, tup2 in complements(values):
        combine(get_reachable(tup1), get_reachable(tup2), starting_dict=reachable)

    return reachable

def complements(values):
    if len(values) == 3:
        x, y, z = values

        yield (x,), (y, z)
        yield (y,), (x, z)
        yield (z,), (x, y)

    elif len(values) == 4:
        w, x, y, z = values

        yield (w,), (x, y, z)
        yield (x,), (w, y, z)
        yield (y,), (w, x, z)
        yield (z,), (w, x, y)

        yield (w, x), (y, z)
        yield (w, y), (x, z)
        yield (w, z), (x, y)
        yield (x, y), (w, z)
        yield (x, z), (w, y)
        yield (y, z), (w, x)

def equal_to_24(a,b,c,d):
    reachable = get_reachable((a,b,c,d))

    if 24 in reachable:
        return reachable[24]

    return "It's not possible!"


def main():
    #a = generate_set(1, 2, 1, 2)
    #print(a)
    #b = combine(3, a)
    #print(b)


    print(equal_to_24(1000,2,2,4))



if __name__ == '__main__':
    main()





