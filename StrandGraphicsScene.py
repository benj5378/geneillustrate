import json

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF, QRect
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor, QFont
from PySide6.QtGui import QImage, QPainter


# Todo, make all color variables QColor
class StrandGraphicsScene(QGraphicsScene):
    # Uses draw functions inherited from QGraphicsScene
    nucleotideWidth = 120
    nucleotideHeight = 90
    baseWidth = 60
    breakEveryNbase = 0

    def __init__(self):
        super().__init__()
        with open("./config.json") as file:
            self.updateConfig(json.load(file))

    def updateConfig(self, config=dict):
        self.colorConfig = dict()
        for base, rgb in config["colors"].items():
            r, g, b = rgb
            self.colorConfig[base] = QColor(r, g, b)

    def updateColor(self, base: str, color: QColor):
        self.colorConfig[base] = color

    def getColor(self, base: str) -> QColor:
        if base == "A":
            _base = "adenine"
        elif base == "C":
            _base = "cytosine"
        elif base == "G":
            _base = "guanine"
        elif base == "T":
            _base = "thymine"
        elif base in ["adenine", "cytosine", "guanine", "thymine"]:
            _base = base
        else:
            raise ValueError(f"Base {base} does not exist!")
        return self.colorConfig[_base]

    def drawBase(
        self,
        x: int,
        y: int,
        letter: str,
        flipped=False,
    ) -> None:
        letter = letter.upper()
        if letter == " ":
            return
        color = self.getColor(letter)

        if flipped:
            f = -1
        else:
            f = 1

        p = QPolygonF(
            [
                QPointF(x + 0, y),
                QPointF(x + 0, y + self.nucleotideHeight * 0.44 * f),
                QPointF(
                    x + (self.nucleotideWidth - self.baseWidth) / 2,
                    y + self.nucleotideHeight * 0.44 * f,
                ),
                QPointF(
                    x + (self.nucleotideWidth - self.baseWidth) / 2,
                    y + self.nucleotideHeight * f,
                ),
                QPointF(
                    x + (self.nucleotideWidth - self.baseWidth) / 2 + self.baseWidth,
                    y + self.nucleotideHeight * f,
                ),
                QPointF(
                    x + (self.nucleotideWidth - self.baseWidth) / 2 + self.baseWidth,
                    y + self.nucleotideHeight * 0.44 * f,
                ),
                QPointF(x + self.nucleotideWidth, y + self.nucleotideHeight * 0.44 * f),
                QPointF(x + self.nucleotideWidth, y),
                QPointF(x + 0, y),
            ]
        )

        self.addPolygon(p, pen=QPen(Qt.NoPen), brush=QBrush(color))

        textItem = self.addText(letter, QFont(["FreeSans"], 23))
        textItem.setPos(
            x + self.nucleotideWidth / 2 - textItem.boundingRect().width() / 2,
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
        flipped=False
    ) -> None:
        currentX = 0
        for letter in sequence:
            self.drawBase(currentX, y, letter, flipped)
            currentX = currentX + self.nucleotideWidth

    def drawSequence(self, x: int, y: int, sequence1: str, sequence2: str):
        if self.breakEveryNbase == 0:
            self.drawStrand(x, y, sequence1, False)
            self.drawStrand(x, y + 2 * self.nucleotideHeight, sequence2, True)
            return

        verticalSpacing = 0.3 * self.nucleotideHeight
        for i, j in enumerate(range(0, max(len(sequence1), len(sequence2)), self.breakEveryNbase)):
            self.drawStrand(x, y + (self.nucleotideHeight * 2 + verticalSpacing) * i, sequence1[j:j + self.breakEveryNbase], False)
            self.drawStrand(x, y + (self.nucleotideHeight * 2 + verticalSpacing) * i + 2 * self.nucleotideHeight, sequence2[j:j + self.breakEveryNbase], True)

    def exportToPNG(self):
        # It works. It just works. No idea how.
        area = QRect(
            0, 0, self.sceneRect().width(), self.sceneRect().height()
        )  # QRect(0, 0, 500, 500)
        img = QImage(area.size(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(img)
        self.render(painter, img.rect(), area)
        painter.end()
        img.save("./export.png")
