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
            self._selection = selection[0]
            self.hda_name = self._selection.type().name()

        # Add new clicked connection to button
        self.button.clicked.connect(self.import_textures)
        self.showui()
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

        ''' 
        Search Keywords MS
            ( 'Albedo', 'AO', 'Displacement', 'Normal', 
              'Opacity', 'Roughness', 'Spec', 'Translucency' )

        Search Keywords Polyhaven
            ( 'arm', 'diff', 'disp', 'normal', 
              'rough' )

        Search Keywords Ambient CG
            ( 'AmbientOcclusion', 'Color', 'Displacement', 'Metalness', 
              'NormalGL', 'Roughness' )

        Search Keywords GSG
            ( 'basecolor', 'height', 'metallic', 'normal', 
              'roughness' )

        Parameter Names
            (
            'albedo_file', 'ao_file', 'normal_file', 'opacity_file',
            'trans_file', 'disp_file', 'rough_file' )
        '''

        texture_source = self.get_source()

        if(texture_source == self.TexId.Megascans):

            msDict = { 'Albedo':'albedo_file', 'AO':'ao_file', 'Displacement':'disp_file', 'Normal':'normal_file', 
            'Opacity':'opacity_file', 'Roughness':'rough_file', 'Specular':'spec_file', 'Translucency':'trans_file',
            'Metalness':'metalness_file' }

            self.run_import(msDict)

        elif(texture_source == self.TexId.Polyhaven):
            # Special snowflake embedded RGB texture will need unique HDA or setup
            polyDict = { 'diff':'albedo_file', 'arm':'ao_file', 'disp':'disp_file', 'normal':'normal_file', 
            'rough':'rough_file', 'arm':'metalness_file' }

            self.run_import(polyDict)
        
        elif(texture_source == self.TexId.Ambient_cg):

            amDict = { 'Color':'albedo_file', 'AmbientOcclusion':'ao_file', 'Displacement':'disp_file', 
            'NormalGL':'normal_file', 'Roughness':'rough_file', 'Metalness':'metalness_file' }

            self.run_import(amDict)

        elif(texture_source == self.TexId.Gsg):

            gsDict = { 'basecolor':'albedo_file', 'AO':'ao_file', 'height':'disp_file', 'normal':'normal_file', 
            'roughness':'rough_file', 'metallic':'metalness_file'  }

            self.run_import(gsDict)

    # Run import logic for provided dictionary with relevant keywords and HDA parms
    def run_import(self, mainDict) -> None:

        keywords = list(mainDict.keys())

        # Amount of keywords 
        length = len(keywords)

        # For each keyword do an action if keyword is found in directory
        for iter in range(length):
            for file in self._files:
                # Search for relevant name in file
                keyword_found = file.find(keywords[iter])
                # If file is found, set the correlated parm to file path and break loop
                if(keyword_found != -1):
                    file_path = self._directory + file
                    self._selection.parm(mainDict[keywords[iter]]).set(file_path)
                    break
                else:
                    # Clear param texture if doesnt exist - Optional*
                    self._selection.parm(mainDict[keywords[iter]]).set('')
    