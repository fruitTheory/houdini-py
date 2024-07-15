import hou
import os
from importlib import reload
from solaris_utils.ui import file_selector as fs
from solaris_utils import texture_import as tx
reload(tx)


# Write a USD with variants from all scan variations
class VariantImport(fs.FileSelector):

  def __init__(self) -> None:
    super().__init__(title="Variant Import")
    
    self.showui()
    self.button.clicked.connect(self.create_nodes)
    self.button.clicked.connect(self.import_textures)


  def create_nodes(self) -> None:

    # for file in self._files:
    #   if(file.startswith("Var")):
    #     # hou.node('/stage').createNode('componentgeometry', file)
    #     print(os.listdir(self._directory+file))

    comp_geo = hou.node('/stage').createNode('componentgeometry', 'converter')
    comp_geo2 = hou.node('/stage').createNode('componentgeometry', 'converter')

    geo_variants = hou.node('/stage').createNode('componentgeometryvariants', 'variants')
    geo_variants.setInput(0, comp_geo)
    geo_variants.setInput(1, comp_geo2)

    matlib = geo = hou.node('/stage').createNode('materiallibrary', 'matlib')
    matlib.setParms({'matpathprefix':'/ASSET/materials/'})
    self.atlas_mtl = matlib.createNode('Dpp::doublesided_mtl', 'name')

    comp_mat = hou.node('/stage').createNode('componentmaterial', 'default')
    comp_mat.setParms({'variantname':'default'})
    comp_output = hou.node('/stage').createNode('componentoutput', 'test_component')

    comp_mat.setInput(0, geo_variants); comp_mat.setInput(1, matlib)
    comp_output.setFirstInput(comp_mat)

    # Component geo inner SOPs 
    comp_geo_sop = hou.node("/stage/"+comp_geo.name()+"/sopnet/geo")

    file_import = comp_geo_sop.createNode('file', 'fbx_import')
    file_import.setParms({'file':'test.fbx'})

    attrib_del = comp_geo_sop.createNode('attribdelete', 'clean')
    attrib_del.setParms({'ptdel':'N','negate':True, 'vtxdel':'uv', 'primdel':'name'})

    xform = comp_geo_sop.createNode('xform', 'global_scale')
    xform.setParms({'scale':0.01})

    polyreduce = comp_geo_sop.createNode('polyreduce', 'reduce')
    polyreduce.setParms({'percentage':10, 'originalpoints':True})

    attrib_del.setInput(0, file_import)
    xform.setInput(0, attrib_del)
    polyreduce.setInput(0, xform)

    # Default - 0, Proxy - 1, SimProxy - 2
    comp_geo_sop.children()[0].setInput(0, xform)
    comp_geo_sop.children()[1].setInput(0, polyreduce)

  # Call import texture to import files into mtlx HDA
  def import_textures(self) -> None:
    atlas_mtl = self.atlas_mtl

    try:
      # Override inherited directory path and files
      self._directory += "Textures/Atlas/"
      self._files = os.listdir(self._directory)
      tx.TextureImport(atlas_mtl, True, self._files, self._directory)

    except AttributeError as err:
      print("Error:", err)

  # Import each fbx for directory
  def import_variants(self) -> None:
    pass

  # Write out USD with variants and mtl
  def write_USD(self) -> None:
    pass
  