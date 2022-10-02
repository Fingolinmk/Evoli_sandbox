from cmath import nan
from operator import itemgetter
from random import uniform, choice
from typing import Callable
from random import gauss


def start_randomly(
    quality_function,
    number_of_individuals: int = 10,
    x_range=(-10, 10),
    x_sigma=1,
    y_range=(-10, 10),
    y_sigma=1
):
    ret = []
    for i in range(number_of_individuals):
        child = {
            "x": uniform(x_range[0], x_range[1]),
            "y": uniform(y_range[0], y_range[1]),
            "x_sigma": x_sigma,
            "y_sigma": y_sigma
        }
        child["z"] = quality_function(child["x"], child["y"])
        ret.append(child)
    ret = sorted(ret, key=itemgetter('z'))
    return ret


def recombinate(generation: list, offspring: int) -> list:
    offspring_gen = []
    for i in range(offspring):
        parent1 = choice(generation)
        parent2 = choice(generation)
        child = parent1
        child["x"] = (parent1["x"]+parent2["x"])/2
        child["y"] = (parent1["y"]+parent2["y"])/2
        child["z"] = nan
        offspring_gen.append(child)
    return offspring_gen


def mutate(generation: list) -> list:
    mutated_gen = []
    for elm in generation:
        elm["x"] = elm["x"]+gauss(0, elm["x_sigma"])
        elm["y"] = elm["y"]+gauss(0, elm["y_sigma"])

        elm["x_sigma"] = elm["x_sigma"]+gauss(0, elm["x_sigma"])
        elm["y_sigma"] = elm["y_sigma"]+gauss(0, elm["y_sigma"])

        mutated_gen.append(elm)
    return mutated_gen


def select_best(generation: list, survial_size: int, quality_function: Callable) -> list:
    for elm in generation:
        elm["z"] = quality_function(elm["x"], elm["y"])
    sorted_gen = sorted(generation, key=itemgetter('z'))
    return sorted_gen[0:survial_size]
