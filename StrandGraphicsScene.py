import json

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QPointF, QRect
from PySide6.QtGui import QPolygonF, QPen, QBrush, QColor, QFont
from PySide6.QtGui import QImage, QPainter


# Todo, make all color variables QColor
class StrandGraphicsScene(QGraphicsScene):
    # Uses draw functions inherited from QGraphicsScene

    def __init__(self):
        super().__init__()
        with open("./config.json") as file:
            self.updateConfig(json.load(file))

    def updateConfig(self, config=dict):
        self.colorConfig = config["colors"]

    def updateColor(self, base: str, color: list[int, int, int]):
        self.colorConfig[base] = color

    def getColor(self, base: str) -> list[int, int, int]:
        return self.colorConfig[base]

    def drawBase(
        self,
        x: int,
        y: int,
        letter: str,
        flipped=False,
        nucleotideWidth=120,
        nucleotideHeight=90,
        basewidth=60,
    ) -> None:
        letter = letter.upper()
        if letter == "A":
            confcolor = self.colorConfig["adenine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "C":
            confcolor = self.colorConfig["cytosine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "G":
            confcolor = self.colorConfig["guanine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == "T":
            confcolor = self.colorConfig["thymine"]
            color = QColor.fromRgb(confcolor[0], confcolor[1], confcolor[2])
        elif letter == " ":
            return
        else:
            raise ValueError("Base does not exist!")

        if flipped:
            f = -1
        else:
            f = 1

        p = QPolygonF(
            [
                QPointF(x + 0, y),
                QPointF(x + 0, y + nucleotideHeight * 0.44 * f),
                QPointF(
                    x + (nucleotideWidth - basewidth) / 2,
                    y + nucleotideHeight * 0.44 * f,
                ),
                QPointF(
                    x + (nucleotideWidth - basewidth) / 2, y + nucleotideHeight * f
                ),
                QPointF(
                    x + (nucleotideWidth - basewidth) / 2 + basewidth,
                    y + nucleotideHeight * f,
                ),
                QPointF(
                    x + (nucleotideWidth - basewidth) / 2 + basewidth,
                    y + nucleotideHeight * 0.44 * f,
                ),
                QPointF(x + nucleotideWidth, y + nucleotideHeight * 0.44 * f),
                QPointF(x + nucleotideWidth, y),
                QPointF(x + 0, y),
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
        nucleotideHeight=90,
        basewidth=60,
    ) -> None:
        currentX = 0
        for letter in sequence:
            self.drawBase(
                currentX,
                y,
                letter,
                flipped,
                nucleotideWidth,
                nucleotideHeight,
                basewidth,
            )
            currentX = currentX + nucleotideWidth

    def drawSequence(
        self,
        x: int,
        y: int,
        sequence1: str,
        sequence2: str,
        nucleotideWidth=120,
        nucleotideHeight=90,
        basewidth=60,
    ):
        self.drawStrand(
            x, y, sequence1, False, nucleotideWidth, nucleotideHeight, basewidth
        )
        self.drawStrand(
            x,
            y + 2 * nucleotideHeight,
            sequence2,
            True,
            nucleotideWidth,
            nucleotideHeight,
            basewidth,
        )

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
