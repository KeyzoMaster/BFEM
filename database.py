import sqlite3 as sq
import pandas as pd


class BrevetDB:
    def __init__(self):
        self.conn = sq.connect("BD.db")
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()

    def generateur_anonymat_principal(self, num_table):
        return int((2 * num_table) * (2 * num_table + 1) / 2)

    def a_deja_copies(self, num, tour="PREMIER TOUR"):
        ano = self.generateur_anonymat_principal(num)
        return self.cursor.execute("SELECT * FROM Note WHERE anonymat = ? AND tour = ?", (ano, tour)).fetchall()

    def generateur_anonymat_copie(self, num_table, anonymat, i):
        anonymat = 100 / anonymat
        num_table = 100 / num_table
        return int(.5 * (.5 * (num_table + anonymat) * (num_table + anonymat + 1) + anonymat + i)
                   * (.5 * (num_table + anonymat) * (num_table + anonymat + 1) + anonymat + i + 1) + i)

    def ajouter_jury(self, ia, ief, localite, centre, president, tel):
        self.cursor.execute("""INSERT INTO Jury(ia,ief,localite,centre_examen,president_jury,telephone) VALUES(
        ?,?,?,?,?,?);""", (ia, ief, localite, centre, president, tel))
        self.conn.commit()

    def correction_copie(self, anonymat_copie, note):
        self.cursor.execute("""UPDATE Copie SET note_copie = ? WHERE anonymat_copie = ?""", (note, anonymat_copie))
        self.conn.commit()

    def liste_copies_non_notees(self, tour="PREMIER TOUR"):
        dict_copies = {}
        matieres = self.matieres_a_faire(tour=tour)
        for matiere in matieres:
            temp = self.cursor.execute("""SELECT Copie.anonymat_copie FROM Note
                     INNER JOIN Copie ON Copie.anonymat_copie=Note.anonymat_copie WHERE note_copie
                     IS NULL and nom_matiere = ?;""", (matiere,)).fetchall()
            copies = []
            for num in temp:
                copies.append(num[0])
            if copies:
                dict_copies[matiere] = copies
        self.conn.commit()
        return dict_copies

    def est_apte(self, num_table):
        aptitude = self.cursor.execute("SELECT aptitude_sportive FROM Candidat WHERE num_table = ? ;",
                                       (num_table,)).fetchone()[0]
        self.conn.commit()
        return aptitude == "APTE"

    def a_choisi_epreuve_facutative(self, num_table):
        choix = self.cursor.execute("SELECT choix_epreuve_facultative FROM Candidat WHERE num_table = ? ;",
                                    (num_table,)).fetchone()[0]
        self.conn.commit()
        return choix == "OUI"

    def liste_num(self):
        infos = self.cursor.execute('SELECT num_table FROM Candidat').fetchall()
        self.conn.commit()
        nums = []
        for row in infos:
            nums.append(row[0])
        return nums

    def basic_information_candidat(self, num):
        infos = self.cursor.execute('SELECT prenom_s, nom, type_candidat FROM Candidat WHERE num_table = ?',
                                    (num,)).fetchall()
        self.conn.commit()
        return infos[0]

    def notes_information_candidat(self, num):
        matieres = self.liste_matieres_faites(num=num)
        notes_dic = {}
        for mat in matieres:
            notes_dic[mat] = str(self.nb_points(num, mat, with_coef=False))
        matieres = self.liste_matieres_faites(num, tour="SECOND TOUR")
        for mat in matieres:
            notes_dic[mat] = str(self.nb_points(num, mat, with_coef=False))
        return notes_dic

    def personal_information_candidat(self, num):
        personal_infos_dict = {"Numéro de table": "", "Prénom(s)": "", "Nom": "", "Date de naissance": "",
                               "Lieu de naissance": "", "Sexe": "", "Nationalité": "", "Etablissement": "",
                               "Epreuve Facultative": "",
                               "Aptitude sportive": "", "Type de candidat": "", "ID Livret": "", "Anonymat": "", }
        infos = self.cursor.execute("""SELECT num_table,prenom_s, nom, date_naissance,lieu_naissance, sexe,
         nationalite, etablissement, epreuve_facultative, aptitude_sportive, type_candidat,id_livret,
         anonymat FROM Candidat WHERE num_table = ?;""", (num,)).fetchone()

        i = 0
        for k in personal_infos_dict.keys():
            personal_infos_dict[k] = str(infos[i])
            i += 1
        infos = self.cursor.execute("""SELECT nombre_tentatives ,moy_6e , moy_5e, moy_4e, moy_3e, 
        moy_cycle FROM Livret WHERE id_livret = ?;""", (int(personal_infos_dict["ID Livret"]),)).fetchone()
        personal_infos_dict["Nombre de tentatives"] = str(infos[0])
        personal_infos_dict["Moyenne 6e"] = str(infos[1])
        personal_infos_dict["Moyenne 5e"] = str(infos[2])
        personal_infos_dict["Moyenne 4e"] = str(infos[3])
        personal_infos_dict["Moyenne 3e"] = str(infos[4])
        personal_infos_dict["Moyenne du cycle"] = str(infos[5])
        personal_infos_dict["Statut"] = ""
        self.conn.commit()
        return personal_infos_dict

    def nb_notes(self):
        return int(self.cursor.execute("SELECT count(*) FROM Note").fetchone()[0])

    def ajouter_copie_et_note(self, num_table, matiere, tour="PREMIER TOUR", note=None):
        ano_princ = self.generateur_anonymat_principal(num_table)
        i = self.nb_notes()
        ano_copie = self.generateur_anonymat_copie(num_table, ano_princ, i)
        self.cursor.execute("""INSERT INTO Copie(anonymat_copie, note_copie, nom_matiere)
                                           VALUES (?, ?, ?)""", (ano_copie, note, matiere))
        self.cursor.execute("""INSERT INTO Note(anonymat, anonymat_copie, tour) VALUES (?, ?, ?);""",
                            (ano_princ, ano_copie, tour))
        self.conn.commit()

    def matieres_a_faire(self, num=None, tour="PREMIER TOUR"):
        matieres = []
        if tour == "PREMIER TOUR":
            query_text = ""
            if num and not self.est_apte(num):
                query_text += ", \"eps\""
            if num and not self.a_choisi_epreuve_facutative(num):
                query_text += ", \"epreuve_facultative\""
            temp = self.cursor.execute("""SELECT nom_matiere FROM Matiere WHERE nom_matiere NOT IN (
            "francais_sec", "mathematiques_sec", "pc_lv2_sec" """ + query_text + ");").fetchall()
            self.conn.commit()
            for mat in temp:
                matieres.append(mat[0])
        else:
            matieres = ["francais_sec", "mathematiques_sec", "pc_lv2_sec"]
        return matieres

    def ajouter_toutes_copies_et_notes(self, num, matieres, tour="PREMIER TOUR", note=None):
        if not self.a_deja_copies(num, tour):
            for mat in matieres:
                self.ajouter_copie_et_note(num, mat, tour, note)

    def ajouter_livret(self, nb_tentatives, moy_6e, moy_5e, moy_4e, moy_3e):
        if moy_6e and moy_5e and moy_4e and moy_3e:
            moy_cycle = (float(moy_6e) + float(moy_5e) + float(moy_4e) + float(moy_3e)) / 4
            self.cursor.execute("""INSERT INTO Livret(nombre_tentatives ,moy_6e , moy_5e, moy_4e, moy_3e, moy_cycle)
                                    VALUES (?, ?, ?, ?, ?, ?);""",
                                (nb_tentatives, float(moy_6e), float(moy_5e), float(moy_4e), float(moy_3e),
                                 moy_cycle))
        else:
            self.cursor.execute("INSERT INTO Livret(nombre_tentatives) VALUES(?);", (nb_tentatives,))
        self.conn.commit()
        return int(self.cursor.execute("""SELECT id_livret FROM Livret 
                                          ORDER BY id_livret DESC LIMIT 1;""").fetchone()[0])

    def modifier_livret(self, id_livret, nb_tentatives, moy_6e, moy_5e, moy_4e, moy_3e):
        moy_cycle = (moy_6e + moy_5e + moy_4e + moy_3e) / 4
        self.cursor.execute("""UPDATE Livret SET nombre_tentatives=?, moy_6e=?, moy_5e=?, moy_4e=?, moy_3e=?,
        moy_cycle=? WHERE id_livret=?;""", (nb_tentatives, moy_6e, moy_5e, moy_4e, moy_3e, moy_cycle, id_livret))
        self.conn.commit()

    def modifier_candidat(self, prenom, nom, dn, ln, sexe, nat, eta, opt, apt, type, nb, m6, m5, m4, m3, id, num):
        self.cursor.execute("""UPDATE Candidat SET prenom_s = ?, nom = ?, date_naissance ?, lieu_naissance = ?, 
                                    sexe = ?,nationalite = ?, etablissement = ?, choix_epreuve_facultative = ?, 
                                    epreuve_facultative = ?, aptitude_Sportive = ?, 
                                    type_candidat = ? WHERE num_table = ?""", (prenom, nom, dn, ln, sexe,
                                                                               nat, eta,
                                                                               "OUI" if opt is not None else "NON",
                                                                               None if opt is None else opt,
                                                                               apt, type, int(num)))
        self.modifier_livret(int(id), nb, m6, m5, m4, m3)

    def supprimer_candidat(self, num):
        (anonymat, id_livret) = self.cursor.execute("SELECT anonymat, id_livret FROM Candidat WHERE num_table=?;",
                                                    (num,)).fetchone()
        temp = self.cursor.execute("SELECT anonymat_copie FROM Note WHERE anonymat=?;",
                                   (anonymat,)).fetchall()
        liste_anonymats = []
        for ano in temp:
            liste_anonymats.append(ano[0])
        self.cursor.execute("DELETE FROM Candidat WHERE num_table = ?;", (num,))
        self.cursor.execute("DELETE FROM Livret WHERE id_livret=?;", (id_livret,))
        self.cursor.execute("DELETE FROM Note WHERE anonymat=?;", (anonymat,))
        for ano in liste_anonymats:
            self.cursor.execute("DELETE FROM Copie WHERE anonymat_copie=?;", (ano,))
        self.conn.commit()

    def ajouter_candidat(self, num, prenoms, nom, date_naissance, lieu_naissance, sexe, nationalite, etablissement,
                         epreuve_facultative, etat_sportif, type_candidat, id_livret):

        if not num:
            num = self.liste_num()[-1] + 1
        self.cursor.execute("""INSERT INTO Candidat (num_table, prenom_s, nom, date_naissance, lieu_naissance, 
                                    sexe,nationalite, etablissement, choix_epreuve_facultative, epreuve_facultative, 
                                    aptitude_Sportive, type_candidat,id_livret, anonymat) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """,
                            (num, str(prenoms).upper(), str(nom).upper(), date_naissance, lieu_naissance,
                             sexe, nationalite, etablissement, "OUI" if epreuve_facultative != "NEUTRE" else "NON",
                             None if epreuve_facultative == "NEUTRE" else epreuve_facultative,
                             etat_sportif, type_candidat, id_livret, self.generateur_anonymat_principal(num)))
        self.conn.commit()

    def est_repechable(self, num):
        (moy, nb_tentatives) = self.cursor.execute("""SELECT moy_cycle, nombre_tentatives FROM Livret INNER JOIN Candidat ON Candidat.id_livret = 
        Livret.id_livret WHERE Candidat.num_table = ?;""", (num,)).fetchone()
        self.conn.commit()
        return moy is not None and float(moy) >= 10 and int(nb_tentatives) <= 2

    def liste_matieres_faites(self, num, tour="PREMIER TOUR"):
        temp = self.cursor.execute("""SELECT nom_matiere FROM Copie INNER JOIN Note ON Copie.anonymat_copie=
                Note.anonymat_copie INNER JOIN Candidat on Note.anonymat=Candidat.anonymat WHERE num_table=
                ? AND tour = ? AND note_copie IS NOT NULL;""", (num, tour)).fetchall()
        self.conn.commit()
        liste = []
        for m in temp:
            liste.append(m[0])
        return liste

    def nb_points(self, num, matiere, with_coef=True):
        temp = self.cursor.execute("""SELECT note_copie, coef_matiere FROM Matiere INNER JOIN Copie ON Matiere.nom_matiere=
        Copie.nom_matiere INNER JOIN Note ON Copie.anonymat_copie=
        Note.anonymat_copie INNER JOIN Candidat on Note.anonymat=Candidat.anonymat WHERE num_table=? AND Copie.nom_matiere 
        = ? AND note_copie IS NOT NULL;""", (num, matiere)).fetchone()
        self.conn.commit()
        return float(temp[0]) * (int(temp[1])) if with_coef else float(temp[0])

    def calcul_points_premier_tour(self, num):
        liste_mat = self.liste_matieres_faites(num)
        points = 0
        if "eps" in liste_mat:
            note_eps = self.nb_points(num, "eps")
            points += note_eps - 10
            liste_mat.remove("eps")
        if "epreuve_facultative" in liste_mat:
            note_epreuve_facultative = self.nb_points(num, "epreuve_facultative")
            if note_epreuve_facultative > 10:
                points += note_epreuve_facultative - 10
            liste_mat.remove("epreuve_facultative")
        for mat in liste_mat:
            points += self.nb_points(num, mat)
        return points

    def calcul_points_second_tour(self, num):
        liste_mat = self.liste_matieres_faites(num, tour="SECOND TOUR")
        points = 0
        for mat in liste_mat:
            points += self.nb_points(num, mat)
        return points

    def resultats_premier_tour(self):
        liste_num = self.liste_num()
        resultats = []
        for num in liste_num:
            points = self.calcul_points_premier_tour(num)
            if points >= 180 or (self.est_repechable(num) and 171 <= points < 180):
                resultats.append([num, points, "Admis(e)"])
            elif points >= 153 or (self.est_repechable(num) and 144 <= points < 153):
                resultats.append([num, points, "Autorise(e) au second tour"])
                self.ajouter_toutes_copies_et_notes(num, self.matieres_a_faire(tour="SECOND TOUR"), "SECOND TOUR")
        resultats.sort(key=lambda x: x[1], reverse=True)
        full_results = []
        for n in resultats:
            r = self.personal_information_candidat(n[0])
            r["Statut"] = n[-1]
            full_results.append(r)
        return full_results

    def resultats_second_tour(self):
        resultat_premier_tour = self.resultats_premier_tour()
        liste_num = []
        for e in resultat_premier_tour:
            if e["Statut"] == "Autorise(e) au second tour":
                liste_num.append(e["Numéro de table"])
        resultats = []

        for num in liste_num:
            points = self.calcul_points_second_tour(num)
            if points >= 80 or (self.est_repechable(num) and 76 <= points < 80):
                resultats.append([num, points, "Admis(e)"])
        resultats.sort(key=lambda x: x[1], reverse=True)

        full_results = []
        for n in resultats:
            r = self.personal_information_candidat(n[0])
            r["Statut"] = n[-1]
            full_results.append(r)
        return full_results

    def resultats(self, tour="PREMIER TOUR"):
        if not self.liste_copies_non_notees(tour=tour):
            if tour == "PREMIER TOUR":
                return self.resultats_premier_tour()
            else:
                return self.resultats_second_tour()

    def fill_db(self, xslx_file_path):
        df = pd.read_excel(xslx_file_path, sheet_name="Feuille 1")

        # effacer toutes les tables si elles existent
        self.cursor.execute("DROP TABLE IF EXISTS Note;")
        self.cursor.execute("DROP TABLE IF EXISTS Copie;")
        self.cursor.execute("DROP TABLE IF EXISTS Matiere;")
        self.cursor.execute("DROP TABLE IF EXISTS Session;")
        self.cursor.execute("DROP TABLE IF EXISTS Candidat;")
        self.cursor.execute("DROP TABLE IF EXISTS Livret;")
        self.cursor.execute("DROP TABLE IF EXISTS ChoixEpreuveFacultative;")
        self.cursor.execute("DROP TABLE IF EXISTS Sexe;")
        self.cursor.execute("DROP TABLE IF EXISTS TypeCandidat;")
        self.cursor.execute("DROP TABLE IF EXISTS AptitudeSportive;")
        self.cursor.execute("DROP TABLE IF EXISTS EpreuveFacultative;")
        self.cursor.execute("DROP TABLE IF EXISTS Jury;")

        # table des sexes
        self.cursor.execute("CREATE TABLE Sexe(sexe TEXT, PRIMARY KEY(sexe));")
        self.cursor.execute("INSERT INTO Sexe(sexe) VALUES (?), (?)", ("M", "F"))

        # table des epreuves facultatives
        self.cursor.execute("CREATE TABLE EpreuveFacultative(epreuve_facultative TEXT, PRIMARY KEY("
                            "epreuve_facultative));")
        self.cursor.execute("INSERT INTO EpreuveFacultative(epreuve_facultative) VALUES (?),(?),(?)",
                            ("COUTURE", "DESSIN", "MUSIQUE"))

        # table du choix d'epreuve facultative
        self.cursor.execute("""CREATE TABLE ChoixEpreuveFacultative(choix_epreuve_facultative TEXT,
                                  PRIMARY KEY(choix_epreuve_facultative));""")
        self.cursor.execute("INSERT INTO ChoixEpreuveFacultative(choix_epreuve_facultative) VALUES (?),(?)",
                            ("OUI", "NON"))

        # table de l'aptitude sportive
        self.cursor.execute(
            """CREATE TABLE AptitudeSportive(aptitude_sportive TEXT,PRIMARY KEY(aptitude_sportive));""")
        self.cursor.execute("INSERT INTO AptitudeSportive(aptitude_sportive) VALUES (?),(?)",
                            ("APTE", "INAPTE"))

        # table des types de candidats
        self.cursor.execute("CREATE TABLE TypeCandidat(type_candidat TEXT,PRIMARY KEY(type_candidat));")
        self.cursor.execute("INSERT INTO TypeCandidat(type_candidat) VALUES (?),(?)",
                            ("OFFICIEL", "INDIVIDUEL"))

        # table des matières
        self.cursor.execute("""CREATE TABLE Matiere(nom_matiere TEXT, coef_matiere INTEGER NOT NULL,
                               PRIMARY KEY(nom_matiere));""")
        self.cursor.execute("""INSERT INTO Matiere(nom_matiere, coef_matiere) VALUES (?,?),
                               (?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?),(?,?);""",
                            ("compo_franc", 2, "dictee", 1, "etude_de_texte", 1, "instruction_civique", 1,
                             "histoire_geographie", 1, "mathematiques", 4, "pc_lv2", 2, "svt", 2, "anglais1", 2,
                             "anglais_oral", 1, "eps", 1, "epreuve_facultative", 1,
                             "francais_sec", 3, "mathematiques_sec", 3, "pc_lv2_sec", 2))

        # table du jury
        self.cursor.execute("""CREATE TABLE Jury(id_jury INTEGER,ia TEXT NOT NULL,ief TEXT NOT NULL,
                   localite TEXT NOT NULL,centre_examen TEXT NOT NULL,president_jury TEXT NOT NULL,
                   telephone TEXT NOT NULL, PRIMARY KEY(id_jury));""")

        # tables des sessions
        self.cursor.execute("CREATE TABLE Session(tour TEXT, PRIMARY KEY(tour));")
        self.cursor.execute("INSERT INTO Session(tour) VALUES (?),(?)",
                            ("PREMIER TOUR", "SECOND TOUR"))

        # table des candidats
        self.cursor.execute("""CREATE TABLE Candidat(
                  num_table INTEGER,
                  anonymat INTEGER NOT NULL,
                  prenom_s TEXT NOT NULL,
                  nom TEXT NOT NULL,
                  date_naissance NUMERIC NOT NULL,
                  lieu_naissance TEXT NOT NULL,
                  sexe TEXT NOT NULL,
                  nationalite TEXT NOT NULL,
                  etablissement TEXT NOT NULL,
                  choix_epreuve_facultative TEXT NOT NULL,
                  epreuve_facultative TEXT,
                  aptitude_sportive TEXT NOT NULL,
                  type_candidat TEXT NOT NULL,
                  id_livret INTEGER NOT NULL,
                  PRIMARY KEY(num_table),
                  UNIQUE(anonymat),
                  FOREIGN KEY(epreuve_facultative) REFERENCES EpreuveFacultative(epreuve_facultative),
                  FOREIGN KEY(sexe) REFERENCES Sexe(sexe),
                  FOREIGN KEY(id_livret) REFERENCES Livret(id_livret),
                  FOREIGN KEY(aptitude_sportive) REFERENCES AptitudeSportive(aptitude_sportive),
                  FOREIGN KEY(choix_epreuve_facultative) REFERENCES ChoixEpreuveFacultative(choix_epreuve_facultative),
                  FOREIGN KEY(type_candidat) REFERENCES TypeCandidat(type_candidat));""")

        # table des copies
        self.cursor.execute("""CREATE TABLE Copie(
                                  anonymat_copie TEXT,
                                  note_copie NUMERIC(4,2),
                                  nom_matiere TEXT NOT NULL,
                                  PRIMARY KEY(anonymat_copie),
                                  FOREIGN KEY(nom_matiere) REFERENCES Matiere(nom_matiere));""")

        # table des livrets
        self.cursor.execute("""CREATE TABLE Livret(id_livret INTEGER,nombre_tentatives INTEGER NOT NULL,
                                  moy_6e NUMERIC(4,2), moy_5e NUMERIC(4,2), moy_4e NUMERIC(4,2),
                                  moy_3e NUMERIC(4,2), moy_cycle TEXT,
                                  PRIMARY KEY(id_livret));""")

        # table des notes
        self.cursor.execute("""CREATE TABLE Note(
                                  anonymat INTEGER,
                                  anonymat_copie TEXT,
                                  tour TEXT,
                                  PRIMARY KEY(anonymat, anonymat_copie, tour),
                                  FOREIGN KEY(anonymat) REFERENCES Candidat(anonymat),
                                  FOREIGN KEY(anonymat_copie) REFERENCES Copie(anonymat_copie),
                                  FOREIGN KEY(tour) REFERENCES Session(tour));""")

        # remplissage table des livrets et des candidats
        for _, row in df.iterrows():
            date_naissance = row["Date de nais."]

            # Convertir le Timestamp en format texte (YYYY-MM-DD)
            if isinstance(date_naissance, pd.Timestamp):
                date_naissance = date_naissance.strftime("%d-%m-%Y")
            id_livret = self.ajouter_livret(int(row["Nb fois"]), float(row["Moy_6e"]), float(row["Moy_5e"]),
                                            float(row["Moy_4e"]), float(row["Moy_3e"]))

            self.ajouter_candidat(int(row["N° de table"]), row["Prenom (s)"], row["NOM"], date_naissance,
                                  row["Lieu de nais."], row["Sexe"], row["Nationnallité"], row["Etablissement"],
                                  str(row["Epreuve Facultative"]).upper(),
                                  row["Etat Sportif"], str(row["Type de candidat"]).upper(), id_livret)

        # Remplir les tables epreuves et notes
        mat_premier_tour = {"Note EPS": "eps", "Note CF": "compo_franc", "Note Ort": "dictee",
                            "Note TSQ": "etude_de_texte", "Note SVT": "svt", "Note ANG1": "anglais1",
                            "Note MATH": "mathematiques", "Note HG": "histoire_geographie",
                            "Note IC": "instruction_civique", "Note PC/LV2": "pc_lv2", "Note ANG2": "anglais_oral",
                            "Note Ep Fac": "epreuve_facultative"}

        for k, v in mat_premier_tour.items():
            for _, row in df.iterrows():
                if float(row[k]) >= 0:
                    self.ajouter_copie_et_note(int(row["N° de table"]), v, "PREMIER TOUR", note=float(row[k]))
        self.commit_and_close()
