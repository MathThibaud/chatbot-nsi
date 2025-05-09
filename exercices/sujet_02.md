## EXERCICE 1 (10 points)

Dans cet exercice, les tableaux sont représentés par des listes Python (`type list`).

Écrire en Python deux fonctions :

- `lancer`, de paramètre `n`, un entier positif, qui renvoie un tableau de `n` entiers obtenus aléatoirement entre 1 et 6 (1 et 6 inclus) ;
- `paire_6`, de paramètre `tab`, un tableau de `n` entiers compris entre 1 et 6, et qui renvoie un booléen égal à `True` si le nombre de 6 est supérieur ou égal à 2, `False` sinon.

On pourra utiliser la fonction `randint(a, b)` du module `random` dont la documentation officielle est la suivante :  
`random.randint(a, b)` renvoie un entier aléatoire `N` tel que `a <= N <= b`.

Exemples :
```python
>>> lancer1 = lancer(5)
>>> lancer1
[5, 6, 6, 2, 2]
>>> paire_6(lancer1)
True

>>> lancer2 = lancer(5)
>>> lancer2
[6, 5, 1, 6, 6]
>>> paire_6(lancer2)
True

>>> lancer3 = lancer(3)
>>> lancer3
[2, 2, 6]
>>> paire_6(lancer3)
False

>>> lancer4 = lancer(0)
>>> lancer4
[]
>>> paire_6(lancer4)
False
```

EXERCICE 2 (10 points)

On considère une image en 256 niveaux de gris que l’on représente par une grille de nombres, c’est-à-dire une liste composée de sous-listes toutes de longueurs identiques.

La largeur de l’image est la longueur d’une sous-liste.
La hauteur de l’image est le nombre de sous-listes.
Chaque élément des sous-listes est un entier entre 0 et 255 représentant l’intensité lumineuse d’un pixel.

Le négatif d’une image est l’image constituée des pixels x_n tels que x_n + x_i = 255, où x_i est le pixel correspondant dans l’image initiale.
La binarisation d’une image avec une valeur seuil s consiste à créer une image dont chaque pixel vaut 0 si x_i < s et 255 sinon.
Compléter les fonctions suivantes :

``python
def nombre_lignes(image):
    '''Renvoie le nombre de lignes de l'image'''
    return ...

def nombre_colonnes(image):
    '''Renvoie la largeur de l'image'''
    return ...

def negatif(image):
    '''Renvoie le négatif de l'image sous forme de liste de listes'''
    nouvelle_image = [[0 for k in range(nombre_colonnes(image))] for i in range(nombre_lignes(image))]
    for i in range(nombre_lignes(image)):
        for j in range(...):
            nouvelle_image[i][j] = ...
    return nouvelle_image

def binaire(image, seuil):
    '''Renvoie l’image binarisée'''
    nouvelle_image = [[0] * nombre_colonnes(image) for i in range(nombre_lignes(image))]
    for i in range(nombre_lignes(image)):
        for j in range(...):
            if image[i][j] < ...:
                nouvelle_image[i][j] = ...
            else:
                nouvelle_image[i][j] = ...
    return nouvelle_image
```


Exemple :


```python
img = [
    [20, 34, 254, 145, 6],
    [23, 124, 237, 225, 69],
    [197, 174, 207, 25, 87],
    [255, 0, 24, 197, 189]
]

>>> nombre_lignes(img)
4
>>> nombre_colonnes(img)
5
>>> negatif(img)
[[235, 221, 1, 110, 249], [232, 131, 18, 30, 186], [58, 81, 48, 230, 168], [0, 255, 231, 58, 66]]
>>> binaire(img, 120)
[[0, 0, 255, 255, 0], [0, 255, 255, 255, 0], [255, 255, 255, 0, 0], [255, 0, 0, 255, 255]
```