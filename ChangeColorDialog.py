from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import QFile
from PySide6.QtGui import QColor


class ChangeColorDialog:
    def __init__(
        self,
        updateColorMethod: callable,
        getColorMethod: callable,
        updateCallback: callable,
    ):
        """Binder is the method for the user input to be parsed to"""
        self.loadUI()
        self.setupUI()
        self.updateColorMethod = updateColorMethod
        self.getColorMethod = getColorMethod
        self.updateCallback = updateCallback

    def loadUI(self):
        ui_file = QFile("ChangeColorDialog.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.show()

    def setupUI(self):
        self.ui.adenineChangeColorButton.pressed.connect(
            lambda: self.updateColor("adenine")
        )
        self.ui.cytosineChangeColorButton.pressed.connect(
            lambda: self.updateColor("cytosine")
        )
        self.ui.guanineChangeColorButton.pressed.connect(
            lambda: self.updateColor("guanine")
        )
        self.ui.thymineChangeColorButton.pressed.connect(
            lambda: self.updateColor("thymine")
        )

    def updateColor(self, base):
        oldcolor = self.getColorMethod(base)
        newcolor = QColorDialog.getColor(oldcolor)
        self.updateColorMethod(base, newcolor)
        self.updateCallback()  # For instance, update graphics
