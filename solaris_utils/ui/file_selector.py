import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets

# General basic Ui for selecting files
class FileSelector(QtWidgets.QWidget):

    # Global Signal object and type to emit
    signal_files = QtCore.Signal(list)
    signal_directory = QtCore.Signal(str)
    ui_base_filename = 'file_selector.ui'

    # Create detached widget
    def __init__(self) -> None:
        super().__init__() # Qwidget

        # Get current file path and ui file
        current_dir = os.path.dirname(__file__)
        ui_filename = self.ui_base_filename
        ui_file = os.path.join(current_dir, ui_filename)

        # Pull ui file and parent to houdini's window
        self.setWindowTitle('File Importer')
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget = self) # QDialog
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Initialize btn - Parent to object - Connect btn to function
        self.button = self.ui.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.setParent(self)
        self.button.clicked.connect(self.select_directory)

        # Receive signal and send to receiver function 
        self.signal_files.connect(self.handle_file_signal)
        self.signal_directory.connect(self.handle_directory_signal)


    # Select a directory and emits the files contain and directory path
    def select_directory(self) -> None:
        hui = hou.ui # Houdini interal ui actions
        directory = hui.selectFile(file_type=hou.fileType.Directory)
        directory = hou.expandString(directory) # Unpack hou variables
        dir_files = os.listdir(directory)

        # Emit data to instanced Signal: types are list[str] and str
        self.signal_files.emit(dir_files)
        self.signal_directory.emit(directory)

    # Function 
    def handle_file_signal(self, value) -> None:
        self._files = value
        # print(self._files)

    def handle_directory_signal(self, value) -> None:
        self._directory = value
        # print(self._directory)
        
    
    def showui(self) -> None:
        self.show()
