import hou
import os

from solaris_utils.ui import file_selector as fs
from importlib import reload
reload(fs)

# Convert images to colorspace
class ColorConvert(fs.FileSelector):

    def __init__(self) -> None:
        super().__init__()

        # Add new connection to button
        self.button.clicked.connect(self.file_parse)
        self.showui()

    # Look through files and search for Albedo or HDR - wip
    def file_parse(self) -> None:
        
        num_files = len(self.files)
        for file in self.files:
            split = file.split('_')[-1]
            find = split.find('Albedo')
            if(find != -1):
                # print(file), print(self.directory)
                self.convert_to_aces(file)
            if(file.endswith('.hdr')):
                # print(file), print(self.directory)
                self.convert_to_aces(file)

    # Convert file to ACEScg via comp network
    def convert_to_aces(self, file) -> None:

        converter = hou.node('/stage').createNode('cop2net', 'converter')
        converter.setCurrent(True, True) # select node, clear previous selection

        # Create file node and set params 
        file_node = converter.createNode('file', 'file_name')

        ext = file.split('.')[-1]
        if(ext == 'jpg'):
            file_node.setParms({'linearize':False})

        filepath = os.path.join(self.directory, file)
        file_node.parm('filename1').set(filepath)

        # Create vopcop2gen node
        vopcop2gen = converter.createNode('vopcop2gen', 'aces_convert')
        vopcop2gen.setInput(0, file_node)
        vc_internal_nodes = vopcop2gen.children()

        global_type = hou.vopNodeTypeCategory().nodeTypes()['global']
        output_type = hou.vopNodeTypeCategory().nodeTypes()['output']

        # Safe way to grab specific already created nodes  
        for node in vc_internal_nodes:
            if(node.type() == global_type):
                vc_global_node = node
            if(node.type() == output_type):
                vc_output_node = node

        # Setting node types to create and returns list of created nodes
        vc_node_type = ('floattovec', 'ocio_transform', 'vectofloat')
        vc_created_node = []
        for node_type in vc_node_type:
            node = vopcop2gen.createNode(node_type)
            vc_created_node.append(node)

        float_to_vec, ocio_transform, vec_to_float = vc_created_node

        # Set inner node inputs
        for index in range(3):
            float_to_vec.setInput(index, vc_global_node, 3+index)
            vc_output_node.setInput(index, vec_to_float, index)

        ocio_transform.setInput(0, float_to_vec)
        vec_to_float.setInput(0, ocio_transform)

        # Set ocio transforms
        if(ext == 'jpg'): 
            ocio_transform.setParms({'fromspace':'sRGB - Texture', 'tospace':'ACEScg'})
        else:
            ocio_transform.setParms({'fromspace':'Linear Rec.709 (sRGB)', 'tospace':'ACEScg'})

        vopcop2gen.layoutChildren()

        # Create export node
        export_node = converter.createNode('rop_comp', 'rop_output')
        export_node.setInput(0, vopcop2gen)
        
        # Procedural naming, should work for any file extension
        new_filepath = filepath.replace('.'+ ext, '_ACEScg.'+ ext)
        export_node.parm('copoutput').set(new_filepath)
        export_node.parm('execute').pressButton()

        converter.layoutChildren()
