import hou
import os

from solaris_utils.ui import file_selector as fs
from importlib import reload
reload(fs)

# Import textures from disk into a MaterialX network
class TextureImport(fs.FileSelector):

    def __init__(self) -> None:
        super().__init__()

        # Add new clicked connection to button
        self.button.clicked.connect(self.convert_texture)
        self.showui()

    def import_textures(self) -> None:
        pass

    def convert_texture(self) -> None:
        print('Converting..')
