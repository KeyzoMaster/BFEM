from database import BFEMDB
from docx import Document
from docx2pdf import convert
from docx.enum.text import WD_ALIGN_PARAGRAPH


class ImpressBFEM:
    def liste_candidat(self, ia, ief, center, jury):
        db_connection = BFEMDB()
        document = Document()
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
        list_paragraph.add_run('Centre d\'Examen:').bold = True
        list_paragraph.add_run(center)
        list_paragraph.add_run('\n')
        list_paragraph.add_run('\n')
        list_paragraph.add_run('JURY:').bold = True
        list_paragraph.add_run(jury)
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

        table1 = db_connection.complete_information_candidat()
        for row in table1:
            cells = table.add_row().cells
            for i in range(len(row)):
                cells[i].text = str(row[i])

        signe = document.add_paragraph('Le responsable', None)
        signe.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        document.save('impression_candidat.docx')
