import hou
import os

from solaris_utils.ui import file_selector as fs
from importlib import reload
reload(fs)


# Import textures from disk into Custom HDA that is MaterialX based
class TextureImport(fs.FileSelector):

    def __init__(self) -> None:
        super().__init__()

        # Error check - else extract first node
        selection = hou.selectedNodes()
        if(len(selection) != 1):
            raise ValueError('Select only one node')
        else:
            self.selection = selection[0]

        # Add new clicked connection to button
        self.button.clicked.connect(self.import_textures)
        self.showui()
        self.create_nodes()


    # Struct for enum-like
    class TexId:
        Megascans = 0
        Polyhaven = 1
        Ambient_cg = 2
        Gsg = 3

    def get_source(self) -> int:
        # Loose ID's - megascans, polyhaven, ambient_cg, gsg
        identifiers = ('Albedo', 'arm', 'AmbientOcclusion', 'basecolor')

        print(self.selection)

        for file in self._files:
            if(file.find(identifiers[0]) != -1):
                return self.TexId.Megascans
            
            if(file.find(identifiers[1]) != -1):
                return self.TexId.Polyhaven
            
            if(file.find(identifiers[2]) != -1):
                return self.TexId.Ambient_cg

            if(file.find(identifiers[3]) != -1):
                return self.TexId.Gsg

    def import_textures(self) -> None:
        texture_source = self.get_source()
        print('source:', texture_source)

        if(texture_source == self.TexId.Megascans):
            self.import_megascans()

        elif(texture_source == self.TexId.Polyhaven):
            self.import_polyhaven()
        
        elif(texture_source == self.TexId.Ambient_cg):
            self.import_ambient_cg()

        elif(texture_source == self.TexId.Gsg):
            self.import_gsg()


    def import_megascans(self) -> None:
        megascans_tex = ('Albedo', 'AO', 'Displacement', 'Normal', 
                'Opacity', 'Roughness', 'Spec', 'Translucency')
        # for file in self._files:
        #     if(file.find('basecolor') != -1):
        #         print('found')

        # print(file.find('basecolor'))
        # fsplit = file.split('_')[-1]
        # fsplit = fsplit.split('.')[-2]
        # print(fsplit)

        pass

    def import_polyhaven(self) -> None:
        polyhaven_tex = ('arm', 'diff', 'disp', 'normal', 'rough')

        pass

    def import_ambient_cg(self) -> None:
        ambient_cg = ('AmbientOcclusion', 'Color', 'Displacement', 'Metalness', 'NormalGL', 'Roughness')
        
        pass

    def import_gsg(self) -> None:
        gsg_tex = ('basecolor', 'height', 'metallic', 'normal', 'roughness')
        
        pass


    def create_nodes(self) -> None:
        # print('Converting..')
        pass

    # megascans_tex_amt = len(megascans_tex)
    # gsg_tex_amt = len(gsg_tex)
    # ambient_cg_amt = len(ambient_cg)
    # polyhaven_tex_amt = len(polyhaven_tex)