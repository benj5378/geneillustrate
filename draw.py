from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor, QFont

width1 = 120
width2 = 60

def drawBase(x : int, y : int, scene : QGraphicsScene, letter : str, flipped=False) -> None:
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
            QPointF(x + (width1 - width2) / 2, y + 40 * f),
            QPointF(x + (width1 - width2) / 2, y + 90 * f),
            QPointF(x + (width1 - width2) / 2 + width2, y + 90 * f),
            QPointF(x + (width1 - width2) / 2 + width2, y + 40 * f),
            QPointF(x + width1, y + 40 * f),
            QPointF(x + width1, y + 0 * f),
            QPointF(x + 0, y + 0 * f),
        ]
    )

    scene.addPolygon(p, pen=QPen(Qt.NoPen), brush=QBrush(color))

    textItem = scene.addText(letter, QFont(["FreeSans"], 23))
    textItem.setPos(
        x + 60 - textItem.boundingRect().width() / 2,
        (y + 5) if not flipped else (y + 2 - textItem.boundingRect().height()),  # estimations, hardcoded
    )
    textItem.setDefaultTextColor(QColor.fromRgb(255, 255, 255))


def drawStrand(x : int, y : int, scene : QGraphicsScene, sequence : str, flipped=False) -> None:
    currentX = 0
    for letter in sequence:
        drawBase(currentX, y, scene, letter, flipped)
        currentX = currentX + 120

def drawSequence(x : int, y : int, scene : QGraphicsScene, sequence1 : str, sequence2 : str):
    drawStrand(x, y, scene, sequence1, False)
    drawStrand(x, y + 2 * 90, scene, sequence2, True)