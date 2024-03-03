import hou
import os

from solaris_utils.ui import file_selector as fs

# Import textures from disk and convert to MaterialX network
class ColorConvert:
    def __init__(self) -> None:
        pass

    def convert_to_aces(self) -> str:
        get_files = fs.FileSelector()
        files = get_files.showui()
        if(files != None): print(files)

    # for texture in texture_folder:
        # if texture_type == Albedo or HDR:

    # converter = hou.node('/stage').createNode('cop2net', 'converter')
    # converter.setCurrent(True, True) # select node, clear previous selection
    # frameSelection()

    converter = hou.node('/img').createNode('img', 'converter')

    file_node = converter.createNode('file', 'file_name')

    # ext = file_name.split('.')[-1]
    ext = 'jpg'

    if( ext == 'jpg' or 'png'): 
        file_node.setParms({'linearize':False})


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

    # Set inputs
    for index in range(3):
        float_to_vec.setInput(index, vc_global_node, 4+index)
        vc_output_node.setInput(index, vec_to_float, index)

    ocio_transform.setInput(0, float_to_vec)
    vec_to_float.setInput(0, ocio_transform)

    # Set ocio transform
    if( ext == 'jpg' or 'png'): 
        ocio_transform.setParms({'fromspace':'sRGB - Texture', 'tospace':'ACEScg'})
    else:
        ocio_transform.setParms({'fromspace':'Raw', 'tospace':'ACEScg'})

    vopcop2gen.layoutChildren()

    # Create export node
    export_node = converter.createNode('rop_comp', 'rop_output')
    export_node.setInput(0, vopcop2gen)

    converter.layoutChildren()
        
