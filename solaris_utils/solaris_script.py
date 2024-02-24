import hou

# print('hello')

# def main():

# setups
stage = hou.node('/stage')
stage_str = stage.path()

obj_node = hou.node('/obj')
obj_str = obj_node.path()

nodes_to_create = ('sopimport', 'materiallibrary', 'assignmaterial')
node_names = ('import', 'matlib', 'assign')

# create nodes
sopimport = hou.node(stage_str).createNode(nodes_to_create[0], node_names[0])
matlib = hou.node(stage_str).createNode(nodes_to_create[1], node_names[1])
assign_mat = hou.node(stage_str).createNode(nodes_to_create[2], node_names[2])

# set inputs
matlib.setInput(0, sopimport)
assign_mat.setInput(0, matlib)

# layout  
stage.layoutChildren((sopimport, matlib, assign_mat))

# sop import node
sopimport.setParms({'soppath':'/obj/KB3D_CBD/', 'asreference':True})
sopimport.setParms({'partitionattribs':'shop_materialpath', 'enable_partitionattribs':True})

# assign mat node
assign_mat.setParms({'primpattern1':'prim', 'matspecpath1':'material'})


# get the matnet of user selected kitbash
for node in obj_node.children():
    if node.name() == 'KB3D_CBD':
        print('true')
        kitbash_matnet = node.node('matnet')

copy_src = kitbash_matnet.children()
copy_dest = stage.node('lib') # replace with matlib

# create and set all material connection
assign_mat.parm('nummaterials').set(len(copy_src))
for name in copy_src:
    assign_mat.parm('matspecpath1').set(name.name())

# print(copy_dest, copy_src[0])

# hou.copyNodesTo(copy_src, copy_dest)

# print(copy_dest.children())
# for child in copy_dest.children():
#     child.setGenericFlag('Material', True)


# hou.OpNode.setGenericFlag('Material')


# for each_node in copy_src:
#     hou.copyNodesToClipboard(each_node)
#     hou.pasteNodesFromClipboard(copy_dest.path())


# temp destroy created nodes
# for node in created_node:
#     node.destroy()


# for node in created_nodes:
#     node.moveToGoodPosition()
#     # node.layoutChildren()