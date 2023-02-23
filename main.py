import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QGraphicsScene
from PySide6.QtCore import QFile, QIODevice, QObject, SIGNAL

from draw import *
from sequence_mapping import *


app = QApplication(sys.argv)

ui_file = QFile("main.ui")
ui_file.open(QIODevice.ReadOnly)
window = QUiLoader().load(ui_file)
ui_file.close()

window.show()

def updateView():
    nucleotideWidth = int(window.nucleotideWidthInput.text())
    baseWidth = int(window.baseWidthInput.text())

    scene.clear()
    text = window.strandEdit.toPlainText()
    strands = text.splitlines()

    if len(strands) == 1:
        drawStrand(0, 0, scene, strands[0], False, nucleotideWidth, baseWidth)
    elif len(strands) == 2:
        drawSequence(0, 0, scene, strands[0], strands[1], nucleotideWidth, baseWidth)
    elif len(strands) == 0:
        return
    else:
        raise ValueError(f"Too many strands, {len(strands)} given, wanted 1 or 2")



scene = QGraphicsScene()
window.strandGraphics.setScene(scene)

drawSequence(0, 0, scene, "ATGTTACT", "TACAATGA")

textEdit = window.strandEdit
textEdit.setFontFamily("DejaVu Sans Mono")


textEdit.textChanged.connect(updateView)
window.baseWidthInput.textChanged.connect(updateView)
window.nucleotideWidthInput.textChanged.connect(updateView)


def updateGeneMap():
    genes = list()

    text = window.geneMapEdit.toPlainText()
    genesStr = text.splitlines()
    for geneStr in genesStr:
        geneData = geneStr.split(", ")
        geneName = geneData[0]
        geneWidth = int(geneData[1])
        geneColor = (int(geneData[2]), int(geneData[3]), int(geneData[4]))

        genes.append((
            geneName,
            geneWidth,
            geneColor
        ))

    scene2.clear()
    drawLinearMap(scene2, genes)



scene2 = QGraphicsScene()
window.geneMapGraphics.setScene(scene2)

geneMapEdit = window.geneMapEdit
geneMapEdit.setFontFamily("DejaVu Sans Mono")

QObject.connect(geneMapEdit, SIGNAL('textChanged()'), updateGeneMap)




app.exec()

