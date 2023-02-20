import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsScene, QTextEdit
from PySide6.QtCore import QFile, QIODevice, QLine, Qt, QPointF, QObject, SIGNAL
from PySide6.QtGui import QPainter, QPolygonF, QPen, QBrush, QColor, QFont

from draw import *


app = QApplication(sys.argv)

ui_file = QFile("main.ui")
ui_file.open(QIODevice.ReadOnly)
window = QUiLoader().load(ui_file)
ui_file.close()

window.show()

def updateView():
    scene.clear()
    text = window.textEdit.toPlainText()
    strands = text.splitlines()

    if len(strands) == 1:
        drawStrand(0, 0, scene, strands[0])
    elif len(strands) == 2:
        drawSequence(0, 0, scene, strands[0], strands[1])
    elif len(strands) == 0:
        return
    else:
        raise ValueError(f"Too many strands, {len(strands)} given, wanted 1 or 2")



scene = QGraphicsScene()
window.graphicsView.setScene(scene)

drawSequence(0, 0, scene, "ATGTTACT", "TACAATGA")

textEdit = window.textEdit
textEdit.setFontFamily("DejaVu Sans Mono")

QObject.connect(textEdit, SIGNAL('textChanged()'), updateView)


app.exec()

