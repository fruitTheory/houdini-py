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
            # Type node
            self.selection = selection[0]
            self.hda_name = self.selection.type().name()

        # Add new clicked connection to button
        self.button.clicked.connect(self.import_textures)
        self.showui()
        # self.create_nodes()
        self.signal_directory

    # Struct for enum-ish
    class TexId:
        Megascans = 0
        Polyhaven = 1
        Ambient_cg = 2
        Gsg = 3
    
    # Return value representing where textures are sourced from
    def get_source(self) -> int:
        # Loose ID's - megascans, polyhaven, ambient_cg, gsg
        identifiers = ('Albedo', 'arm', 'AmbientOcclusion', 'basecolor')

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

        if(texture_source == self.TexId.Megascans):
            self.import_megascans()

        elif(texture_source == self.TexId.Polyhaven):
            self.import_polyhaven()
        
        elif(texture_source == self.TexId.Ambient_cg):
            self.import_ambient_cg()

        elif(texture_source == self.TexId.Gsg):
            self.import_gsg()


    def import_megascans(self) -> None:
        ''' 
        Search Keywords
            ( 'Albedo', 'AO', 'Displacement', 'Normal', 
              'Opacity', 'Roughness', 'Spec', 'Translucency' )

        Parameter Names
            (
            'albedo_file', 'ao_file', 'normal_file', 'opacity_file',
            'trans_file', 'disp_file', 'rough_file' )
        '''
        msDict = { 'Albedo':'albedo_file', 'AO':'ao_file', 'Displacement':'disp_file', 'Normal':'normal_file', 
            'Opacity':'opacity_file', 'Roughness':'rough_file', 'Specular':'spec_file', 'Translucency':'trans_file' }

        keywords = list(msDict.keys())

        # Amount of keywords - 8
        length = len(msDict)

        # For each keyword do an action if keyword is found in directory
        for iter in range(length):
            for file in self._files:
                # Searching for relevant name in file
                keyword_found = file.find(keywords[iter])
                # If file is found, set the correlated parm to file path and break loop
                if(keyword_found != -1):
                    # print('hit', file)
                    file_path = self._directory + file
                    self.selection.parm(msDict[keywords[iter]]).set(file_path)
                    break
                else:
                    # Clear param texture doesnt exist - Optional*
                    self.selection.parm(msDict[keywords[iter]]).set('')


    def import_polyhaven(self) -> None:
        # Special snowflake embedded RGB texture will need unique HDA or setup
        polyhaven_key = ('arm', 'diff', 'disp', 'normal', 'rough')
        pass

    def import_ambient_cg(self) -> None:
        ambient_cg_key = ('AmbientOcclusion', 'Color', 'Displacement', 'Metalness', 'NormalGL', 'Roughness')
        
        pass

    def import_gsg(self) -> None:
        gsg_key = ('basecolor', 'height', 'metallic', 'normal', 'roughness')
        
        pass


    def create_nodes(self) -> None:
        # print('Converting..')
        pass

    # megascans_tex_amt = len(megascans_tex)
    # gsg_tex_amt = len(gsg_tex)
    # ambient_cg_amt = len(ambient_cg)
    # polyhaven_tex_amt = len(polyhaven_tex)