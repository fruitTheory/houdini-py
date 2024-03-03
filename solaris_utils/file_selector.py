import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets

# General basic Ui for selecting files
class FileSelector(QtWidgets.QWidget):

    # Global Signal that passes type list
    signal_files = QtCore.Signal(list)
    signal_directory = QtCore.Signal(str)

    # Create detached widget
    def __init__(self) -> None:
        # Init Qwidget
        super().__init__()

        # Get current file path and ui file in same area
        current_dir = os.path.dirname(__file__)
        ui_filename = 'ui/file_importer.ui'
        ui_file = os.path.join(current_dir, ui_filename)

        # Pull ui file and set parent to houdini's window
        self.setWindowTitle('File Importer')
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget = self) # QDialog
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Initialize btn - Parent to object - Connect btn to function
        self.button = self.ui.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.setParent(self)
        self.button.clicked.connect(self.select_directory)


    # Select a directory and returns files inside of it
    def select_directory(self) -> list[str]:
        hui = hou.ui # Houdini interal ui actions
        directory = hui.selectFile(file_type=hou.fileType.Directory)
        directory = hou.expandString(directory) # Unpack hou variables
        dir_files = os.listdir(directory)

        # Emit instanced Signal: value is list of files
        self.signal_files.emit(dir_files)
        self.signal_directory.emit(directory)
        
    
    def showui(self) -> None:
        self.show()
