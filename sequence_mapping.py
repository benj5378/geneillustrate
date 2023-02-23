from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from PySide6.QtCore import QRectF

def drawLinearMap(scene : QGraphicsScene, genes : list[tuple[str, int, tuple[int, int, int]]]):    
    currentX = 0
    for gene in genes:
        geneName = gene[0]
        geneWidth = gene[1]
        geneColor = gene[2]

        drawGene(currentX, 0, scene, geneName, geneWidth, geneColor)
        currentX = currentX + geneWidth


def drawGene(x : int, y : int, scene : QGraphicsScene, geneName : str, geneWidth : int, geneColor : tuple[int, int, int]):
    rect = QRectF(x, y, geneWidth, 50)
    scene.addRect(
        rect,
        QPen(QColor.fromRgb(60, 60, 60)),
        QBrush(QColor.fromRgb(geneColor[0], geneColor[1], geneColor[2]))
    )

    textItem = scene.addText(geneName, QFont(["FreeSans"], 23))

    boundingbox = textItem.boundingRect()

    textItem.setPos(
        x + geneWidth / 2 - boundingbox.width() / 2,
        y + 50 - boundingbox.height()
    )