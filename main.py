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

    plot_x = np.linspace(x0,x1, 1000)
    plot_y = Fonction_test(plot_x)
    plt.plot(plot_x, plot_y, color='red')
    # On ajoute l'aire arithmétique de chaque rectangle à l'aire totale

    for i in range(n):

        aire += dx * fonction(x)
        x += dx

        plot_x = np.append(plot_x, x)
        plot_y = np.append(plot_y, Fonction_test(x))
        plt.bar(x,fonction(x), width=dx, color='blue', alpha=0.5, edgecolor='blue')


    plt.title("Intégration rectangle")
    plt.show()



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

    #Plot de la courbe exacte
    plot_x = np.linspace(x0,x1,1000)
    plot_y = Fonction_test(plot_x)
    plt.plot(plot_x, plot_y, color="red")

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

        #Plot de la methode d'integration trapezoidale
        method_x = [x, x, x+dx, x+dx]
        method_y = [0, a, b, 0]
        plt.fill(method_x, method_y,color='blue', alpha=0.5)


        if a > b:

            aire_a_ajouter = dx * b + (a - b) * dx / 2

        elif a == b:

            aire_a_ajouter = dx * a

        else:

            aire_a_ajouter = dx * a + (b - a) * dx / 2


        aire += aire_a_ajouter

        x += dx

    plt.title("Intégration trapézoidale")
    plt.show()


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

    # Plot de la courbe exacte
    plot_x = np.linspace(x0, x1, 1000)
    plot_y = Fonction_test(plot_x)
    plt.plot(plot_x, plot_y, color="red")

    # On initialise notre aire, notre largeur de parabole et notre position initiale
    aire = 0
    dx = (x1 - x0) / (n)
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


        method_x = np.linspace(a,b,100)
        method_y = ( fa * (method_x - ab_div2) * (method_x - b) / ((a - ab_div2) * (a - b)) +
            fab_div2 * (method_x - a) * (method_x - b) / ((ab_div2 - a) * (ab_div2 - b)) +
            fb * (method_x - a) * (method_x - ab_div2) / ((b - a) * (b - ab_div2)))

        plt.plot(method_x,method_y, color="blue")
        plt.fill_between(method_x, method_y, color='blue',alpha=0.5)

        x += dx
    plt.title("Intégration simpson")
    plt.show()
    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:

        aire = -aire

    # On retourne l'aire
    return aire


def Integration_rectangles_numpy(fonction, X0, X1, n):
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

    # On initialise nos variables dépendantes et indépendantes
    aire = 0
    dx = (x1 - x0) / n
    X = np.arange(x0 + dx / 2, x1, dx)
    Y = X.copy()
    Y = fonction(Y)

    # Plot de la courbe exacte
    plot_x = np.linspace(x0, x1, 1000)
    plot_y = Fonction_test(plot_x)

    plt.plot(plot_x, plot_y, color="red")
    plt.bar(X,Y, width=dx, color='blue', alpha=0.5, edgecolor='blue')
    plt.title("Intégration rectangles numpy")

    plt.show()

    # On calcule l'aire de chaque trapèze puis on en fait la sommation
    aire = Y.copy()*dx
    aire = sum(aire)

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:
        aire = -aire

    # On retourne l'aire
    return aire


def Integration_trapezes_numpy(fonction, X0, X1, n):
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

    # On initialise nos variables dépendantes et indépendantes
    aire = 0
    dx = (x1 - x0) / n
    Xa = np.arange(x0, x1, dx)
    Xb = np.arange(x0+dx, x1+dx, dx)
    Ya = Xa.copy()
    Yb = Xb.copy()
    Ya = fonction(Ya)
    Yb = fonction(Yb)

    # On calcule l'aire de chaque trapèze puis on en fait la sommation
    aire = Ya.copy()*dx + (Yb.copy() - Ya.copy()) * dx / 2
    aire = sum(aire)




    # Plot de la methode d'integration trapezoidale numpy
    method_x = np.append(Xa,X1) #Il ne manque que la dernière valeur de X dans notre vecteur Xa, donc on la rajoute
    method_y = fonction(method_x)
    plt.plot(method_x, method_y, color='blue')
    plt.vlines(method_x, 0, method_y,color="blue")
    plt.fill_between(method_x, method_y, color="blue", alpha=0.5, edgecolor="blue")

    # Plot de la courbe exacte
    plot_x = np.linspace(x0, x1, 1000)
    plot_y = Fonction_test(plot_x)
    plt.plot(plot_x, plot_y, color="red")

    plt.title("Intégration trapézoidale numpy")
    plt.show()
    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:
        aire = -aire

    # On retourne l'aire
    return aire


