import json

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor, QFont
from PySide6.QtGui import QImage, QPainter


class StrandGraphicsScene(QGraphicsScene):
    # Uses draw functions inherited from QGraphicsScene

    def __init__(self):
        super().__init__()
        with open("./config.json") as file:
            self.config = json.load(file)

    def drawBase(
        self,
        x: int,
        y: int,
        letter: str,
        flipped=False,
        nucleotideWidth=120,
        basewidth=60,
    ) -> None:
        letter = letter.upper()
        if letter == "A":
            confcolor = self.config["colors"]["adenine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "C":
            confcolor = self.config["colors"]["cytosine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "G":
            confcolor = self.config["colors"]["guanine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "T":
            confcolor = self.config["colors"]["thymine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == " ":
            return
        else:
            raise ValueError

        if flipped:
            f = -1
        else:
            f = 1

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

        self.addPolygon(p, pen=QPen(Qt.NoPen), brush=QBrush(color))

        textItem = self.addText(letter, QFont(["FreeSans"], 23))
        textItem.setPos(
            x + nucleotideWidth / 2 - textItem.boundingRect().width() / 2,
            (y + 5)
            if not flipped
            else (y + 2 - textItem.boundingRect().height()),  # estimations, hardcoded
        )
        textItem.setDefaultTextColor(QColor.fromRgb(255, 255, 255))

    def drawStrand(
        self,
        x: int,
        y: int,
        sequence: str,
        flipped=False,
        nucleotideWidth=120,
        basewidth=60,
    ) -> None:
        currentX = 0
        for letter in sequence:
            self.drawBase(currentX, y, letter, flipped, nucleotideWidth, basewidth)
            currentX = currentX + nucleotideWidth

    def drawSequence(
        self,
        x: int,
        y: int,
        sequence1: str,
        sequence2: str,
        nucleotideWidth=120,
        basewidth=60,
    ):
        self.drawStrand(x, y, sequence1, False, nucleotideWidth, basewidth)
        self.drawStrand(x, y + 2 * 90, sequence2, True, nucleotideWidth, basewidth)
