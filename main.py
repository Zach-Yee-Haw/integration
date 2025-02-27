import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import timeit
import time


def Fonction_test(x):

    # Aire sous la courbe entre -5 et 5 = 200
    y = -2.5 * x**3 + 3 * x**2 + 7*x - 5

    return y

def Solution_analytique(x, b = 0):

    # Solution analytique à notre foction de test
    y = -2.5/4 * x**4 + x**3 + 7/2 * x**2 - 5 * x + b

    return y


def Integration_rectangles_python_base(fonction, X0, X1, n):

    """
    :param fonction: Fonction à intégrer
    :param X0: Première valeur de X
    :param X1: Dernière valeur de X
    :param n: Nombre de rectangles
    :return: L'aire sous la courbe
    """

    # Si les bornes sont inversée (x0 > x1), le signe de l'aire devra être inversé
    negatif = False
    x0 = X0
    x1 = X1

    if X0 > X1:

        negatif = True
        x0 = X1
        x1 = X0

    # On initialise notre aire, notre largeur de rectangles et notre position initiale
    aire = 0
    dx = (x1 - x0) / n
    x = x0 + dx/2

    # On ajoute l'aire arithmétique de chaque rectangle à l'aire totale
    for i in range(n):

        aire += dx * fonction(x)

        x += dx

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:

        aire = -aire

    # On retourne l'aire
    return aire


def Integration_trapezes_python_base(fonction, X0, X1, n):

    """
    :param fonction: Fonction à intégrer
    :param X0: Première valeur de X
    :param X1: Dernière valeur de X
    :param n: Nombre de rectangles
    :return: L'aire sous la courbe
    """

    # Si les bornes sont inversée (x0 > x1), le signe de l'aire devra être inversé
    negatif = False
    x0 = X0
    x1 = X1

    if X0 > X1:

        negatif = True
        x0 = X1
        x1 = X0

    # On initialise notre aire, notre largeur de trapèzes et notre position initiale
    aire = 0
    dx = (x1 - x0) / n
    x = x0

    # On calcule l'aire de chaque trapèze et on l'ajoute au total
    for i in range(n):

        # On calcul la valeur de la fonction aux points x et x + dx
        a = fonction(x)
        b = fonction(x + dx)



        if a > b:

            aire_a_ajouter = dx * b + (a - b) * dx / 2

        elif a == b:

            aire_a_ajouter = dx * a

        else:

            aire_a_ajouter = dx * a + (b - a) * dx / 2


        aire += aire_a_ajouter

        x += dx

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:

        aire = -aire

    # On retourne l'aire
    return aire


def Integration_simpson_python_base(fonction, X0, X1, n):

    """
    :param fonction: Fonction à intégrer
    :param X0: Première valeur de X
    :param X1: Dernière valeur de X
    :param n: Nombre de rectangles
    :return: Une liste contenant l'erreur de chaque méthode d'intégration
    """

    # Si les bornes sont inversée (x0 > x1), le signe de l'aire devra être inversé
    negatif = False
    x0 = X0
    x1 = X1

    if X0 > X1:

        negatif = True
        x0 = X1
        x1 = X0

    # On initialise notre aire, notre largeur de parabole et notre position initiale
    aire = 0
    dx = (x1 - x0) / n
    x = x0

    # On ajoute l'aire arithmétique de chaque parabole à l'aire totale
    for i in range(n):

        a = x
        b = x + dx
        ab_div2 = (a + b) / 2
        fa = fonction(a)
        fb = fonction(b)
        fab_div2 = fonction(ab_div2)

        aire += (b - a) / 6 * (fa + 4 * fab_div2 + fb)

        x += dx

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:

        aire = -aire

    # On retourne l'aire
    return aire


def Erreur_integration(x0, x1, n):

    """
    :param X0: Première valeur de X
    :param X1: Dernière valeur de X
    :param n: Nombre de rectangles
    :return:
    """

    resultat_analytique= Solution_analytique(x1) - Solution_analytique(x0)
    resultat_rectangles = Integration_rectangles_python_base(Fonction_test, x0, x1, n)
    resultat_trapezes = Integration_trapezes_python_base(Fonction_test, x0, x1, n)
    resultat_simpson = Integration_simpson_python_base(Fonction_test, x0, x1, n)

    erreur_rectangle = abs((resultat_rectangles-resultat_analytique)/resultat_analytique)
    erreur_trapezes = abs((resultat_trapezes - resultat_analytique) / resultat_analytique)
    erreur_simpson = abs((resultat_simpson - resultat_analytique) / resultat_analytique)

    return [erreur_rectangle, erreur_trapezes, erreur_simpson]
