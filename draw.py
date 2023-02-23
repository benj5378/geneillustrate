from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor, QFont


def drawBase(x : int, y : int, scene : QGraphicsScene, letter : str, flipped=False, nucleotideWidth=120, basewidth=60) -> None:
    letter = letter.upper()
    if letter == "A": color = QColor.fromRgb(0, 0, 255)
    elif letter == "C": color = QColor.fromRgb(255, 0, 0)
    elif letter == "G": color = QColor.fromRgb(0, 255, 0)
    elif letter == "T": color = QColor.fromRgb(255, 196, 0)
    elif letter == " ": return
    else: raise ValueError

    if flipped: f = -1
    else: f = 1
    
    p = QPolygonF(
        [
            QPointF(x + 0, y + 0 * f),
            QPointF(x + 0, y + 40 * f),
            QPointF(x + (nucleotideWidth - basewidth) / 2, y + 40 * f),
            QPointF(x + (nucleotideWidth - basewidth) / 2, y + 90 * f),
            QPointF(x + (nucleotideWidth - basewidth) / 2 + basewidth, y + 90 * f),
            QPointF(x + (nucleotideWidth - basewidth) / 2 + basewidth, y + 40 * f),
            QPointF(x + nucleotideWidth, y + 40 * f),
            QPointF(x + nucleotideWidth, y + 0 * f),
            QPointF(x + 0, y + 0 * f),
        ]
    )

    scene.addPolygon(p, pen=QPen(Qt.NoPen), brush=QBrush(color))

    textItem = scene.addText(letter, QFont(["FreeSans"], 23))
    textItem.setPos(
        x + nucleotideWidth / 2 - textItem.boundingRect().width() / 2,
        (y + 5) if not flipped else (y + 2 - textItem.boundingRect().height()),  # estimations, hardcoded
    )
    textItem.setDefaultTextColor(QColor.fromRgb(255, 255, 255))


def drawStrand(x : int, y : int, scene : QGraphicsScene, sequence : str, flipped=False, nucleotideWidth=120, basewidth=60) -> None:
    currentX = 0
    for letter in sequence:
        drawBase(currentX, y, scene, letter, flipped, nucleotideWidth, basewidth)
        currentX = currentX + nucleotideWidth

def drawSequence(x : int, y : int, scene : QGraphicsScene, sequence1 : str, sequence2 : str, nucleotideWidth=120, basewidth=60):
    drawStrand(x, y, scene, sequence1, False, nucleotideWidth, basewidth)
    drawStrand(x, y + 2 * 90, scene, sequence2, True, nucleotideWidth, basewidth)