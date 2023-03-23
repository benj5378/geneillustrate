import sys
import json

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, QObject, SIGNAL

from StrandGraphicsScene import StrandGraphicsScene
from SequenceMappingGraphicsScene import SequenceMappingGraphicsScene


app = QApplication(sys.argv)

ui_file = QFile("main.ui")
ui_file.open(QIODevice.ReadOnly)
window = QUiLoader().load(ui_file)
ui_file.close()

window.show()

def zoomIn():
    window.strandGraphics.scale(1.2, 1.2)

def zoomOut():
    window.strandGraphics.scale(1 / 1.2, 1 / 1.2)


def updateView():
    nucleotideWidth = int(window.nucleotideWidthInput.text())
    baseWidth = int(window.baseWidthInput.text())

    _StrandGraphicsScene.clear()
    text = window.strandEdit.toPlainText()
    strands = text.splitlines()

    if len(strands) == 1:
        _StrandGraphicsScene.drawStrand(
            0, 0, strands[0], False, nucleotideWidth, baseWidth
        )
    elif len(strands) == 2:
        _StrandGraphicsScene.drawSequence(
            0, 0, strands[0], strands[1], nucleotideWidth, baseWidth
        )
    elif len(strands) == 0:
        return
    else:
        raise ValueError(f"Too many strands, {len(strands)} given, wanted 1 or 2")


_StrandGraphicsScene = StrandGraphicsScene()
window.strandGraphics.setScene(_StrandGraphicsScene)

_StrandGraphicsScene.drawSequence(0, 0, "ATGTTACT", "TACAATGA")

textEdit = window.strandEdit
textEdit.setFontFamily("DejaVu Sans Mono")


textEdit.textChanged.connect(updateView)
window.baseWidthInput.textChanged.connect(updateView)
window.zoomInButton.pressed.connect(zoomIn)
window.zoomOutButton.pressed.connect(zoomOut)
window.action_to_PNG.triggered.connect(_StrandGraphicsScene.exportToPNG)


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

    _SequenceMappingGraphicsScene.clear()
    _SequenceMappingGraphicsScene.drawLinearMap(genes)


_SequenceMappingGraphicsScene = SequenceMappingGraphicsScene()
window.geneMapGraphics.setScene(_SequenceMappingGraphicsScene)

geneMapEdit = window.geneMapEdit
geneMapEdit.setFontFamily("DejaVu Sans Mono")

QObject.connect(geneMapEdit, SIGNAL('textChanged()'), updateGeneMap)




app.exec()

