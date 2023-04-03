from math import ceil
import mariadb

conn = mariadb.connect(
    user="root",
    password="",
    host="127.0.0.1",
    port=3307,
    database="puissance3_test"
)


def test_plateau(plateau): # (Bool, winner) (si la partie est finie ou non, winner = -1 ou 1 ou 0 )
    for a,b,c in [[0,1,2],[1,2,3],[4,5,6],[5,6,7],[8,9,10],[9,10,11],[12,13,14],[13,14,15],[16,17,18],[17,18,19],[0,4,8],[1,5,9],[2,6,10],[3,7,11],[4,8,12],[5,9,13],[6,10,14],[7,11,15],[8,12,16],[9,13,17],[10,14,18],[11,15,19],[2, 5, 8], [3, 6, 9], [6, 9, 12], [7, 10, 13], [10, 13, 16], [11, 14, 17],[1, 6, 11], [0, 5, 10], [5, 10, 15], [4, 9, 14], [9, 14, 19], [8, 13, 18]]:
        if plateau[a]+plateau[b]+plateau[c] == 3:
            return (True,1) # victoire des bleus
        elif plateau[a]+plateau[b]+plateau[c] ==-3:
            return (True,-1) # victoire des rouges
    for i in range(4):
        if L[i]==0:
            return (False, 0) # pas fini

    return (True,0) # match nul

#### PLATEAU ET INT #################
# le plateau (4 largeur et 5 hauteur) est presenté par un tuple de taille 20
# (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0)
# les 4 derniers elements representent la ligne tout en bas
def plateau_to_int(L):
    s=0
    for i in range(4*5):
        s+= (L[i]+1)*3**i
    return s

def int_to_plateau(n):
    l=[]
    while n>0:
        l.append(n%3)
        n = n//3
    
    l += [0 for k in range(20 - len(l))]
    l = [k-1 for k in l]
    return l
############################


############## DIVERS ##############
def aff_plateau(L):
    for i in range(5):
        for j in range(4):
            print(f"{L[4*i+j] : 4}", end = "")
        print()


def creer_nouv_plateau(L: tuple, col: int, n: int):
    """
    L = le plateau a modifier
    q = le num de la colonne dans lequel mettre le jeton
    n = le jeton
    """
    i=4

    while L[4*i+col]!=0 and i>=1: i-=1
    case = 4*i+col
    return L[:case]+(n,)+L[case+1:]

##################################

# -1 : case rouge, 0 : case vide, 1 : case bleu; les rouges commencent
def nombre_de_coups(l):
    s=0
    for i in l:
        if i==0: s+=1
    return 20-s
############ MAIN ################

d = dict()
data_coup = []

def evaluate(plateau): 
    if plateau in d.keys():
        return d[plateau]
    

    #on teste si la partie est finie
    e,f = test_plateau(plateau)
    if e:
        n = nombre_de_coups(plateau)
        a = (f==1) * (20 - n) + (f==-1) * (-20-n) # et si f=0, a=0
        d[plateau] =  a
        return a

    #on determine le tour
    tour = (sum(plateau) == 0)

    evaluation = -20 if tour == 1 else 20
    for i in range(4): # pour tous les coups possibles
        if plateau[i]==0:# si la colonne n'est pas complete (le cas avec toutes les colonnes completes est traité dans 'test_plateau()')
            
            nouv_plateau = creer_nouv_plateau(plateau, i,2*tour-1)
            data_coup.append((plateau_to_int(plateau), plateau_to_int(nouv_plateau)))

            e = evaluate(nouv_plateau)
            if tour and e>evaluation:# si cest au tour des bleus (1)
                evaluation = e
            elif (not tour) and e<evaluation:
                evaluation = e
                
    d[plateau]=evaluation
    return evaluation
L = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

print("c'est parti (c'est normal si ca prend un peu de temps)")
evaluate(L)
# #transforme le dictionnaire de la forme { (plateau) : eval, ...} en liste [ (plateau_to_int(plateau), eval), ...]
data_plateau_eval,i = [None for k in range(len(d))],0
for plateau,eval in d.items():
    data_plateau_eval[i] = (plateau_to_int(plateau), eval)
    i+=1

# on enregistre dans une BDD
def enregister_BDD():
    global data_plateau_eval, data_coup

    # data_plateau_eval_example = [
    #     (2452263203, 1), 
    #     "..."
    # ]

    # decoupage de l'enregistremment de la liste en paquet de 1000 👍
    n = len(data_plateau_eval)
    for i in range(ceil(n/1000)) : 
        curseur = conn.cursor()

        temp = data_plateau_eval[i*1000 : (i+1)*1000 if (i+1)*1000<n else n]
        
        request = "INSERT INTO positions (id_position, eval) VALUES (%s, %s)"
        curseur.executemany(request, temp)
        conn.commit()
    
    ###########################################

    # data_coup_example = [
    #     ("position_depart", "position_fin")
    #     (2452263203, 2437914296), 
    #     "..."
    # ]
    n = len(data_coup)
    for i in range(ceil(n/1000)) : 
        curseur = conn.cursor()

        temp = data_coup[i*1000 : (i+1)*1000 if (i+1)*1000<n else n]

        request = "INSERT INTO coups (id_position_depart, id_position_arrive) VALUES (%s, %s)"
        curseur.executemany(request, temp)
        conn.commit()
    print("c'est bon 😅")
    ########
    
enregister_BDD()


