# Puissance3
C
rée l'IA du jeu puissance 3 ( 5 col x 4 lignes)

requiert le module mariadb

calcule l'evaluation de chaque partie et l'enregistre dans une base de donnée sous la forme
position (id_position INT, eval INT) et coups (id_coup, id_position_depart, id_position_arrive)

le plateau est representé par un tuple de longueur 19, obtenu en parcourant par ligne le plateau à partir du coin superieur gauche, comme chaque entier du tuple ne peut prendre que 3 valeurs (rouge, jaune ou vide), on represente aussi le plateau comme un nombre en base 3 (2:rouge, 1:vide, 0:jaune) obtenu à partir du tuple (dnas le quel on a 1:rouge, 0:vide, -1: jaune)
