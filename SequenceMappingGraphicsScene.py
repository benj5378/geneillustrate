from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from PySide6.QtCore import QRectF


class SequenceMappingGraphicsScene(QGraphicsScene):
    # Uses draw functions inherited from QGraphicsScene
    def __init__(self):
        super().__init__()

    def drawLinearMap(self, genes: list[tuple[str, int, tuple[int, int, int]]]):
        currentX = 0
        for gene in genes:
            geneName = gene[0]
            geneWidth = gene[1]
            geneColor = gene[2]

            self.drawGene(currentX, 0, geneName, geneWidth, geneColor)
            currentX = currentX + geneWidth

    def drawGene(
        self,
        x: int,
        y: int,
        geneName: str,
        geneWidth: int,
        geneColor: tuple[int, int, int],
    ):
        rect = QRectF(x, y, geneWidth, 50)
        self.addRect(
            rect,
            QPen(QColor.fromRgb(60, 60, 60)),
            QBrush(QColor.fromRgb(geneColor[0], geneColor[1], geneColor[2])),
        )

        textItem = self.addText(geneName, QFont(["FreeSans"], 23))

        boundingbox = textItem.boundingRect()

        textItem.setPos(
            x + geneWidth / 2 - boundingbox.width() / 2, y + 50 - boundingbox.height()
        )
