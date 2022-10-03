from numpy import exp, sqrt, e, cos, pi


def ackley(x, y, a=20, b=0.2, c=pi * 2):
    res = (
        -a
        * exp(
            (
                -b * sqrt(1 / 2 * (x * x + y * y))
                - exp(1 / 2 * (cos(c * x) + (cos(c * y))))
            )
        )
        + a
        + e
    )
    return res
