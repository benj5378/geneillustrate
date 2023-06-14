import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QEvent

from StrandGraphicsScene import StrandGraphicsScene
from SequenceMappingGraphicsScene import SequenceMappingGraphicsScene
from ChangeColorDialog import ChangeColorDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.loadUI()
        self.setupUI()
        self.makeBindings()
        self.startSetting()
        self.ui.show()

    def loadUI(self):
        ui_file = QFile("main.ui")
        ui_file.open(QIODevice.ReadOnly)
        self.ui = QUiLoader().load(ui_file, self)
        ui_file.close()

        # In connection with eventFilter
        self.ui.setParent(self, self.ui.windowFlags() | Qt.WindowType.Window)
        self.ui.installEventFilter(self)

    def setupUI(self):
        self.ui.strandEdit.setFontFamily("DejaVu Sans Mono")
        self.ui.strandGraphicsScene = StrandGraphicsScene()
        self.ui.strandGraphics.setScene(self.ui.strandGraphicsScene)

        self.ui.geneMapEdit.setFontFamily("DejaVu Sans Mono")
        self.ui.sequenceMappingGraphicsScene = SequenceMappingGraphicsScene()
        self.ui.geneMapGraphics.setScene(self.ui.sequenceMappingGraphicsScene)

    def makeBindings(self):
        # Strand tab bindings
        self.ui.baseWidthInput.textChanged.connect(self.updateStrandGraphics)
        self.ui.nucleotideWidthInput.textChanged.connect(self.updateStrandGraphics)
        self.ui.breakEveryNBaseInput.textChanged.connect(self.updateStrandGraphics)
        self.ui.strandEdit.textChanged.connect(self.updateStrandGraphics)
        self.ui.zoomInButton.pressed.connect(self.strandGraphicsZoomIn)
        self.ui.zoomOutButton.pressed.connect(self.strandGraphicsZoomOut)

        # Gene map tab bindings
        self.ui.geneMapEdit.textChanged.connect(self.updateSequenceMappingGraphics)

        # Menu bindings
        self.ui.action_to_PNG.triggered.connect(self.ui.strandGraphicsScene.exportToPNG)
        self.ui.actionChange_colors.triggered.connect(self.changeColors)

    # Helps closing quitting the application when the window is exitted
    # I don't know how it works, it just works
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Close and source is self.ui:
            QApplication.instance().quit()
        return super().eventFilter(source, event)

    def startSetting(self):
        self.ui.strandEdit.setPlainText("ATGTTACT\nTACAATGA")

    def strandGraphicsZoomOut(self):
        self.uistrandGraphics.scale(1 / 1.2, 1 / 1.2)

    def strandGraphicsZoomIn(self):
        self.ui.strandGraphics.scale(1.2, 1.2)

    def updateStrandGraphics(self):
        self.ui.strandGraphicsScene.nucleotideWidth = int(
            self.ui.nucleotideWidthInput.text()
        )
        self.ui.strandGraphicsScene.nucleotideHeight = int(
            self.ui.nucleotideHeightInput.text()
        )
        self.ui.strandGraphicsScene.baseWidth = int(self.ui.baseWidthInput.text())
        self.ui.strandGraphicsScene.breakEveryNbase = int(self.ui.breakEveryNBaseInput.text())

        self.ui.strandGraphicsScene.clear()
        text = self.ui.strandEdit.toPlainText()
        strands = text.splitlines()

        if len(strands) == 1:
            self.ui.strandGraphicsScene.drawStrand(0, 0, strands[0], False)
        elif len(strands) == 2:
            self.ui.strandGraphicsScene.drawSequence(0, 0, strands[0], strands[1])
        elif len(strands) == 0:
            return
        else:
            raise ValueError(f"Too many strands, {len(strands)} given, wanted 1 or 2")

    def updateSequenceMappingGraphics(self):
        genes = list()

        text = self.ui.geneMapEdit.toPlainText()
        genesStr = text.splitlines()
        for geneStr in genesStr:
            geneData = geneStr.split(", ")
            geneName = geneData[0]
            geneWidth = int(geneData[1])
            geneColor = (int(geneData[2]), int(geneData[3]), int(geneData[4]))

            genes.append((geneName, geneWidth, geneColor))

        self.ui.sequenceMappingGraphicsScene.clear()
        self.ui.sequenceMappingGraphicsScene.drawLinearMap(genes)

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)

    def changeColors(self):
        # How does this object get deleted???
        ChangeColorDialog(
            self.ui.strandGraphicsScene.updateColor,
            self.ui.strandGraphicsScene.getColor,
            self.updateStrandGraphics,
        )


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
