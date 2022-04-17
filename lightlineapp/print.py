# from reportlab.lib.pagesizes import letter, A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
from .models import *

from django.contrib.auth.models import User


class PDF_Printer:
    def __init__(self, buffer, pagesize, request):
        self.buffer = buffer
        self.request = request
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

        self.activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        self.activeCueList = CueList.objects.get(project = self.activeProject, active = True)


    # def addPageNumber(self, canvas, doc, w, h):
    #     """
    #     Add the page number
    #     """
    #     page_num = canvas.getPageNumber()
    #     text = "Page #%s" % page_num
    #     canvas.drawRightString(w, h, text)


    # def _header_footer(self, canvas, doc):

    #     # Save the state of our canvas so we can draw on it
    #     canvas.saveState()
    #     styles = getSampleStyleSheet()

    #     # Header

    #     #Populate table with show data
    #     headerTableData = []

    #     headerTableData.append(["SHOW: " + str(self.activeProject)])
    #     headerTableData.append(["LIGHTING DESIGNER: " + self.activeProject.lightingDesigner.getName()])
    #     headerTableData.append(["CUE LIST: " + str(self.activeCueList)])

    #     header = Table(headerTableData, colWidths=[doc.width/5.0])

    #     w, h = header.wrap(doc.width, doc.topMargin)
    #     header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

    #     # Footer
    #     footer = Paragraph(str(self.activeCueList), styles['Normal'])
    #     w, h = footer.wrap(doc.width, doc.bottomMargin)
    #     footer.drawOn(canvas, doc.leftMargin, h)
    #     #Page Number
    #     self.addPageNumber(canvas, doc, w, h)

    #     # Release the canvas
        
    #     canvas.restoreState()

    # def printTest(self):    
    #     buffer = self.buffer
    #     doc = SimpleDocTemplate(buffer,
    #                             rightMargin=72,
    #                             leftMargin=72,
    #                             topMargin=150,
    #                             bottomMargin=72,
    #                             pagesize=self.pagesize)

    #     # Our container for 'Flowable' objects
    #     elements = []

    #     # A large collection of style sheets pre-made for us
    #     styles = getSampleStyleSheet()
    #     styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

    #     # Draw things on the PDF. Here's where the PDF generation happens.
    #     # See the ReportLab documentation for the full list of functionality.
    #     elements.append(Paragraph(self.activeCueList.listName, styles['Heading1']))

    #     #Populate table with Cues
    #     cueTableData = []
    #     cues = Cue.objects.filter(cueList=self.activeCueList)

    #     i = 0

    #     style = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                                     ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])

    #     for cue in cues:
    #         if cue.getHeader() != None:
    #             cueTableData.append([cue.getHeader()])
    #             style.add('SPAN', (0, i), (4, i))
    #             style.add('BACKGROUND',(0, i), (4, i),  colors.lavender)
    #             cueTableData.append([Paragraph(str(cue.eosCueNumber)), Paragraph(str(cue.cueLabel)), Paragraph(str(cue.pageNumber)), Paragraph(str(cue.cueTime)), Paragraph(str(cue.cueDescription))])
    #             i+=2
    #         else:
    #             cueTableData.append([Paragraph(str(cue.eosCueNumber)), Paragraph(str(cue.cueLabel)), Paragraph(str(cue.pageNumber)), Paragraph(str(cue.cueTime)), Paragraph(str(cue.cueDescription))])
    #             i+=1

    #     # Create the Cues table
    #     colUnit = (doc.width/10.0)
    #     cueTable = Table(cueTableData, colWidths=[colUnit * 1, colUnit * 4, colUnit * 0.5, colUnit * 0.5, colUnit * 4])
    #     cueTable.setStyle(style)

    #     elements.append(cueTable)

    #     doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

    #     # Get the value of the BytesIO buffer and write it to the response.
    #     pdf = buffer.getvalue()
    #     buffer.close()
    #     return pdf
