import hou
import os
from importlib import reload
from solaris_utils.ui import file_selector as fs
from solaris_utils import import_textures as tx
reload(tx)


# Write a USD with variants from all scan variations
class VariantImport(fs.FileSelector):

  def __init__(self) -> None:
    super().__init__(title="Variant Import")
    
    self.showui()
    self.button.clicked.connect(self.create_nodes)
    self.button.clicked.connect(self.import_textures)

  # Create, setup, and wire all nodes
  def create_nodes(self) -> None:

    if(len(self._files) == 0):
      return

    #-----Create Components------#

    file_path_collect = []
    comp_geo_collect = []

    # Create component nodes based on varations
    for file in self._files:
      if(file.startswith("Var")):
        var_name = os.listdir(self._directory+file)[0]

        # Append fbx filepath before altering var_name
        file_path = self._directory + file + '/' + var_name
        file_path_collect.append(file_path)

        var_name = var_name.split(".")[0]
        var_name += "_"
        comp_geo = hou.node('/stage').createNode('componentgeometry', var_name)
        comp_geo_collect.append(comp_geo)

    #-----Create component SOP Nodes------#

    # Setup Component node internals and make connections
    for node in range(len(comp_geo_collect)):
      # Get component name and path to its sop
      node_name = comp_geo_collect[node].name()
      comp_sop = hou.node("/stage/"+node_name+"/sopnet/geo")

      # File
      file_import = comp_sop.createNode('file', 'fbx_import')
      file_import.setParms({'file':file_path_collect[node]})

      # Attrib delete
      attrib_del = comp_sop.createNode('attribdelete', 'clean')
      attrib_del.setParms({'negate':True, 'ptdel':'N', 'vtxdel':'uv', 'primdel':'name'})

      # Transform
      xform = comp_sop.createNode('xform', 'global_scale')
      xform.setParms({'scale':0.01})

      # Polyreduce
      polyreduce = comp_sop.createNode('polyreduce', 'reduce')
      polyreduce.setParms({'percentage':10, 'originalpoints':True})
      
      # Gather
      sop_nodes = [file_import, attrib_del, xform, polyreduce]

      # Set Inputs
      attrib_del.setInput(0, file_import)
      xform.setInput(0, attrib_del)
      polyreduce.setInput(0, xform)
      # Outputs: Default - 0, Proxy - 1, SimProxy - 2
      comp_sop.children()[0].setInput(0, xform)
      comp_sop.children()[1].setInput(0, polyreduce)
      comp_sop.layoutChildren(sop_nodes)

    #-----Create LOP Nodes------#

    # Variant input - Note: setting inputs later on
    set_variants = hou.node('/stage').createNode('componentgeometryvariants', 'variants')
    for node in range(len(comp_geo_collect)):
      set_variants.setInput(node, comp_geo_collect[node])

    # Get parent dir, cant start with a number
    parent_dir = self._directory.split("/")[-2]
    parent_dir_short = parent_dir.split("_")[1]

    # Material library
    matlib = hou.node('/stage').createNode('materiallibrary', 'matlib')
    matlib.setParms({'matpathprefix':'/ASSET/mtl/'})
    self.atlas_mtl = matlib.createNode('Dpp::doublesided_mtl', parent_dir_short+'_mtl')

    # Component Basics
    comp_mat = hou.node('/stage').createNode('componentmaterial', 'mtl_variant')
    comp_mat.setParms({'variantname':'default'})
    self.comp_output = hou.node('/stage').createNode('componentoutput', parent_dir_short)
    self.comp_output.setParms({'name':parent_dir})
    comp_mat.setInput(0, set_variants); comp_mat.setInput(1, matlib)
    self.comp_output.setFirstInput(comp_mat)

    # Layout Nodes
    lop_nodes = [set_variants, matlib, comp_mat, self.comp_output]
    lop_nodes.extend(comp_geo_collect)
    hou.node('/stage').layoutChildren(lop_nodes)
    

  # Call import texture to import files into material HDA
  def import_textures(self) -> None:
    if(len(self._files) == 0):
      return
    atlas_mtl = self.atlas_mtl

    try:
      # Override inherited directory path and files
      self._directory += "Textures/Atlas/"
      self._files = os.listdir(self._directory)
      tx.TextureImport(atlas_mtl, True, self._files, self._directory)
      self.comp_output.parm('execute').pressButton()

    except AttributeError as err:
      print("Error:", err)

  # Import each fbx for directory
  def import_variants(self) -> None:
    pass

  # Write out USD with variants and mtl
  def write_USD(self) -> None:
    pass
  