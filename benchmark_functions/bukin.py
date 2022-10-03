from numpy import sqrt


def bukin(x: float, y: float, a: float = 100, b: float = 0.01, c: float = 10):
    return 100*sqrt(abs(y-0.01*x**2)) + 0.01*abs(x+10)
