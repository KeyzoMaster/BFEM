import sqlite3 as sq
import pandas as pd


class BFEMDB:
    def __init__(self):
        self.conn = sq.connect("BD2.db")
        self.cursor = self.conn.cursor()

    def fill_db(self, xslx_file_path):
        df = pd.read_excel(xslx_file_path, sheet_name="Feuille 1")

        self.cursor.execute("DROP TABLE IF EXISTS Livret_scolaire")
        self.cursor.execute("DROP TABLE IF EXISTS Candidat")
        self.cursor.execute("DROP TABLE IF EXISTS NotesSecondTour")
        self.cursor.execute("DROP TABLE IF EXISTS Note")

        self.cursor.execute("""
            CREATE TABLE Livret_scolaire(
                Id_Livret_scolaire INTEGER PRIMARY KEY ,
                Nombre_fois INT,
                Moyenne_6eme DECIMAL(15,2),
                Moyenne_5eme DECIMAL(15,2),
                Moyenne_4eme DECIMAL(15,2),
                Moyenne_3eme DECIMAL(15,2),
                Moyenne_cycle DECIMAL(15,2)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE NotesSecondTour(
                id TEXT PRIMARY KEY,
                Francais DECIMAL(4,2),
                CoefA INT,
                Mathematiques DECIMAL(4,2),
                CoefB INT,
                PC_LV2 DECIMAL(4,2),
                CoefC INT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Candidat(
                Numero_Table INTEGER PRIMARY KEY AUTOINCREMENT,
                Prenom_s TEXT NOT NULL,
                Nom TEXT NOT NULL,
                Date_Naissance DATE NOT NULL,
                Lieu_Naissance TEXT NOT NULL,
                Sexe CHAR(1) NOT NULL,
                Nationalite TEXT,
                Etablissement TEXT,
                Choix_Epr_Facultatif BOOLEAN,
                Epreuve_Facultative TEXT,
                Aptitude_Sportif BOOLEAN,
                Id_Livret_scolaire INTEGER NOT NULL UNIQUE,
                FOREIGN KEY(Id_Livret_scolaire) REFERENCES Livret_scolaire(Id_Livret_scolaire)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Note(
                Id_Note INTEGER PRIMARY KEY AUTOINCREMENT,
                Compo_Franc DECIMAL(15,2),
                Coef1 INT,
                Dictee DECIMAL(15,2),
                Coef2 INT,
                Etude_de_texte DECIMAL(15,2),
                Coef3 INT,
                Instruction_Civique DECIMAL(15,2),
                Coef4 INT,
                Histoire_Geographie DECIMAL(15,2),
                Coef5 INT,
                Mathematiques DECIMAL(15,2),
                Coef6 INT,
                PC_LV2 DECIMAL(15,2),
                Coef7 INT,
                SVT DECIMAL(15,2),
                Coef8 INT,
                Anglais1 DECIMAL(15,2),
                Coef9 INT,
                Anglais_orale DECIMAL(15,2),
                Coef10 INT,
                EPS DECIMAL(15,2),
                Epreuve_Facultative DECIMAL(15,2),
                Numero_Table INTEGER NOT NULL,
                id TEXT NOT NULL,
                FOREIGN KEY(Numero_Table) REFERENCES Candidat(Numero_Table),
                FOREIGN KEY(id) REFERENCES NotesSecondTour(id)
            );
        """)

        # Meme cheminement pour remplir les autres tables

        for _, row in df.iterrows():
            date_naissance = row["Date de nais."]

            # Convertir le Timestamp en format texte (YYYY-MM-DD)
            if isinstance(date_naissance, pd.Timestamp):
                date_naissance = date_naissance.strftime("%Y-%m-%d")
            self.cursor.execute("""
                INSERT INTO Candidat (
                    Numero_Table, Prenom_s, Nom, Date_Naissance, Lieu_Naissance, Sexe,
                    Nationalite, Etablissement, Choix_Epr_Facultatif, Epreuve_Facultative, Aptitude_Sportif, 
                    Id_Livret_scolaire
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            """, (
                row["N° de table"], row["Prenom (s)"], row["NOM"], date_naissance,
                row["Lieu de nais."], row["Sexe"], row["Nationnallité"], row["Etablissement"],
                False if row["Epreuve Facultative"] == "NEUTRE" else True, row["Epreuve Facultative"],
                row["Etat Sportif"],
                row["N° de table"]
            ))

        # float(row["Moy_6e"])

        # Remplir la table Note
        for _, row in df.iterrows():
            self.cursor.execute("""INSERT INTO Note(
                        Id_note, Compo_Franc, Coef1, Dictee, Coef2, Etude_de_texte, Coef3, Instruction_Civique, Coef4, 
                        Histoire_Geographie, Coef5, Mathematiques, Coef6, 
                        PC_LV2, Coef7, SVT, Coef8, Anglais1, Coef9, Anglais_orale, Coef10, EPS, Epreuve_Facultative, 
                        Numero_Table, id)
                        VALUES (?, ?, 1, ?, 2, ?, 3, ?, 4, ?, 5, ?, 6, ?, 7, ?, 8, ?, 9, ?, 10, ?, ?, ?, ?)
                        """, (
                row["N° de table"], float(row["Note CF"]), float(row["Note Ort"]), float(row["Note TSQ"]),
                float(row["Note IC"]), float(row["Note HG"]), float(row["Note MATH"]),
                float(row["Note PC/LV2"]), float(row["Note SVT"]), float(row["Note ANG1"]), float(row["Note ANG2"]),
                float(row["Note EPS"]), float(row["Note Ep Fac"]),
                row["N° de table"], row["N° de table"]
            ))
            # remplir livret
        for _, row in df.iterrows():
            self.cursor.execute("""INSERT INTO Livret_scolaire(
                Id_Livret_scolaire ,Nombre_fois ,Moyenne_6eme ,Moyenne_5eme ,Moyenne_4eme ,Moyenne_3eme,Moyenne_cycle)
                VALUES (?, ?, ?, ?, ?, ?,((?+ ?+ ?+?)/4))""",
                                (row["N° de table"], row["Nb fois"], float(row["Moy_6e"]), float(row["Moy_5e"]),
                                 float(row["Moy_4e"]),
                                 float(row["Moy_3e"]),
                                 float(row["Moy_6e"]), float(row["Moy_5e"]), float(row["Moy_4e"]), float(row["Moy_3e"])
                                 ))
        self.conn.commit()
        self.conn.close()

    def basic_information_candidat(self):
        infos = self.cursor.execute('SELECT Numero_Table, Prenom_s, Nom FROM Candidat').fetchall()
        self.conn.commit()
        return infos

    def complete_information_candidat(self):
        infos = self.cursor.execute('SELECT * FROM Candidat').fetchall()
        self.conn.commit()
        return infos

"""#recupere les information du candidat par numero de table
def numero_table():
    num=input("entrer le numero de table :  ")
    resultat = cur.execute("SELECT Numero_Table, Prenom_s, Nom, Date_Naissance, Lieu_Naissance, Sexe,Etablissement FROM
    Candidat WHERE Numero_Table=?",(num,))
    conn.commit()
    return resultat

numero_table()
"""
