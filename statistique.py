import sqlite3 as sq
import matplotlip.pyplot as mpl

conn = sq.connect("BD2.db")
cur = conn.cursor()

candidat = ['Admis', 'Admis au 2nd Tour', 'Ajourne']
cur.execute("""SELECT total_point FROM Note """)
total = cur.fetchall()

ad = 0
t2 = 0
aj = 0
for i in total:
    if i > 180:
        ad = ad + 1
    elif 180 > i >= 153:
        t2 = t2 + 1
    else:
        aj = aj + 1

valeur = [ad, t2, aj]
couleur = ['lightcoral', 'blue', 'yellowgreen']
explode = [0.1, 0, 0.2]

mpl.pie(sizes=valeur, labels=candidat, colors=couleur, explode=explode)
mpl.axis('equal')
mpl.title('STATISTIQUE DES RESULTATS DE L\'EXAMEN')
mpl.show()
conn.commit()
conn.close()