def Integration_simpson_numpy(fonction, X0, X1, n):
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

    # On initialise nos variables dépendantes et indépendantes
    aire = 0
    dx = (x1 - x0) / n
    Xa = np.arange(x0, x1, dx)
    Xb = np.arange(x0+dx, x1+dx, dx)
    Xc = np.arange(x0+dx/2, x1+dx/2, dx)
    Ya = Xa.copy()
    Yb = Xb.copy()
    Yc = Xc.copy()
    Ya = fonction(Ya)
    Yb = fonction(Yb)
    Yc = fonction(Yc)



    # Plot de la courbe exacte
    plot_x = np.linspace(x0, x1, 1000)
    plot_y = Fonction_test(plot_x)
    plt.plot(plot_x, plot_y, color="red")

    method_x = np.linspace(Xa, Xb, 100)
    method_y = (Ya * (method_x - Xc) * (method_x - Xb) / ((Xa - Xc) * (Xa - Xb)) +
                Yc * (method_x - Xa) * (method_x - Xb) / ((Xc - Xa) * (Xc - Xb)) +
                Yb * (method_x - Xa) * (method_x - Xc) / ((Xb - Xa) * (Xb - Xc)))
    plt.plot(method_x, method_y, color="blue")
    plt.title("Intégration simpson numpy")
    plt.show()

    # On calcule l'aire de chaque parabole puis on en fait la sommation
    aire = (Xb.copy() - Xa.copy()) / 6 * (Ya.copy() + 4 * Yc.copy() + Yb.copy())
    aire = sum(aire)

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:
        aire = -aire

    # On retourne l'aire
    return aire


def Integration_trapezes_scipy(fonction, X0, X1, n):
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

    # On initialise nos variables dépendantes et indépendantes
    dx = (x1 - x0) / n
    X = np.arange(x0, x1 + dx, dx)
    Y = X.copy()
    Y = fonction(Y)

    # On calcul notre aire à l'aide de scipy
    aire = sp.integrate.trapezoid(Y, x=X, dx=dx)

    # Si les bornes sont inversée, on inverse le signe de l'aire
    if negatif:
        aire = -aire

    # On retourne l'aire
    return aire


def Integration_simpson_scipy(fonction, X0, X1, n):
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

    # On initialise nos variables dépendantes et indépendantes
    dx = (x1 - x0) / n
    X = np.arange(x0, x1 + dx, dx)
    Y = X.copy()
    Y = fonction(Y)

    # On calcul notre aire à l'aide de scipy
    aire = sp.integrate.simpson(Y, x=X, dx=dx)


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

    resultat_rectangles_python_base = Integration_rectangles_python_base(Fonction_test, x0, x1, n)
    resultat_rectangles_numpy = Integration_rectangles_numpy(Fonction_test, x0, x1, n)

    resultat_trapezes_python_base = Integration_trapezes_python_base(Fonction_test, x0, x1, n)
    resultat_trapezes_numpy = Integration_trapezes_numpy(Fonction_test, x0, x1, n)
    resultat_trapezes_scipy = Integration_trapezes_scipy(Fonction_test, x0, x1, n)

    resultat_simpson_python_base = Integration_simpson_python_base(Fonction_test, x0, x1, n)
    resultat_simpson_numpy = Integration_simpson_numpy(Fonction_test, x0, x1, n)
    resultat_simpson_scipy = Integration_simpson_scipy(Fonction_test, x0, x1, n)


    erreur_rectangle_python_base = abs((resultat_rectangles_python_base-resultat_analytique)/resultat_analytique)
    erreur_rectangle_numpy = abs((resultat_rectangles_numpy - resultat_analytique) / resultat_analytique)

    erreur_trapezes_python_base = abs((resultat_trapezes_python_base - resultat_analytique) / resultat_analytique)
    erreur_trapezes_numpy = abs((resultat_trapezes_numpy - resultat_analytique) / resultat_analytique)
    erreur_trapezes_scipy = abs((resultat_trapezes_scipy - resultat_analytique) / resultat_analytique)

    erreur_simpson_python_base = abs((resultat_simpson_python_base - resultat_analytique) / resultat_analytique)
    erreur_simpson_numpy = abs((resultat_simpson_numpy - resultat_analytique) / resultat_analytique)
    erreur_simpson_scipy = abs((resultat_simpson_scipy - resultat_analytique) / resultat_analytique)


    return [[erreur_rectangle_python_base, erreur_rectangle_numpy],
            [erreur_trapezes_python_base, erreur_trapezes_numpy, erreur_trapezes_scipy],
            [erreur_simpson_python_base, erreur_simpson_numpy, erreur_simpson_scipy]]


def main():
    #Integration_rectangles_python_base(Fonction_test, -5, 5, 100)
    #Integration_trapezes_python_base(Fonction_test,-1,1,50)
    #Integration_simpson_python_base(Fonction_test, -5, 5, 3)
    #Integration_rectangles_numpy(Fonction_test, -5, 5, 100)
    #Integration_trapezes_numpy(Fonction_test, -1, 1, 50)
    #Integration_simpson_numpy(Fonction_test, -1, 1, 50)
    Integration_trapezes_scipy(Fonction_test, -1, 1, 50)
    #print(Erreur_integration(-1, 1, 10))
    #print(2 ** 64)

main()
