from operator import itemgetter
from random import uniform


def start_randomly(
    quality_function,
    number_of_individuals: int = 10,
    x_range=(-10, 10),
    y_range=(-10, 10),
):
    ret = []
    for i in range(number_of_individuals):
        child = {
            "x": uniform(x_range[0], x_range[1]),
            "y": uniform(y_range[0], y_range[1]),
        }
        child["z"] = quality_function(child["x"], child["y"])
        ret.append(child)
    ret = sorted(ret, key=itemgetter('z'))
    return ret


def select_best(generation: list, survial_size: int) -> list:
    sorted_gen = sorted(generation, key=itemgetter('z'))
    return sorted_gen[0:survial_size]
