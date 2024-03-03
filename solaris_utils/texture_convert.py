import hou
import os

from solaris_utils.utility import node_utils
from solaris_utils import file_selector as fs

# Import textures from disk and convert to MaterialX network
class TextureImport:
    def __init__(self) -> None:
        pass

    def import_textures(self) -> str:
        get_files = fs.FileSelector()
        files = get_files.showui()
        if(files != None): print(files)

