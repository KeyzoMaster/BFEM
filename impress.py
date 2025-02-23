from database import BrevetDB
from docx import Document
from docx2pdf import convert
from docx.enum.text import WD_ALIGN_PARAGRAPH


class ImpressBFEM:
    def liste_candidats(self):
        document = Document()
        (ia, ief, localite, centre, president, tel) = BrevetDB().cursor.execute("""SELECT ia, ief, localite, 
        centre_examen, president_jury, telephone FROM Jury""")
        titre = document.add_heading("OFFICE du BFEM", 1)
        titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # les informations du jury et du centre d'examen
        document.add_heading(' ', 2)
        list_paragraph = document.add_paragraph()
        list_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        list_paragraph.style = None
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('IA:').bold = True
        list_paragraph.add_run(ia)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('IEF:').bold = True
        list_paragraph.add_run(ief)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('Localité').bold = True
        list_paragraph.add_run(localite)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('Centre d\'Examen:').bold = True
        list_paragraph.add_run(centre)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('Président du Jury').bold = True
        list_paragraph.add_run(president)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('Téléphone').bold = True
        list_paragraph.add_run(tel)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')

        # liste des candidats et les anonymats
        titre2 = document.add_heading('LISTE DES CANDIDATS', 3)
        titre2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        titre2.style = None

        table = document.add_table(cols=13, rows=1)
        table.style = 'Table Grid'

        # heading_cells = table.rows[0].cells
        # heading_content = ("Prénom(s)", "Nom", "")

        # for i in range(13):
        # heading_cells[i].text = str(heading_content[i])

        table1 = BrevetDB().complete_information_liste()
        for row in table1:
            cells = table.add_row().cells
            for i in range(len(row)):
                cells[i].text = str(row[i])

        signe = document.add_paragraph('Le responsable', None)
        signe.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        document.save('impression_candidat.docx')

        # TITRE de fichier

        # convertir le document .docx en document .pdf
        chemin_word = "impression_candidat.docx"
        chemin_pdf = "impression_candidat.pdf"

        convert(chemin_word, chemin_pdf)

    def liste_anonymats(self):
        pass

    def releve_note(self,num_table):
        pass

    def pv_bfem(self):
        pass
