import hou
import os

from solaris_utils.ui import file_selector as fs
from importlib import reload
reload(fs)

# Import textures from disk and convert to MaterialX network
class TextureImport(fs.FileSelector):

    files = []
    directory = ""

    def __init__(self) -> None:
        super().__init__()

        # Receive signal from button emitting
        self.signal_files.connect(self.handle_file_signal)
        self.signal_directory.connect(self.handle_directory_signal)

        # Add new clicked connection to button
        self.button.clicked.connect(self.convert_texture)

    def import_textures(self) -> str:
        self.showui()

    def handle_file_signal(self, value):
        self.files = value
        print(self.files)

    def handle_directory_signal(self, value):
        self.directory = value
        print(self.directory)

    def convert_texture(self):
        print('Converting..')




