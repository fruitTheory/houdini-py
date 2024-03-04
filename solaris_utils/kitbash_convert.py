import hou


class KitConvert:

    'KB3D_CBD' 'KB3D_MTM' 'KB3D_AOE' # Example name inputs

    stage = hou.node('/stage')
    obj = hou.node('/obj')

    def __init__(self) -> None:
        pass

    def test(self):
        pass

    # Method to convert all avaialable kits - wip
    def convertAll(self) -> None:
        # Simple dialog that returns user input
        # 0 - Convert all, 1 - Convert single, 2 - Don't Convert
        user_selection = hou.ui.readInput( message = 'For single convert input default Kitbash Geo name', initial_contents = "KB3D_AOE", buttons= ["Convert All", "Convert One", "Don't Convert"])

        # If user chooses to cancel
        if(user_selection[0] == 2):
            return

        # Filter for kitbash nodes in obj - use later
        filter_kitbash_nodes = [child for child in self.obj.children() if child.name().startswith('KB3D')]

        kit_list_size = len(filter_kitbash_nodes)
        # print(user_selection)

        if(user_selection[0] == 0):
            for index in range(kit_list_size):
                filter_kitbash_nodes[index].destroyUserData('Converted')

        # Loop and check if create flag already set
        for index in range(kit_list_size):
            if(filter_kitbash_nodes[0].userData('Converted') == 'True'):
                # print('Already created:', filter_kitbash_nodes[0])
                # Needs to be first index always, linear loop
                filter_kitbash_nodes.pop(0)

        # Length of list after pruning
        kit_post_pop = len(filter_kitbash_nodes)

        # Convert any kitbash nodes detected
        if(user_selection[0] == 0):
            for kitbash_name in filter_kitbash_nodes:
                nodes = self.convert(str(kitbash_name))

        if(user_selection[0] == 1):
            self.convert(user_selection[1])

        # Set default user data for remaining kits, a 'flag' to say if already created
        for index in range(kit_post_pop):
            if(kit_post_pop > 0):
                filter_kitbash_nodes[index].setUserData('Converted', 'True')
        

            
    # Convert provided kit name from Obj to Solaris
    def convert(self, name) -> tuple[str, str, str]:

        kitname = name

        get_nodes = self.create_nodes(kitname)
        sopimport = get_nodes[0]
        matlib = get_nodes[1]
        assign_mat = get_nodes[2]
        created_nodes = (sopimport, matlib, assign_mat)

        kitbash_matnet = self.get_kitbash_matnet(kitname)

        copy_src = kitbash_matnet.children()
        copy_dest = matlib # the created material library

        # Cheap guard from doubly copying
        if len(copy_dest.children()) != len(copy_src):
            hou.copyNodesTo(copy_src, copy_dest) # copy from obj to lops
            sopimport.setPicked(1) # stops going into network

        # Set the material flag on for imported materials
        for child in copy_dest.children():
            child.setGenericFlag(hou.nodeFlag.Material, True)

        node_total = len(copy_src)
        assign_mat.parm('nummaterials').set(node_total)

        Stage = assign_mat.stage()

        Materials = []
        GeomSubsets = []

        # Traversing graph, should be a more explicit way to get prims
        for prim in Stage.Traverse():
            if prim.GetTypeName() == 'Mesh':
                GeomSubsets = prim.GetChildrenNames()
            if prim.GetTypeName() == 'Scope':
                Materials = prim.GetChildrenNames()

        # Store each split object into filter geom
        filter_geom = []
        [filter_geom.append(object.split('_')[-1]) for object in GeomSubsets]
        filter_geom.sort()

        # Quick get and set material path
        geo_name = self.get_kitgeo_name(kitname)
        mat_path = '/{}/materials/'.format(geo_name)

        for node_num in range(node_total):
            assign_mat.parm('primpattern{}'.format(node_num+1)).set('*{}'.format(filter_geom[node_num]))
            assign_mat.parm('matspecpath{}'.format(node_num+1)).set('{}{}'.format(mat_path, Materials[node_num]))

        return created_nodes


    # Create and wire needed nodes, returns tuple of nodes
    def create_nodes(self, kitname) -> tuple[str, str, str]:

        nodes_to_create = ('sopimport', 'materiallibrary', 'assignmaterial')
        node_names = ('import', 'matlib', 'assign')

        # get current geo name of kit
        geo_name = self.get_kitgeo_name(kitname)

        # create nodes
        sopimport = hou.node(str(self.stage)).createNode(nodes_to_create[0], geo_name)
        matlib = hou.node(str(self.stage)).createNode(nodes_to_create[1], node_names[1])
        assign_mat = hou.node(str(self.stage)).createNode(nodes_to_create[2], node_names[2])

        # wire inputs
        matlib.setInput(0, sopimport)
        assign_mat.setInput(0, matlib)

        # set default settings
        sopimport.setParms({'primpath':'{}'.format(geo_name)})
        sopimport.setParms({'soppath':'/obj/{}'.format(kitname), 'asreference':True})
        sopimport.setParms({'partitionattribs':'shop_materialpath', 'enable_partitionattribs':True})
        matlib.parm('matpathprefix').set('/{}/materials/'.format(geo_name))
        assign_mat.setParms({'primpattern1':'prim', 'matspecpath1':'material'})

        # store and layout
        created_nodes = (sopimport, matlib, assign_mat)
        self.stage.layoutChildren(created_nodes)

        return created_nodes

    # Returns node that contains materials for specified kitbash
    def get_kitbash_matnet(self, kitname) -> any:
        # find the matnet
        for node in self.obj.children():
            if node.name() == kitname:
                kitbash_matnet = (node.node('matnet'))

        return kitbash_matnet

    # Return string that is name of kitbash geo
    def get_kitgeo_name(self, kitname) -> str:
        kit = self.obj.node(kitname)
        kit_nodes = kit.children()

        for node in kit_nodes:
            if node.name().startswith(kitname):
                geo = node

        geo_name = str(geo).split('_grp')[0]
        geo_name = geo_name.split(kitname + '_')[1]

        return geo_name
    
    # If using aces swap all base colors of selected node
    def convert_to_aces() -> None:
        pass

    # Delete provided nodes
    def delete_nodes(self, nodes) -> None:
        for node in nodes:
            node.destroy()
