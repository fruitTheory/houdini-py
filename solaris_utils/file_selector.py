import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets

# General basic Ui for selecting files
class FileSelector(QtWidgets.QWidget):

    # Create detached widget
    def __init__(self) -> None:
        # Init Qwidget
        super().__init__()

        # Get current file path and ui file in same area
        current_dir = os.path.dirname(__file__)
        ui_filename = 'ui/file_importer.ui'
        ui_file = os.path.join(current_dir, ui_filename)

        self.setWindowTitle('File Importer')
        # Pull ui file and set parent to houdini's window
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget = self) # QDialog
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Setup button one - parent to object - connect btn to function
        button = self.ui.findChild(QtWidgets.QPushButton, 'pushButton')
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.setParent(self)
        self.connect(button, QtCore.SIGNAL('clicked()'), self.select_directory)

    # Select a directory and returns files inside of it
    def select_directory(self) -> list[str]:
        hui = hou.ui # Houdini interal ui actions
        directory = hui.selectFile(file_type=hou.fileType.Directory)
        directory = hou.expandString(directory) # Unpack variables in case
        dir_files = os.listdir(directory)
        print(dir_files)

        return dir_files
    
    def showui(self) -> None:
        self.show()

