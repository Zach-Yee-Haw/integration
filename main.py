import numpy as np
from matplotlib import pyplot as plt
import timeit
import time




def Fonction_test(x):

    y = 5*x**2 + 2*x - 5

    return y




def Integration_rectangles_python_base(fonction, X0, X1, n):

    """
    :param fonction: Fonction à intégrer
    :param X0: Première valeur de X
    :param X1: Deuxième valeur de X
    :param n: Nombre de rectangles
    :return: L'aire sous la courbe
    """

    negatif = False
    x0 = X0
    x1 = X1

    if X0 > X1:

        negatif = True
        x0 = X1
        x1 = X0

    x = x0
    aire = 0
    dx = (x1 - x0) / n
    x = x0 + dx/2

    for i in range(n):

        aire += dx * fonction(x)

        x += dx

    if negatif == True:

        aire = -aire

    return aire
